from django.shortcuts import render, HttpResponse, redirect
from .forms import registerFrom
from vendor.forms import VendorForm
from django.contrib import messages
from .models import User


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

            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('register')
        else:
            messages.warning(request, 'Please fill up the form correctly!')
    else:
        form = registerFrom()

    data = {
        'form':form
    }
    return render(request, 'frontend/account/register.html', data)



def registerVendor(request):
    if request.method == 'POST':
        form = registerFrom(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.save()
            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('home')
        else:
            messages.warning(request, 'Please fillup the form correctly!')
    else:
        v_form = VendorForm()
        form = registerFrom()

    data = {
        'v_form':v_form,
        'form':form,
    }
    return render(request, 'frontend/account/vendor-register.html', data)


