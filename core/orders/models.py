from django.conf import settings
from django.db import models

from store.models import Product

class Order(models.Model):
    """ 
        Rappresenta un ordine, viene creato dopo un pagamento.
        Dopo essere creato si puo' vedere negli ordini passati nella sezione del profilo 'order history'.
    """

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tot_paid       = models.DecimalField(max_digits=5, decimal_places=2)
    order_key      = models.CharField(max_length=200)
    created        = models.DateTimeField(auto_now_add=True)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

 

class OrderItem(models.Model):
    """ Rappresenta un certo prodotto preso per un ordine. """
    
    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price   = models.DecimalField(max_digits=5, decimal_places=2)
    qty     = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)