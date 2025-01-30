from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from accounts.views import check_vendorpermission
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify


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


def menu_builder(request):
    vendor=Vendor.objects.get(user=request.user)
    categories= Category.objects.filter(vendor=vendor)
    context={
        'categories': categories,
    }
    return render(request,'vendor/menu_builder.html',context)



def food_items_category(request, pk=None):
    vendor=Vendor.objects.get(user=request.user)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
    context={
        'fooditems':fooditems,
        'category': category,
    }

    return render(request, 'vendor/food_items_category.html',context)



def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=Vendor.objects.get(user=request.user)
            category.slug=slugify(category_name)
            form.save()
            messages.success(request,'new category was created successfully')
            return redirect('menu_builder')
    else:
        form=CategoryForm()
    context={
        'form': form,
    }
    return render(request,'vendor/add_category.html',context)



def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=Vendor.objects.get(user=request.user)
            category.slug=slugify(category_name)
            form.save()
            messages.success(request,'new category updated successfully')
            return redirect('menu_builder')
    else:
        form=CategoryForm(instance=category)
    context={
        'category':category,
        'form': form,
    }
    return render(request,'vendor/edit_category.html',context)



def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'category deleted successfully')
    return redirect('menu_builder')