from decimal import Decimal

from store.models import Product

class Cart():
    """ The cart is the collection of products buyed by a customer. """
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        
        # If the key of the session doesn't exist it creates it
        if 'skey' not in request.session: 
            cart = self.session['skey'] = {} 

        self.cart = cart
        
    def add(self, product, qty):
        """ Adds the selected quantity of a product in the cart. """

        product_id = str(product.id)

        # If the product is already in the cart it only changes the quantity
        if product_id in self.cart: 
            self.cart[product_id]['qty'] = qty
        else:   
            self.cart[product_id] = {'price': str(product.price), 'qty': int(qty) }
        
        self.session.modified = True # Tells django that we changed the session

    def delete(self, product):
        """ Deletes a product from the list in the cart. """

        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, qty):
        """ Updates the quantity of the selected product. """

        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        
        self.session.modified = True

    def clear(self):
        """ Clear cart of the current session. """

        del self.session['skey']
        self.session.modified = True

    def __iter__(self):
        """ Iterates over the products of the cart. """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['tot_price'] = item['price'] * item['qty']
            yield item

    def __len__(self): 
        """ Counts the qty of the items in the cart. """

        return sum(item['qty'] for item in self.cart.values())

    def get_tot_price(self):
        """ Returns the sum to pay. """
        return sum(item['qty']*Decimal(item['price']) for item in self.cart.values())
        