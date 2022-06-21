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
        Category.objects.create(name='manga', slug='manga')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='Manga1', created_by_id=1,
                                           slug='Manga1', price=4.50, image='images' )

    # TEST on url

    def test_home(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 200)
    
    def test_product_detail(self):
        resp = self.c.get(reverse_lazy('store:product_detail', args=['Manga1']))
        self.assertEqual(resp.status_code, 200)

    def test_category_detail(self):
        resp = self.c.get(reverse_lazy('store:category_list', args=['manga']))
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
        req = self.factory.get('/Manga1')
        resp = product_all(req)
        html = resp.content.decode('utf8')

        self.assertIn('<title>MangaStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(resp.status_code, 200)