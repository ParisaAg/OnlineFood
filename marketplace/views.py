from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from vendor import models
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from .context_processors import get_cart_counter,get_cart_amounts

from marketplace.models import Cart

from django.shortcuts import get_object_or_404
# Create your views here.

def MarketPlace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_counts=vendors.count()
    context = {
        'vendors': vendors,
        'vendor_counts':vendor_counts,
    }
    return render(request,'marketplace/listing.html',context)


def vendor_detail(request,vendor_slug):
    vendor= get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories =Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cert_items = Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cert_items':cert_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)




def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    



def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context={
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html',context)