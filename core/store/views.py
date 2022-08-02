from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
import re

from .models import Category, Product
from .forms import AddProductForm, AddCategoryForm


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

    
def create_product(request):    
    if request.method == 'POST':
        prodform = AddProductForm(request.POST)
        
        if prodform.is_valid():
            slug = re.sub('\W', '', prodform.cleaned_data['title'].lower())
            Product.objects.create(slug=slug, **prodform.cleaned_data)
            
            return redirect('/')
    else:
        prodform = AddProductForm()
  
    return render(request, 'store/products/createprod.html', { 'form': prodform } )


def create_category(request):
    if request.method == 'POST':
        catform = AddCategoryForm(request.POST)
        
        if catform.is_valid():
            category = catform.save(commit=False)
            category.name = catform.cleaned_data['name']
            category.slug = re.sub('\W', '', category.name.lower())

            category.save()
            return redirect('/')
    else:
        catform = AddCategoryForm()
  
    return render(request, 'store/products/createcat.html', { 'form': catform } )