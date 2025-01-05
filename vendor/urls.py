from django.urls import path
from . import views
from accounts import views as AcView



urlpatterns = [
            path('profile/',views.vendorProfile,name='vendorProfile'),
            path('',AcView.VendorDashboard,name='vendor'),

]
