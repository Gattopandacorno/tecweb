from decimal import Decimal

from . import cart
from store.models import Product

class Cart():
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session: 
            cart = self.session['skey'] = {} 
        self.cart = cart
        
    def add(self, product, qty):
        if product.id not in self.cart:
            self.cart[product.id] = {'price': str(product.price), 'qty': int(qty) }
        
        self.session.modified = True # Tells django that we changed the session

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['item'])
            item['tot_price'] = item['price'] * item['qty']
        
        yield item

    def __len__(self): # Counts the qty of the items in the cart
        return sum(item['qty'] for item in self.cart.values())
        