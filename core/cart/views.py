from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

import random
import string

from .cart import Cart
from store.models import Product


def cart(request):
    """ Ritorna il carrello di una certa sessione. """

    return {'cart': Cart(request)}

def cart_summary(request):
    """ Rendera la lista corrente dei prodotti nel carrello. """

    cart = Cart(request)
    ctx  = { 'cart': cart }
    return render(request, 'cart/summary.html', ctx)

def cart_add(request):
    """ Aggiunge un prodotto nel carrello. """

    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id  = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        
        tot_qty  = cart.__len__()
        response = JsonResponse({'qty': tot_qty})
        return response


def cart_del(request):
    """ Cancella un prodotto dal carrello. """

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cartqty  = cart.__len__()
        carttot  = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot})
        return response

def cart_update(request):
    """ Cambia la quantita' di un prodotto nel carrello. """

    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=qty)

        cartqty  = cart.__len__()
        carttot  = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot })
        return response

@login_required
def CartView(request):
    """ Il pagamento avviene tramite l'immisione del numero della carta. """

    cart = Cart(request)
    tot  = str(cart.get_tot_price())
    tot  = tot.replace('.', '')
    tot  = int(tot)

    key  = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))

    ctx  = {'client_secret': key}
    return render(request, 'payment/home.html', context=ctx )