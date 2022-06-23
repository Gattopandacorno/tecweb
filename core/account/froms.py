from dataclasses import field
from logging import PlaceHolder
from xml.dom import ValidationErr
from django import forms

from .models import UserBase

class RegistrationForm(forms.ModelForm):
    username        = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email           = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'You must provide an email.'})
    password        = forms.CharField(label='Password', widget=forms.PasswordInput)
    validation_pass = forms.CharField(label='repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = {'username', 'email',}

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = UserBase.objects.filter(username=username)
        
        if r.count():
            raise forms.ValidationError("Username already in use")
        
        return username


    def clean_password(self):
        cd = self.cleaned_data

        if cd['password'] != cd['validation_pass']:
            raise forms.ValidationError('PassWords not matching')
        
        return cd['validation_pass']


    def clean_email(self):
        email = self.cleaned_data['email']

        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already connected to an account")
        
        return email


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'E-Mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Password'})
        self.fields['validation_pass'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Repeat Password'})
