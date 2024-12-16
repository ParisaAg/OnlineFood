from django.urls import path
from . import views
from .views import registerUser, registerVendor



urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

]
