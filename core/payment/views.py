from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import random
import string

from cart.cart import Cart

@login_required
def CartView(request):
    """ 
        Quando un utente vuole fare il checkout 
        viene redirezionato con i giusti dati nella pagina per il pagamento. 
    """

    cart = Cart(request)
    tot  = str(cart.get_tot_price())
    tot  = int(tot.replace('.', ''))
    key  = ''.join(random.choice(string.printable) for _ in range(20)) # Creates the order key
    ctx  = {'client_secret': key,}

    return render(request, 'payment/home.html', context=ctx)


def order_placed(request):
    """ Dopo ogni pagamento viene pulito il carrello. """
    
    cart = Cart(request)
    cart.clear()

    return render(request, 'account/profile.html')