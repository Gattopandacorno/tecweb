from django.test import TestCase
from django.urls import reverse_lazy

from account.models import UserBase
from .models import Category, Product, Review


class TestCategoriesModel(TestCase):
    """ Test per le istanze di Category. """
    
    def setUp(self):
        """ Crea una nuova istanza di Category per testarla. """

        self.data = Category.objects.create(name='django', slug='django')


    def test_category_instance(self):
        """ Testa se i dati passati sono istanza di Category. """

        data = self.data
        self.assertTrue(isinstance(data, Category))

    def test_category_entry(self):
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
    
    def test_product_instance(self):
        """ Testa se i dati passati sono istanza di Product. """

        data = self.data
        self.assertTrue(isinstance(data, Product))

    def test_product_entry(self):
        """ Testa il metodo  __str__ per Product. """

        data = self.data
        self.assertEqual(str(data), 'django beginners')


class TestReviewModel(TestCase):
    """ Test per le istanze di Review. """
    
    def setUp(self):
        """ Crea una nuova categoria, user e prodotto per creare un istanza di Review. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create_user(username='admin', email='admin@a.com', password='admin')
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
        
        self.data = Review.objects.create(user_id=1,product_id=1, text='this is a comment', rate=3)
        

    def test_review_instance(self):
        """ Testa se i dati passati sono istanza di Review. """

        data = self.data
        self.assertIsInstance(data, Review)
    
    def test_review_entry(self):
        """ Testa il metodo __str__ per Review. """

        data = self.data
        self.assertEquals(str(data), 'this is a comment')


class TestStoreView(TestCase):

    def setUp(self):
        """ Crea una nuova categoria, user e prodotto. """

        Category.objects.create(name='django', slug='django')
        UserBase.objects.create_user(username='user', email='a@a.com', password='user', is_active=True)
        Product.objects.create(category_id=1, title='django beginners',
                                           slug='django-beginners', price=4.50, image='images' )
        self.credentials = {'username': 'a@a.com', 'password': 'user'}

    def test_product_detail(self):
        """ Controlla che vengano visti tutti i dettagli di un prodotto nella pagina. """

        resp = self.client.post('/django-beginners/') 
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/single.html')
        self.assertEqual(list(resp.context['reviews']), [])
        self.assertIsNotNone(resp.context['product'])


        Review.objects.create(user_id=1,product_id=1, text='this is a comment', rate=3)
        resp = self.client.post('/django-beginners/')
        self.assertNotEqual(list(resp.context['reviews']), [])

    def test_category(self):
        """ Testa che vengano correttamente passati tutti i prodotti di una certa categoria. """

        resp = self.client.post('/shop/django/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/category.html')
       
        self.assertNotEqual(list(resp.context['products']), [])
        self.assertEqual(len(list(resp.context['products'])), 1)
        
        self.assertIsNotNone(resp.context['category'], )

    def test_product_all(self):
        """ Testa che vengano correttamente passati tutti i prodotti nel database alla homepage. """

        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/home.html')
        self.assertNotEqual(list(resp.context['products']), [])
        self.assertEqual(len(list(resp.context['products'])), 1)

    def test_create_product(self):
        """ Testa che venga correttamente salvata l'istanza di un nuovo prodotto e che non sia accessibile a tutti gli utenti."""

        # Prova con utente anonimo
        resp = self.client.post(reverse_lazy('store:create_product'))
        self.assertEqual(resp.status_code, 302)
        self.assertTemplateNotUsed(resp, '/')

        # Prova con utente cliente
        u = UserBase.objects.create_user(username='user1', email='user@us.com', password='user1')
        self.client.force_login(u)        
        resp = self.client.post(reverse_lazy('store:create_product'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        # Prova con utente admin
        u = UserBase.objects.create_user(username='admin', email='admin@a.com', password='admin', is_staff=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_product'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/createprod.html')
        self.assertEqual(str(resp.context['user']), 'admin')
        self.assertTrue(resp.context['user'].is_authenticated)

        # Prova con utente venditore
        u = UserBase.objects.create_user(username='seller', email='seller@s.com', password='seller', is_seller=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_product'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/createprod.html')
        self.assertEqual(str(resp.context['user']), 'seller')
        self.assertTrue(resp.context['user'].is_authenticated)
        
    def test_create_category(self):
        """ 
            Test per vedere se la categoria viene correttamente salvata nel database. 
            Non essendo disponibile a tutti gli utenti si fanno i test con tutti i tipi di utenti.
        """

        # Prova con utente anonimo
        resp = self.client.post(reverse_lazy('store:create_category'))
        self.assertEqual(resp.status_code, 302)
        self.assertTemplateNotUsed(resp, '/')

        # Prova con utente cliente
        u = UserBase.objects.create_user(username='user1', email='user@us.com', password='user1')
        self.client.force_login(u)        
        resp = self.client.post(reverse_lazy('store:create_category'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        # Prova con utente admin
        u = UserBase.objects.create_user(username='admin', email='admin@a.com', password='admin', is_staff=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_category'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/createcat.html')
        self.assertEqual(str(resp.context['user']), 'admin')
        self.assertTrue(resp.context['user'].is_authenticated)

        # Prova con utente venditore
        u = UserBase.objects.create_user(username='seller', email='seller@s.com', password='seller', is_seller=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_category'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/createcat.html')
        self.assertEqual(str(resp.context['user']), 'seller')
        self.assertTrue(resp.context['user'].is_authenticated)

        # Finalmente prova ad aggiungere una nuova categoria di nome python
        resp = self.client.post(reverse_lazy('store:create_category'), {'action': 'post', 'name': 'python' })
        c = Category.objects.get(name='python')
        self.assertTrue(c)       

    def test_search(self):
        """ 
            Test che prova la funzione di ricerca dei prodotti, 
            essendo un azione disponibile a tutti i tipi di utente non vi è alcun login.
        """

        resp = self.client.get(reverse_lazy('store:search'), {})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        resp = self.client.get(reverse_lazy('store:search'), {'word': 'django'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/category.html')
        self.assertEqual(str(resp.context['category']), 'Searched: django')
        self.assertEqual(len(list(resp.context['products'])), 1)

        resp = self.client.get(reverse_lazy('store:search'), {'word': 'django2'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/products/category.html')
        self.assertEqual(str(resp.context['category']), 'Searched: django2')
        self.assertEqual(len(list(resp.context['products'])), 0)

    def test_create_review(self):
        """ Prova per ogni utente, tranne il compratore, che non si possa creare una recensione. """

        # Prova senza login, con utente anonimo
        resp = self.client.post(reverse_lazy('store:create_review', kwargs={'slug': 'django-beginners'}), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')

        # Prova con utente  admin
        u = UserBase.objects.create_user(username='admin', email='admin@a.com', password='admin', is_staff=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_review', kwargs={'slug': 'django-beginners'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        # Prova con utente venditore
        u = UserBase.objects.create_user(username='seller', email='seller@s.com', password='seller', is_seller=True)
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('store:create_review', kwargs={'slug': 'django-beginners'}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        # Prova con utente cliente
        u = UserBase.objects.create_user(username='user1', email='user@us.com', password='user1')
        self.client.force_login(u)        
        resp = self.client.post(reverse_lazy('store:create_review', kwargs={'slug': 'django-beginners'}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'store/rating/home.html')

        # Finalmente si prova a creare una nuova istanza di review
        resp = self.client.post(reverse_lazy('store:create_review', kwargs={'slug': 'django-beginners'}), 
                            {'action': 'post', 'rate': 3,'text': 'This is a comment' })
        r = Review.objects.all()
        self.assertTrue(list(r))
        self.assertRedirects(resp, '/django-beginners/')