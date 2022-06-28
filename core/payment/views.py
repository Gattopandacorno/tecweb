from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import random
import string

from cart.cart import Cart
# Create your views here.

@login_required
def CartView(request):
    cart = Cart(request)
    tot = str(cart.get_tot_price())
    tot = int(tot.replace('.', ''))
    key = ''.join(random.choice(string.printable) for i in range(20))
    ctx = {'client_secret': key,}

    return render(request, 'payment/home.html', context=ctx)


