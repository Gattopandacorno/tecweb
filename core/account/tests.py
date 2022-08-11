from multiprocessing.connection import Client
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
        self.user = UserBase.objects.create(username='user', email='a@a.com', password='user', is_active=True)
        # TODO: add login
        
    
    def test_registration(self):
        
        self.client.post(reverse_lazy('account:logout'), {'action': 'post'})
        resp = self.client.post(reverse_lazy('account:registration'), {'action': 'post'})
        self.assertTemplateUsed(resp, 'account/register.html')

