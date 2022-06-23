from dataclasses import field
from django import forms

from .models import UserBase

class RegistrationForm(forms.ModelForm):
    username        = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email           = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'You must provide an email.'})
    password        = forms.CharField(label='Password', widget=forms.PasswordInput)
    validation_pass = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = {'username', 'email',}