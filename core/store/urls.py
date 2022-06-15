from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='product_all'), 
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:slug>/', views.category_list, name='category_list'),
]