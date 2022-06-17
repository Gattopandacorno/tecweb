class Cart():
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')

        if 'skey' not in request.session:
            cart = self.session['skey'] = {'num': 12344 } 
            self.cart = cart
            if 'skey' not in request.session:
                cart = self.session['skey'] = {'number': 1013483} 
                self.cart = cart

    def add(self, product):
        product_id = product.id

        if product_id not in self.cart:
            self.cart[product_id] = {'price': product.price}
        
        self.session.modified = True