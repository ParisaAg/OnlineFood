from django.urls import path
from . import views
from .views import registerUser, registerVendor



urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('MyAccount/', views.MyAccount, name='MyAccount'),
    path('Custdashboard/', views.Custdashboard, name='Custdashboard'),
    path('VendorDashboard/', views.VendorDashboard, name='VendorDashboard'),

]
