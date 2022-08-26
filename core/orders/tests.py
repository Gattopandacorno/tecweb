from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from cart.cart import Cart
from store.models import Category, Product
from .models import Order, OrderItem


class TestOrderView(TestCase):
    
    def setUp(self):
        """ Crea categoria, user e prodotti per i test sul carrello. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create_user(username='user', email='a@a.com', password='user', is_active=True)
        self.credentials = {'username': 'a@a.com', 'password': 'user'}

        Product.objects.create(category_id=1, title='django advanced',
                                           slug='django-advanced', price=4.50, image='images', available=1)
        Product.objects.create(category_id=1, title='django intermediate',
                                           slug='django-intermediate', price=4.50, image='images', available=3 )
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images', available=3 )
        
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 1, "productqty": 1, "action": "post" }, xhr=True)
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 2, "action": "post" }, xhr=True)


    def test_no_order(self):
        """ Testa che non esistano entry quando non sono ancora stati aggiunti gli ordini. """
        
        order = Order.objects.all().count()
        self.assertEqual(order, 0)
        
        order_item = OrderItem.objects.all().count()
        self.assertEqual(order_item, 0)


    def test_add(self):

        resp = self.client.post(reverse_lazy('payment:cartview'))
        self.assertEqual(resp.status_code, 302)

        u = UserBase.objects.get(username='user')
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('payment:cartview'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'payment/home.html')
        self.assertTrue(resp.context['user'].is_authenticated)

        
        resp = self.client.post(reverse_lazy('orders:add'), 
                               {'action': 'post', 'csrfmiddlewaretoken': resp.context['csrf_token'], 'order_key': resp.context['client_secret']})

        self.assertEqual(resp.status_code, 200)
        
        o = Order.objects.all()
        self.assertIsNotNone(list(o))
        o = OrderItem.objects.all()
        self.assertIsNotNone(list(o))

        p = Product.objects.get(title='django advanced')
        self.assertFalse(p.in_stock)