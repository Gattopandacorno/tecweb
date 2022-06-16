import sys
from django.shortcuts import render
import sys

from .cart import Cart
from store.models import  Product


def cart(request):
    return {'cart': Cart(request)}

def cart_summary(request):
    products = Product.objects.all() # TODO: taking all the products
    ctx = { 'products': products,
            }
    return render(request, 'store/cart/summary.html', context=ctx)