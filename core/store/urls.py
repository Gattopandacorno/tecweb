from django.urls import path, include


from .views import product_all, category_list, product_detail, create_product, create_category

app_name = 'store'

urlpatterns = [
    path('',product_all, name='product_all'),
    path('create_product/', create_product ,name="create_product"),
    path('create_category/', create_category ,name="create_category"),
    path('<slug:slug>/', product_detail, name='product_detail'),  
    path('shop/<slug:slug>/', category_list, name='category_list'),
]