from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from store.models import Category, Product

# XHR è usato per ajax requests (X)

class TestCartView(TestCase):
    
    def setUp(self):
        """ Crea  user, categoria e prodotti per i test sul carrello. """

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
        """ Testa se il cliente può vedere il carrello. """

        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(resp.status_code, 200)

    def test_cart_add(self):
        """ Testa se possono essere aggiunti altri prodotti al carrello. """

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 3, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 4 })

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 3 })

    def test_cart_del(self):
        """ Testa se possono essere cancellati dei prodotti dal carrello. """

        resp = self.client.post(reverse_lazy('cart:cart_del'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 1, 'subtotal': '4.50' })

    def test_cart_update(self):
        """ Testa se può essere selezionata una quantità diversa per un prodotto nel carrello. """
        
        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 2 }) 