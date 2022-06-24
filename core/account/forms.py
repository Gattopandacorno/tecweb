
from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import UserBase

class RegistrationForm(forms.ModelForm):
    username        = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email           = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'You must provide an email.'})
    validation_pass = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    password        = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = {'username', 'email',}

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = UserBase.objects.filter(username=username)
        
        if r.count():
            raise forms.ValidationError("Username already in use")
        
        return username


    def clean_email(self):
        email = self.cleaned_data['email']

        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already connected to an account")
        
        return email

        
    def clean_password(self):
        cd = self.cleaned_data

        if cd['password'] != cd['validation_pass']:
            raise forms.ValidationError('Passwords not matching')
        
        return cd['validation_pass']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'E-Mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Password'})
        self.fields['validation_pass'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Repeat Password'})



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id':'login-username'}))
    
    password = forms.CharField(widget=forms.PasswordInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'Password', 'id': 'login-pwd'}))