from django.urls import path
from . import views
from .views import registerUser



urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
]
