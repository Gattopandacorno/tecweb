
from django import forms
from django.contrib.auth.forms import AuthenticationForm


from .models import UserBase

class RegistrationForm(forms.ModelForm):
    """ Usata per la registrazione di un utente nuovo (seller o normale utente). """

    username        = forms.CharField(label='Enter username', min_length=4, max_length=50, help_text='Required')
    email           = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'You must provide an email.'})
    validation_pass = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    password        = forms.CharField(label='Password', widget=forms.PasswordInput)

    country         = forms.CharField(label='Country')
    city            = forms.CharField(label='City name', max_length=150)
    address         = forms.CharField(label='Address' ,max_length=150)
    phone_num       = forms.CharField(label='Phone number', min_length=11, max_length=11)
    cap_code        = forms.CharField(label='Postal code', min_length=5, max_length=5)
    

    class Meta:
        model  = UserBase
        fields = {'username', 'email', 'country', 'city', 'address', 'phone_num', 'cap_code'}

    def clean_username(self):
        """ Cleaned data, ritorna se uno username è gia usato o meno. """

        username = self.cleaned_data['username'].lower()
        r = UserBase.objects.filter(username=username)
        
        if r.count():
            raise forms.ValidationError("Username already in use")
        
        return username


    def clean_email(self):
        """ Ritorna se la mail è gia in uso o meno. """

        email = self.cleaned_data['email']

        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already connected to an account")
        
        return email

        
    def clean_password(self):
        """ Verifica che le due password inserite durante la registrazione siano uguali. """

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

        self.fields['country'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Country'})
        self.fields['city'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'City name'})
        self.fields['address'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Address'})
        self.fields['phone_num'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Phone number'})
        self.fields['cap_code'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Postal code'})



class UserLoginForm(AuthenticationForm):
    """ Usato per il login di un utente gia registrato, vengono chieste solo mail e password. """

    username = forms.CharField(widget=forms.TextInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id':'login-username'}))
    
    password = forms.CharField(widget=forms.PasswordInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'Password', 'id': 'login-pwd'}))


class UserEditForm(forms.ModelForm):
    """ Usato per cambiare alcuni parametri del profilo, username e mail non possono essere cambiati. """
    
    email     = forms.EmailField(label='Account email cannot be changes', max_length=200, widget=forms.TextInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    username  = forms.CharField(label='Username', min_length=4, max_length=50, widget=forms.TextInput(
                    attrs={'class': 'form-control mb-3', 'placeholder': 'username', 'id': 'form-firstname', 'readonly': 'readonly'}))
    
    country   = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Country'}))
    city      = forms.CharField(label='City name', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'City name'}))
    address   = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Address'}))
    phone_num = forms.IntegerField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Phone number'}))
    cap_code  = forms.IntegerField(label='Postal code', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Postal code'}))

    
    class Meta:
        model  = UserBase
        fields = ('email', 'username', 'country', 'city', 'address', 'phone_num', 'cap_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required    = True
       
