from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Category, Product
from .forms import RateForm


# Create your views here.

def categories(request):
    return { 'categories': Category.objects.all() }

def product_all(request): 
    products = Product.objects.all()
    ctx = { 'products': products }
    return render(request, template_name='store/home.html', context=ctx)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    ctx = { 'product': product }
    return render(request, 'store/products/single.html', context=ctx)

def category_list(request,slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    ctx = { 'category': category, 
            'products': products }
    return render(request, 'store/products/category.html', context=ctx)
