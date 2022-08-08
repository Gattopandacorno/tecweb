from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """ Custom user creator. """

    def create_superuser(self, email, username, password, **other_fields):
        """ Creates the superuser. Note that the superuser is different from the seller user."""

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser')

        return self.create_user(email, username, password, **other_fields)


    def create_user(self, email, username, password, **other_fields):
        """ Creates a new user. The user will be a 'normal buyer'. """

        if not email: # If the mail is not provided
            raise ValueError(_('You must provide email address'))
        
        email   = self.normalize_email(email)
        user    = self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    """ The common fields of all the users. Seller, Admin and common-buyer. """

    email           = models.EmailField(_('email address'), unique=True)
    username        = models.CharField(max_length=150, unique=True)
    about           = models.TextField(_('about'), blank=True)

    country         = models.CharField(max_length=150 ,blank=True)
    phone_num       = models.CharField(max_length=11, blank=True)
    cap_code        = models.CharField(max_length=5, blank=True)
    address         = models.CharField(max_length=150, blank=True)
    city            = models.CharField(max_length=150, blank=True)

    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    
    # This fields is True when the admin creates a new seller account
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

    def is_normal(self):
        if self.is_staff or self.is_seller:
            return False
        return True
    