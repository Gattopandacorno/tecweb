from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from store.models import Category, Product
from .models import Order, OrderItem


class TestOrderView(TestCase):
    
    def setUp(self):
        """ Setup of the test creating new entry in Category, Product and User. 
        """

        Category.objects.create(name='django', slug='django')
        self.user = UserBase.objects.create(username='user', email='a@a.com', password='user', is_active=True)
        Product.objects.create(category_id=1, title='django advanced',
                                           slug='django-advanced', price=4.50, image='images', available=3)
        Product.objects.create(category_id=1, title='django intermediate',
                                           slug='django-intermediate', price=4.50, image='images', available=3 )
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images', available=3 )
        
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 1, "productqty": 1, "action": "post" }, xhr=True)
        self.client.post( reverse_lazy('cart:cart_add'), {"productid": 2, "productqty": 2, "action": "post" }, xhr=True)


    def test_no_order(self):
        """
            It tests when the user have not already done the checkout.
            There shouldn't be entry in the Order or OrderItem table.
        """
        
        order = Order.objects.all().count()
        self.assertEqual(order, 0)
        
        order_item = OrderItem.objects.all().count()
        self.assertEqual(order_item, 0)


    # TODO: do this
    def test_add(self):
        login = self.client.login(email=self.user.email, password='user')

        self.client.post(reverse_lazy('orders:add'), {'action': 'post'})
      