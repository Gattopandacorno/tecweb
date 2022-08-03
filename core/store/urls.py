from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('create_product/', views.create_product ,name="create_product"),
    path('create_category/', views.create_category ,name="create_category"),
    path('<slug:slug>/', views.product_detail, name='product_detail'),  
    path('shop/<slug:slug>/', views.category_list, name='category_list'),
    path('rating/create_review/<slug:slug>/', views.create_review, name="create_review")
]