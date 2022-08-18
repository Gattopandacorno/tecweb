from django.test import TestCase

from account.models import UserBase
from .models import Category, Product, Review


class TestCategoriesModel(TestCase):
    """ Test per le istanze di Category. """
    
    def setUp(self):
        """ Crea una nuova istanza di Category per testarla. """

        self.data = Category.objects.create(name='django', slug='django')


    def test_category_model_instance(self):
        """ Testa se i dati passati sono istanza di Category. """

        data = self.data
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """ Testa il metodo __str__ per Category. """
        data = self.data
        self.assertEqual(str(data), 'django')



class TestProductModel(TestCase):
    """ Test per le istanze di Product. """

    def setUp(self):
        """ Crea Category per creare una nuova istanza di Product. """

        Category.objects.create(name='django', slug='django')
        self.data = Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
    
    def test_product_model_instance(self):
        """ Testa se i dati passati sono istanza di Product. """

        data = self.data
        self.assertTrue(isinstance(data, Product))

    def test_product_model_entry(self):
        """ Testa il metodo  __str__ per Product. """

        data = self.data
        self.assertEqual(str(data), 'django beginners')


class TestReviewModel(TestCase):
    """ Test per le istanze di Review. """
    
    def setUp(self):
        """ Crea una nuova categoria, user e prodotto per creare un istanza di Review. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
        
        self.data = Review.objects.create(user_id=1,product_id=1, text='this is a comment', rate=3)
        

    def test_review_model_instance(self):
        """ Testa se i dati passati sono istanza di Review. """

        data = self.data
        self.assertIsInstance(data, Review)
    
    def test_review_model_entry(self):
        """ Testa il metodo __str__ per Review. """

        data = self.data
        self.assertEquals(str(data), 'this is a comment')