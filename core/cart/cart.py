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
        product_id = str(product.id)

        if product_id  in self.cart:
            self.cart[product_id]['qty'] = qty
        else:   
            self.cart[product_id] = {'price': str(product.price), 'qty': qty }
        
        self.session.modified = True # Tells django that we changed the session

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['tot_price'] = item['price'] * item['qty']
            yield item

    def __len__(self): # Counts the qty of the items in the cart
        return sum(item['qty'] for item in self.cart.values())

    def get_tot_price(self):
        return sum(int(item['qty'])*Decimal(item['price']) for item in self.cart.values())
        