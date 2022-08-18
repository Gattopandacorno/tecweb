from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """ Creazione custom per l'utente. """

    def create_superuser(self, email, username, password, **other_fields):
        """ Crea un superuser."""

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser')

        return self.create_user(email, username, password, **other_fields)


    def create_user(self, email, username, password, **other_fields):
        """ Crea un nuovo utente. """

        if not email: # Se non viene data la mail
            raise ValueError(_('You must provide email address'))
        
        email   = self.normalize_email(email)
        user    = self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    """ Rappresenta qualsiasi utente: 'compratore', seller e superuser. """

    email           = models.EmailField(_('email address'), unique=True)
    username        = models.CharField(max_length=150, unique=True)

    country         = models.CharField(max_length=150 ,blank=True)
    phone_num       = models.CharField(max_length=11, blank=True)
    cap_code        = models.CharField(max_length=5, blank=True)
    address         = models.CharField(max_length=150, blank=True)
    city            = models.CharField(max_length=150, blank=True)

    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    
    # True quando viene creato un nuovo venditore dal superuser
    is_seller       = models.BooleanField(default=False) 
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects         = CustomUserManager()
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'country', 'city', 'address', 'phone_num', 'cap_code']


    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username