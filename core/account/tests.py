from multiprocessing.connection import Client
from django.test import TestCase
from django.urls import reverse, reverse_lazy

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
        self.user = UserBase.objects.create(username='user', email='a@a.com', password='user', is_active=True)

    def test_login(self):
        resp = self.client.get(reverse_lazy('account:login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/login.html')

    def test_registration(self):
        self.client.post(reverse_lazy('account:logout'), {'action': 'post'})
        resp = self.client.post(reverse_lazy('account:registration'), {'action': 'post'})
        self.assertTemplateUsed(resp, 'account/register.html')

    def test_addseller(self):
        resp = self.client.post(reverse_lazy('account:add_seller'))
        self.assertEqual(resp.status_code, 302)

    def test_profile(self):
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
        resp = self.client.post(reverse_lazy('account:logout'))
        self.assertEqual(resp.status_code, 302)        
        self.assertRedirects(resp, '/')
