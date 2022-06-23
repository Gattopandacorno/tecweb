from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser')

        return self.create_user(email, username, password, **other_fields)


    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide email address'))
        
        email   = self.normalize_email(email)
        user    = self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(_('email address'), unique=True)
    username        = models.CharField(max_length=150, unique=True)
    about           = models.TextField(_('about'), blank=True)

    country         = CountryField()
    phone_num       = models.CharField(max_length=15, blank=True)
    cap_code        = models.CharField(max_length=12, blank=True)
    address         = models.CharField(max_length=150, blank=True)
    city            = models.CharField(max_length=150, blank=True)

    is_staff        = models.BooleanField(default=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    obj             = CustomUserManager()
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username
    
