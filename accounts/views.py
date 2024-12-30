from django.shortcuts import render, HttpResponse,redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import DetectUser,send_verfication_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



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
        return redirect('Custdashboard')
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

            mail_subject = 'verify your email address'
            email_template = 'accounts/emails/verify_email.html'
            send_verfication_email(request, user,mail_subject,email_template)
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
        return redirect('Vendordashboard')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get_or_create(user=user)[0]
            vendor_name = vendor_form.cleaned_data['vendor_name']
            vendor.save()

            # Send verification email

            mail_subject = 'verify your email address'
            email_template = 'accounts/emails/verify_email.html'
            send_verfication_email(request, user,mail_subject,email_template)        

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


def activate(request, uidb64 ,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user= User._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,' thanks for activation! now your account has been activated')
        return redirect('MyAccount')
    else:
        messages.error(request,'invalid activation code! Please try again later')
        return redirect('MyAccount')


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

def forgot_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            
            mail_subject = 'reset password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verfication_email(request,user,mail_subject,email_template)

            messages.success(request,'reset password link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'this account is not exist')
            return redirect('registerUser')
    return render(request,'accounts/forgot_password.html')

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
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')




def reset_password_validate(request,uidb64,token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')