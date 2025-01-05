from django.urls import path,include
from . import views
from .views import registerUser, registerVendor



urlpatterns = [
    path('',views.MyAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('MyAccount/', views.MyAccount, name='MyAccount'),
    path('Custdashboard/', views.Custdashboard, name='Custdashboard'),
    path('VendorDashboard/', views.VendorDashboard, name='VendorDashboard'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('vendor/',include('vendor.urls')),



]
