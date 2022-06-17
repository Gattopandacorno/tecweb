from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .cart import Cart
from store.models import  Product


def cart(request):
    return {'cart': Cart(request)}

def cart_summary(request):
    products = Product.objects.all() # TODO: not all the products
    ctx = { 'products': products,
            }
    return render(request, 'store/cart/summary.html', {})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        response = JsonResponse({'test': 'data'})
        return response
