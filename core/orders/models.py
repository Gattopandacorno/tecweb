from django.conf import settings
from django.db import models

from store.models import Product

class Order(models.Model):
    """ 
        Represents an order. An order is done by doing the checkout('paying') of the cart. 
        After the order is done, it can be seen in the profile sectio called 'order history'.
    """

    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tot_paid        = models.DecimalField(max_digits=5, decimal_places=2)
    order_key       = models.CharField(max_length=200)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    billing_status  = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

 

class OrderItem(models.Model):
    """ Represents the single ordered items in a certain order. """
    
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price   = models.DecimalField(max_digits=5, decimal_places=2)
    qty     = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)