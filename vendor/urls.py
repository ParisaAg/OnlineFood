from django.urls import path
from . import views
from accounts import views as AcView



urlpatterns = [
        path('profile/',views.vendorProfile,name='vendorProfile'),
        path('',AcView.VendorDashboard,name='vendor'),
        path('build-menu/',views.menu_builder,name='menu_builder'),
        path('build-menu/category/<int:pk>/',views.food_items_category,name='food_items_category'),


        #category
        path('build-menu/category/add/',views.add_category,name='add_category'),
        path('build-menu/category/edit/<int:pk>/',views.edit_category,name='edit_category'),
        path('build-menu/category/delete/<int:pk>/',views.delete_category,name='delete_category'),
        #food
        path('build-menu/food/add/',views.add_food,name='add_food'),
        path('build-menu/food/edit/<int:pk>/',views.edit_food,name='edit_food'),
        path('build-menu/food/delete/<int:pk>/',views.delete_food,name='delete_food'),



]
