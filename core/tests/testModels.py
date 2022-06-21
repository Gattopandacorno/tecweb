from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Category, Product

class TestCategoriesModel(TestCase):
    
    def setUp(self):
        self.data = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        data = self.data
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        data = self.data
        self.assertEqual(str(data), 'django')



class TestProductModel(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data = Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
    
    def test_product_model_entry(self):
        data = self.data
        self.assertTrue(isinstance(data, Product))

    def test_product_model_entry(self):
        data = self.data
        self.assertEqual(str(data), 'django beginners')