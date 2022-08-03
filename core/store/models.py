from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    """ Represents the category of a product. Exemples of anime/manga's category can be found
        on wikipedia.  
    """

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories' 

    def get_absolute_url(self):
       return reverse_lazy('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Represents a product. A product can only be a book(manga) or a cartoon(anime). """

    category    = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    author      = models.CharField(max_length=255, default='Not found')
    description = models.TextField(blank=True)
    available   = models.IntegerField(default=1)
    image       = models.ImageField(upload_to='images/', default='images/default.png') # stores the link to the db
    slug        = models.SlugField(max_length=255)
    price       = models.DecimalField(max_digits=4, decimal_places=2, default=4.50)
    in_stock    = models.BooleanField(default=True)
    is_active   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True) 
    updated     = models.DateTimeField(auto_now=True) 

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
    """ Represents the single review of a product. """
    
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    date     = models.DateTimeField(auto_now_add=True)
    text     = models.TextField(blank=True)
    rate     = models.IntegerField(choices=RATE_CHOICES)
   
   
    def __str__(self):
        return self.user.username