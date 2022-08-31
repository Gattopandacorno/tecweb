from decimal import Decimal

from store.models import Product

class Cart():
    """ Carrello dei prodotti di un utente. """
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        
        # Se la chiave della sezione non esiste la crea
        if 'skey' not in request.session: 
            cart  = self.session['skey'] = {} 

        self.cart = cart
        
    def add(self, product, qty):
        """ Aggiunge la quantita' specificata di un prodotto nel carrello. """

        product_id = str(product.id)

        # Cambia la quantità se il prodotto e' gia' nel carrello
        if product_id in self.cart: 
            self.cart[product_id]['qty'] = qty
        else:   
            self.cart[product_id] = {'price': str(product.price), 'qty': int(qty) }
        
        self.session.modified = True # Dice a django che e' cambiata la sessione

    def delete(self, product):
        """ Cancella un prodotto dal carrello. """

        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, qty):
        """ Fa l'update di un prodotto se viene cambiata la quantita'. """

        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        
        self.session.modified = True

    def clear(self):
        """ Cancella tutto quello che c'e' nel carrello. """

        del self.session['skey']
        self.session.modified = True

    def __iter__(self):
        """ Itera per tutti i prodotti nel carrello. """

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
        """ Conta la quantita' totale di prodotti nel carrello. """

        return sum(item['qty'] for item in self.cart.values())

    def get_tot_price(self):
        """ Ritorna la somma totale da pagare. """

        return sum(item['qty']*Decimal(item['price']) for item in self.cart.values())
        