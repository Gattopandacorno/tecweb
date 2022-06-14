from django.shortcuts import render, get_object_or_404

from .models import Category, Product

# Create your views here.

def categories(request):
    return { 'categories': Category.objects.all() }

def all_products(request): 
    products = Product.objects.all()
    ctx = { 'products': products }
    return render(request, template_name='store/home.html', context=ctx)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    ctx = { 'product': product }
    return render(request, 'store/products/detail.html', context=ctx)
