from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .cart import Cart
from store.models import  Product


def cart(request):
    return {'cart': Cart(request)}

def cart_summary(request):
    cart = Cart(request)
    ctx = { 'cart': cart }
    return render(request, 'store/cart/summary.html', ctx)

def cart_add(request):
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
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)

        cartqty = cart.__len__()
        carttot = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        qty = int(request.POST.get('productqty'))
        cart.update(product=product_id, qty=qty)

        cartqty = cart.__len__()
        carttot = cart.get_tot_price()
        response = JsonResponse({'qty': cartqty, 'subtotal': carttot})
        return response