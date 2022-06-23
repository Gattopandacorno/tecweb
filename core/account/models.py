from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager, PermissionsMixin)
from django_countries.fields import CountryField

class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    about = models.TextField(_('about'), blank=True)

    country = CountryField()