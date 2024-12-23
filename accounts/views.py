from django.shortcuts import render, HttpResponse,redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import DetectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

def check_vendorpermission(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_customerpermission(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST': 
        form=UserForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, "your account has been registered successfully!")
            return redirect('registerUser')
        else:
            print('form-errors') 
            print(form.errors) 
    else:
        form = UserForm()
    context = {
            'form': form
        
        }
    return render(request,'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.Vendor
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor_name = vendor_form.cleaned_data['vendor_name']
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': form,
        'vendor_form': vendor_form,
    }

    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('MyAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user= auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your account has been logged in successfully')
            return redirect('MyAccount')
        else:
            messages.error(request, 'invalid email or password')
            return redirect('login')
    return render(request,'accounts/login.html',)

def logout(request):
    auth.logout(request)
    messages.info(request,'Your account has been logged out.')
    return redirect('login')

@login_required(login_url='login')
def MyAccount(request):
    user = request.user
    redirecturl= DetectUser(user)
    return redirect(redirecturl)


@login_required(login_url='login')
@user_passes_test(check_customerpermission)
def Custdashboard(request):
    return render(request,'accounts/Custdashboard.html',)

@login_required(login_url='login')
@user_passes_test(check_vendorpermission)
def VendorDashboard(request):
    return render(request,'accounts/VendorDashboard.html',)