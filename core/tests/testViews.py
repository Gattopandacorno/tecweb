from unittest import skip
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpRequest

from store.models import Category, Product
from store.views import product_all


class TestViewResponse(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                           slug='django-beginners', price=4.50, image='images' )

    # TEST on url

    def test_home(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)
    
    def test_product_detail(self):
        resp = self.c.get(reverse_lazy('store:product_detail', args=['django-beginners']))
        self.assertEqual(resp.status_code, 200)

    def test_category_detail(self):
        resp = self.c.get(reverse_lazy('store:category_list', args=['django']))
        self.assertEqual(resp.status_code, 200)

    """  
    def test_allowed_hosts(self):
        resp = self.c.get('/', HTTP_HOST='noaddr.com')
        self.assertEqual(resp.status_code, 400)
    """

    # TEST on html

    def test_home_html(self):
        req  = HttpRequest()
        resp = product_all(req)
        html = resp.content.decode('utf8')

        self.assertIn('<title>MangaStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(resp.status_code, 200)

    def test_view_fun(self):
        req = self.factory.get('/django-beginners')
        resp = product_all(req)
        html = resp.content.decode('utf8')

        self.assertIn('<title>MangaStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(resp.status_code, 200)