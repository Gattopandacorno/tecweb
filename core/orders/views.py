from msilib.schema import Billboard
from django.shortcuts import render
from django.http.response import JsonResponse

from cart.cart import Cart
from .models import Order, OrderItem

# Create your views here.

def add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        user = request.user
        order_key = request.POST.get('order_key')
        carttot = cart.get_tot_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else: 
            order = Order.objects.create(user=user, tot_paid=carttot, order_key=order_key, billing_status=True)

            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'], price=item['price'], qty=item['qty'])
        
        cart.clear()
        
        response = JsonResponse({ 'success': 'test' })
        return response

def history(request):
    user = request.user
    orders = Order.objects.filter(user=user, billing_status=True)
    
    return orders