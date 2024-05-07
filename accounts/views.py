from django.shortcuts import render, HttpResponse, redirect
from .forms import registerFrom, LoginForm,UserProfile
from vendor.forms import VendorForm
from django.contrib import messages, auth
from .models import User
from .holper import detectUser, send_verification_email
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import get_user_model
from django.db.models import Q

from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied #redirct to 403 error page
    


# Create your views here.
def register(request):
    
    form = registerFrom()

    if request.method == 'POST':
        form = registerFrom(request.POST)
        # return HttpResponse(request.POST['password'])
        if form.is_valid():
            # Create the user using the form
            password = form.cleaned_data['password']

            user = form.save(commit=False)
        
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'account/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('register')
        else:
            messages.warning(request, 'Please fill up the form correctly!')
    else:
        form = registerFrom()

    data = {
        'form':form
    }
    return render(request, 'account/register.html', data)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in!')
        return redirect('my-account')
    
    if request.method == 'POST':
        form = registerFrom(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.VENDOR

            user.save()
            user_profile = UserProfile.objects.get(user=user)

            vendor = v_form.save(commit=False)
            vendor.user_profile = user_profile

            vendor.user = user
            vendor.slug = slugify(vendor.vendor_name)+'-'+str(user.id)

            vendor.save()
            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'account/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('vendor-register')
        else:
            messages.warning(request, 'Please fillup the form correctly!')
    else:
        v_form = VendorForm()
        form = registerFrom()

    data = {
        'v_form':v_form,
        'form':form,
    }
    return render(request, 'account/vendor-register.html', data)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Welcome to Your account')
        return redirect('my-account')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
         
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # user = authenticate(request, username=username, password=password)
            
            user = User.objects.filter(
                Q(username=username) | Q(email=username) | Q(phone_number=username)
            ).first()

            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    # If authentication is successful, log the user in
                    auth.login(request, user)
               
                    messages.success(request, f'Welcome {user.first_name} {user.last_name}')
                    return redirect('my-account')
                else:
                    messages.error(request, 'Invalid login credentials')
                    # return redirect('login')
            else:
                messages.error(request, 'Username is not matching to active users')
                # return redirect('login')
        else:
            messages.error(request, 'Invalid login credentials')
            # return redirect('login')
    else: 
        form = LoginForm()


    data = {'form': form}
    return render(request, 'account/login.html', data)



def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('my-account')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('my-account')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You have logged out successfully.')
    return redirect('login')


@login_required(login_url='login') #login decorator to prevent user access without login
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user) #this is a helper info
    # return HttpResponse(redirectUrl)
    return redirect(redirectUrl)




@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'account/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'account/vendorDashboard.html')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'account/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot-password')
        
    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset-password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('my-account')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset-password')
    return render(request, 'account/reset_password.html')