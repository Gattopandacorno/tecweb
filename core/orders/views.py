from xml.dom import UserDataHandler
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from cart.cart import Cart
from account.models import UserBase
from .models import Order, OrderItem


def add(request):
    """ Creates the 'payed' order and clears the cart.  """

    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        user = get_object_or_404(UserBase, username=request.user)
        order_key = request.POST.get('order_key')
        carttot = cart.get_tot_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else: 
            order = Order.objects.create(user=user, tot_paid=carttot, order_key=order_key, billing_status=True)

            # It also creates the new items's order object
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'], price=item['price'], qty=item['qty'])
        
        cart.clear()
        
        response = JsonResponse({ 'success': 'test' })
        return response

def history(request):
    """ Returns the order history of the user requesting it. """
    
    user = request.user
    orders = Order.objects.filter(user=user, billing_status=True)
    
    return orders