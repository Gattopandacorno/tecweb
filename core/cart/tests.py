from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from store.models import Category, Product

# XHR is used to do an ajax request (X)

class TestCartView(TestCase):
    
    def setUp(self):
        """ Setup of the test. 
            It creates instances of User, Category and Product.
            Then it adds the products in the cart of the created user.
        """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django advanced',
                                           slug='django-advanced', price=4.50, image='images', available=3)
        Product.objects.create(category_id=1, title='django intermediate',
                                           slug='django-intermediate', price=4.50, image='images', available=3 )
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images', available=3 )

        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 1, "productqty": 1, "action": "post" }, xhr=True)
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 2, "action": "post" }, xhr=True)


    def test_cart(self):
        """ Tests if the user can see the cart summary. """

        resp = self.client.get(reverse_lazy('cart:cart_summary'))
        self.assertEqual(resp.status_code, 200)

    def test_cart_add(self):
        """ Tests if the user can add other products to the cart. """

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 3, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 4 })

        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 3 })

    def test_cart_del(self):
        """ Tests if the user can delete a product from the cart. """

        resp = self.client.post(reverse_lazy('cart:cart_del'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 1, 'subtotal': '4.50' })

    def test_cart_update(self):
        """ Tests if the user can change the quantity of a product already in the cart. """
        
        resp = self.client.post(reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 1, "action": "post" }, xhr=True )
        self.assertEqual(resp.json(), { 'qty': 2 }) 