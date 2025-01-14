from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from accounts.views import check_vendorpermission


@login_required(login_url='login')
@user_passes_test(check_vendorpermission)
def vendorProfile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method =='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'form has been updated successfully')
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else: 
        profile_form=UserProfileForm(instance=profile)
        vendor_form=VendorForm(instance=vendor)

        
    context={
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html',context)
