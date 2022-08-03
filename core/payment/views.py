from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import random
import string

from cart.cart import Cart

@login_required
def CartView(request):
    """ When a user want to checkout the order, it will be redirected to the payment system. """

    cart = Cart(request)
    tot = str(cart.get_tot_price())
    tot = int(tot.replace('.', ''))
    key = ''.join(random.choice(string.printable) for i in range(20))
    ctx = {'client_secret': key,}

    return render(request, 'payment/home.html', context=ctx)


def order_placed(request):
    """ After the payment is done it clears the cart. """
    
    cart = Cart(request)
    cart.clear()
    return render(request, 'account/profile.html')