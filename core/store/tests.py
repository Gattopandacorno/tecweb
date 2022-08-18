from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from .models import Category, Product, Review


class TestCategoriesModel(TestCase):
    """ Test for the categories. """
    
    def setUp(self):
        """ Creates a new category to setup the test. """

        self.data = Category.objects.create(name='django', slug='django')


    def test_category_model_instance(self):
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
    
    def test_product_model_instance(self):
        """ Test if the data is an istance of the model Product. """

        data = self.data
        self.assertTrue(isinstance(data, Product))

    def test_product_model_entry(self):
        """ Test if the __str__ method in the Product model is correct. """

        data = self.data
        self.assertEqual(str(data), 'django beginners')


class TestReviewModel(TestCase):
    
    def setUp(self):
        """ Creates new entries of Category, Product and UserBase to setUp the tests. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
        
        self.data = Review.objects.create(user_id=1,product_id=1, text='this is a comment', rate=3)
        

    def test_review_model_instance(self):
        """ It tests if the self.data passed is an instance of the Review class. """

        data = self.data
        self.assertIsInstance(data, Review)
    
    def test_review_model_entry(self):
        """ It tests if the __str__ method in Review is correct. """

        data = self.data
        self.assertEquals(str(data), 'this is a comment')