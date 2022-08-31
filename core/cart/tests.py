from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from store.models import Category, Product

# XHR è usato per ajax requests (X)

class TestCartView(TestCase):
    """ Set di test sulle view del carrello. """
    
    def setUp(self):
        """ Crea user, categoria e prodotti. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='user', email='a@a.com', password='user')
        Product.objects.create(category_id=1, title='django advanced',
                                           slug='django-advanced', price=4.50, image='images', available=3)
        Product.objects.create(category_id=1, title='django intermediate',
                                           slug='django-intermediate', price=4.50, image='images', available=3 )
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images', available=3 )

        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 1, "productqty": 1, "action": "post" }, xhr=True)
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 2, "action": "post" }, xhr=True)


    def test_cart(self):
        """ 
            Testa se un cliente può vedere il carrello. 
            Non importa che l'utente sia loggato poiche' anche un anonimo puo' vederlo. 
        """

        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart/summary.html')
        self.assertEqual(len(resp.context['cart']), 3) # Sono 3 poiche' ho un prodotto id=1 e due prodotti id=2

    def test_cart_add(self):
        """ 
            Testa se possono essere aggiunti altri prodotti al carrello.
            Non importa che l'utente sia loggato.  
        """

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 3, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 4 })
        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(len(resp.context['cart']), 4) # Aggiungo un nuovo prodotto ai 3 di prima

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 3 })
        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(len(resp.context['cart']), 3) # Ai 4 prodotti di prima chiedo di 'toglierne' uno dal prodotto id=2

    def test_cart_del(self):
        """ Testa se possono essere cancellati dei prodotti dal carrello. """

        resp = self.client.post(reverse_lazy('cart:cart_del'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 1, 'subtotal': '4.50' })
        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(len(resp.context['cart']), 1)

    def test_cart_update(self):
        """ Testa se puo' essere selezionata una quantita' diversa per un prodotto nel carrello. """
        
        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 2 }) 
        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(len(resp.context['cart']), 2)