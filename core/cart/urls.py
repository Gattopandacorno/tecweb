from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('update/', views.cart_update, name='cart_update'),
    path('del/', views.cart_del, name='cart_del'),
    path('add/', views.cart_add, name='cart_add'),
    path('', views.cart_summary, name='cart_summary'),
    
]
