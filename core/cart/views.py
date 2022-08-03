from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

import random
import string

from .cart import Cart
from store.models import  Product


def cart(request):
    """ Returns the cart of the current session. """

    return {'cart': Cart(request)}

def cart_summary(request):
    """ Renders the list of the product in the cart. """

    cart = Cart(request)
    ctx = { 'cart': cart }
    return render(request, 'cart/summary.html', ctx)

def cart_add(request):
    """ Adds a new item in the cart. It changes the number of the cart logo. """

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        
        tot_qty = cart.__len__()
        response = JsonResponse({'qty': tot_qty})
        return response


def cart_del(request):
    """ Delete the selected item. It changes the number of the cart logo and subtotal. """

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cartqty = cart.__len__()
        carttot = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot})
        return response

def cart_update(request):
    """ After changing the quantity of a product it changes subtotal with the new price. """

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=qty)

        cartqty = cart.__len__()
        carttot = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot })
        return response

@login_required
def CartView(request):
    """ If the user is logged in it can view the payment system.
        Notice that the only logic in the payment system is to controll the input is a number.
    """

    cart = Cart(request)
    tot  = str(cart.get_tot_price())
    tot  = tot.replace('.', '')
    tot  = int(tot)

    key = ''.join(random.choice(string.ascii_lowercase) for i in range(20))

    ctx = {'client_secret': key}
    return render(request, 'payment/home.html', context=ctx )