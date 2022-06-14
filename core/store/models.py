from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'categorie'

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by  = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE,) # TODO: remove
    title       = models.CharField(max_length=255)
    author      = models.CharField(max_length=255, default='Not found')
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='images/') # storing the link to the db
    slug        = models.SlugField(max_length=255)
    price       = models.DecimalField(max_digits=4, decimal_places=2, default=4.50)
    in_stock    = models.BooleanField(default=True)
    is_active   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True) # TODO: remove
    updated     = models.DateTimeField(auto_now=True) # TODO: remove

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

