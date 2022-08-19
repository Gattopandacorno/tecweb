from django.test import TestCase
from django.urls import reverse_lazy

from .models import UserBase


class TestUserModel(TestCase):
    
    def setUp(self):
        self.data = UserBase.objects.create(username='admin')        

    def test_review_model_instance(self):

        data = self.data
        self.assertIsInstance(data, UserBase)
    
    def test_review_model_entry(self):
        data = self.data
        self.assertEquals(str(data), 'admin')


class TestUserView(TestCase):

    def setUp(self):
        """ Crea un nuovo utente per i test sugli utenti. """

        self.user = UserBase.objects.create_user(username='user', email='a@a.com', password='user', is_active=True)
        self.credentials = {'username': 'a@a.com', 'password': 'user'}



    def test_login(self):
        """ Testa se viene usato il giusto template per il login. """

        resp = self.client.get(reverse_lazy('account:login'), **self.credentials)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')
        self.assertFalse(resp.context['user'].is_authenticated)

        u = UserBase.objects.get(username='user')
        self.client.force_login(u)
        resp = self.client.get(reverse_lazy('account:login'), **self.credentials)
        self.assertTrue(resp.context['user'].is_authenticated)
        

    def test_registration(self):
        """ Testa se viene usato template per la registrazione """

        resp = self.client.post(reverse_lazy('account:registration'))
        self.assertTemplateUsed(resp, 'account/register.html')

    def test_addseller(self):
        """ Testa se viene richiesto il login se un utente non loggato prova ad aggiungere un membro seller. """
        
        resp = self.client.post(reverse_lazy('account:add_seller'))
        self.assertEqual(resp.status_code, 302)

    def test_profile(self):
        """ Testa se viene richiesto il login se si cercano i dettagli di profilo per un utente non loggato. """

        resp = self.client.post(reverse_lazy('account:profile'))
        self.assertEqual(resp.status_code, 302)
        
        resp = self.client.post(reverse_lazy('account:user_history'))
        self.assertEqual(resp.status_code, 302)
        
        resp = self.client.post(reverse_lazy('account:confirmation'))
        self.assertEqual(resp.status_code, 405)

        resp = self.client.post(reverse_lazy('account:delete'))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse_lazy('account:edit_details'))
        self.assertEqual(resp.status_code, 302)

    def test_logout(self):
        """ Testa che dopo il logout l'utente venga mandato alla home page. """

        resp = self.client.post(reverse_lazy('account:logout'))
        self.assertEqual(resp.status_code, 302)        
        self.assertRedirects(resp, '/')
