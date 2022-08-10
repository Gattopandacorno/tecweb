from django.test import TestCase

from account.models import UserBase
from .models import Category, Product


class TestCategoriesModel(TestCase):
    """ Test for the categories. """
    
    def setUp(self):
        """ Creates a new category to setup the test. """
        self.data = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """ Tests if the data is an istance of the model Category. """

        data = self.data
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """ Test if the __str__ method in the Category model is correct. """
        data = self.data
        self.assertEqual(str(data), 'django')



class TestProductModel(TestCase):
    """ Test for products. """

    def setUp(self):
        """ It creates a product with a new Category and a new User to setup the test. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='admin')
        self.data = Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
    
    def test_product_model_entry(self):
        """ Test if the data is an istance of the model Product. """
        data = self.data
        self.assertTrue(isinstance(data, Product))

    def test_product_model_entry(self):
        """ Test if the __str__ method in the Product model is correct. """

        data = self.data
        self.assertEqual(str(data), 'django beginners')