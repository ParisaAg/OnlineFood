from django.urls import path,include
from . import views



urlpatterns = [
    path('',views.MarketPlace,name='marketplace'), 
    path('<slug:vendor_slug>/',views.vendor_detail,name='vendor_detail'), 
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('cart', views.cart, name='cart'),


]