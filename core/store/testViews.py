from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse_lazy
from importlib import import_module

from account.models import UserBase
from .models import Category, Product
from .views import product_all


class TestViewResponse(TestCase):
    """ Test the views of the store package. """

    def setUp(self):
        """" It creates new instances of category, product and user to setup the test. """

        self.c = Client()
        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )

    # TEST on url

    def test_home(self):
        """ Test that the home page is rendered and the status is ok. """

        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)
    
    def test_product_detail(self):
        """ Test that the product detail is rendered and the status is ok. """

        resp = self.c.get(reverse_lazy('store:product_detail', args=['django-beginners']))
        self.assertEqual(resp.status_code, 200)

    def test_category_detail(self):
        """ Test that the category detail is rendered correctly and the status is ok. """

        resp = self.c.get(reverse_lazy('store:category_list', args=['django']))
        self.assertEqual(resp.status_code, 200)



    # TEST on html

    def test_home_html(self):
        """ Like the test_home method but it test the html page. """
        
        req  = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        req.session = engine.SessionStore()
        resp = product_all(req)
        html = resp.content.decode('utf8')

        self.assertIn('<title>MangaStore</title>', html)
        self.assertEqual(resp.status_code, 200)

    