from django.test import TestCase
from django.urls import reverse_lazy

from .models import UserBase


class TestUserModel(TestCase):
    """ Set di test sull'istanza di UserBase. """
    
    def setUp(self):
        """ Crea un utente. """
        self.data = UserBase.objects.create_user(username='admin', email='admin@a.com', password='admin')        

    def test_user_model_instance(self):
        """ Testa che i dati creati come UserBase siano di quell'istanza. """

        data = self.data
        self.assertIsInstance(data, UserBase)
    
    def test_user_model_entry(self):
        """ Testa che i dati ritornino la stringa corretta se passatti alla funzione str. """

        data = self.data
        self.assertEquals(str(data), 'admin')


class TestUserView(TestCase):
    """ Set di test sulle view create per gli user. """

    def setUp(self):
        """ Crea nuovi utenti. Uno admin e uno normale. """

        UserBase.objects.create_user(username='user', email='a@a.com', password='user')
        UserBase.objects.create_user(username='admin', email='admin@a.com', is_staff=True, password='admin')
        self.credentials = {'username': 'a@a.com', 'password': 'user'}

    def test_login(self):
        """ Testa alcuni aspetti del login di un utente. """

        resp = self.client.get(reverse_lazy('account:login'), **self.credentials)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')
        self.assertFalse(resp.context['user'].is_authenticated)

        u = UserBase.objects.get(username='user')
        self.client.force_login(u)
        resp = self.client.get(reverse_lazy('account:login'), **self.credentials)
        self.assertTrue(resp.context['user'].is_authenticated)
        
    def test_registration(self):
        """ Testa alcuni aspetti della parte di registrazione. """

        resp = self.client.post(reverse_lazy('account:registration'))
        self.assertTemplateUsed(resp, 'account/register.html')

        u = UserBase.objects.get(username='user')
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('account:registration'))
        self.assertRedirects(resp, '/')

    def test_addseller(self):
        """ Testa per ogni utente come reagisce il sistema alla richiesta di creare un nuovo seller. """
        
        # Se l'utente e' anonimo
        resp = self.client.post(reverse_lazy('account:add_seller'))
        self.assertEqual(resp.status_code, 302)

        # Se l'utente e' normale
        u = UserBase.objects.get(username='user')
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('account:add_seller'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        # Se l'utente e' un admin
        u = UserBase.objects.get(username='admin')
        self.client.force_login(u)
        resp = self.client.post(reverse_lazy('account:add_seller'))
        self.assertTrue(resp.context['user'].is_authenticated)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/register.html')
        
    def test_profile(self):
        """ Testa come reagisce il sistema per un utente che chiede di vedere il profilo. """

        # Se l'utente e' anonimo
        resp = self.client.post(reverse_lazy('account:profile'))
        self.assertEqual(resp.status_code, 302)
        
        resp = self.client.post(reverse_lazy('account:user_history'))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse_lazy('account:edit_details'))
        self.assertEqual(resp.status_code, 302)
        
        resp = self.client.post(reverse_lazy('account:delete'))
        self.assertEqual(resp.status_code, 302)

        
        # Se e' un admin
        u = UserBase.objects.get(username='admin')
        self.client.force_login(u)

        resp = self.client.post(reverse_lazy('account:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['user'].is_authenticated)
        
        resp = self.client.post(reverse_lazy('account:user_history'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse_lazy('account:edit_details'))
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.post(reverse_lazy('account:delete'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/account/profile/confirmation/')
        
        u = UserBase.objects.get(username='user')
        self.assertTrue(u.is_active)


        # Se e' un utente normale
        u = UserBase.objects.get(username='user')
        self.client.force_login(u)

        resp = self.client.post(reverse_lazy('account:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['user'].is_authenticated)
        
        resp = self.client.post(reverse_lazy('account:user_history'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse_lazy('account:edit_details'))
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.post(reverse_lazy('account:delete'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/account/profile/confirmation/')
       
        u = UserBase.objects.get(username='user')
        self.assertFalse(u.is_active)

        # Se e' un seller
        u = UserBase.objects.create_user(username='seller', email='seller@s.com', password='seller')
        self.client.force_login(u)

        resp = self.client.post(reverse_lazy('account:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['user'].is_authenticated)
        
        resp = self.client.post(reverse_lazy('account:user_history'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse_lazy('account:edit_details'))
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.post(reverse_lazy('account:delete'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/account/profile/confirmation/')
        
        u = UserBase.objects.get(username='user')
        self.assertFalse(u.is_active)

    def test_logout(self):
        """ Testa che dopo il logout si venga rimandati alla home page. """

        resp = self.client.post(reverse_lazy('account:logout'))
        self.assertEqual(resp.status_code, 302)        
        self.assertRedirects(resp, '/')