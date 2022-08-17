from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from cart.cart import Cart
from account.models import UserBase
from store.models import Product
from .models import Order, OrderItem


def add(request):
    """ Creates the 'payed' order and clears the cart.  """

    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        user = get_object_or_404(UserBase, username=request.user)
        order_key = request.POST.get('order_key')
        carttot = cart.get_tot_price()

        if not Order.objects.filter(order_key=order_key).exists():

            order = Order.objects.create(user=user, tot_paid=carttot, order_key=order_key, billing_status=True)

            # It also creates the new items's order object
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'], price=item['price'], qty=item['qty'])
                qty = Product.objects.get(slug=item['product'].slug).available - item['qty']

                print(qty)
                if qty <= 0:
                    Product.objects.filter(slug=item['product'].slug).update(available=0, in_stock=False)
                else:
                    Product.objects.filter(slug=item['product'].slug).update(available=qty)
        
        cart.clear()
        
        response = JsonResponse({ 'success': 'test' })
        return response

def history(request):
    """ Returns the order history of the user requesting it. """
    
    user = request.user
    orders = Order.objects.filter(user=user, billing_status=True)
    
    return orders