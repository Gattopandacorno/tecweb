from email.policy import default
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories' 

    def get_absolute_url(self):
       return reverse_lazy('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    author      = models.CharField(max_length=255, default='Not found')
    description = models.TextField(blank=True)
    available   = models.IntegerField(default=1)
    image       = models.ImageField(upload_to='images/', default='images/default.png') # storing the link to the db
    slug        = models.SlugField(max_length=255)
    price       = models.DecimalField(max_digits=4, decimal_places=2, default=4.50)
    in_stock    = models.BooleanField(default=True)
    is_active   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True) # TODO: remove
    updated     = models.DateTimeField(auto_now=True) # TODO: remove
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)

    class Meta:
        ordering = ('-created',)

    def get_qty(self):
        return range(self.available)

    def get_absolute_url(self):
        return reverse_lazy('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title



RATE_CHOICES = [(1, '1 - Trash'), (2, '2 - Bad'), (3, '3 - Ok'), (4, '4 - Nice'), (5, '5 - Perfect')]

class Review(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    date     = models.DateTimeField(auto_now_add=True)
    text     = models.TextField(blank=True)
    rate     = models.PositiveIntegerField(choices=RATE_CHOICES, blank=True)
    likes    = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username