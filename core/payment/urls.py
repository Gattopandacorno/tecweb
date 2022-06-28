from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'payment'

urlpatterns = [
    path('confirm_pay/', TemplateView.as_view(template_name='payment/confirm_pay.html'), name='confirm_pay'),
    path('', views.CartView, name='cartview'), 
]