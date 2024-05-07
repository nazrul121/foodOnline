from django.shortcuts import render, get_object_or_404, HttpResponse
from vendor.forms import VendorForm

# Create your views here.
from django.shortcuts import render, redirect
from accounts.models import UserProfile
from .models import Vendor
from accounts.forms import UserProfileForm
from django.contrib import messages



from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor



def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendor-profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/profile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)

def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendor-profile')
    else:
        # to set data into form input field, Django use formName(isinstance)
        # instance = modelName
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    data = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/profile.html', data)