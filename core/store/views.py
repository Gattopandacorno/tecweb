from datetime import datetime
from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import re

from account.models import UserBase
from .forms import AddProductForm, AddCategoryForm, AddReviewForm
from .models import Category, Product, Review


def categories(request):
    """ Returns all the categories created that are in the database. """

    return { 'categories': Category.objects.all() }

def product_all(request): 
    """ Returns all the products created that are in the database.
        This will be displayed in the home page.
    """

    products = Product.objects.all()
    ctx = { 'products': products }
    return render(request, template_name='store/home.html', context=ctx)

def all_reviews(request, slug):
    """ Returns all the reviews for a certain product. """

    prod = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product=prod)
    
    # Used to know if the user has already done a review for this product
    if request.user.is_authenticated:
        usr = Review.objects.filter(product=prod, user=request.user).exists()
    else:
        usr = False

    ctx = {'reviews': reviews, 'usr': usr}
    return ctx

def product_detail(request, slug):
    """ Returns the datail of a product. It will be showned reviews, price, quantity available, title,... """

    product = get_object_or_404(Product, slug=slug)
    ctx = all_reviews(request=request,slug=slug)

    ctx.update({ 'product': product })
    return render(request, 'store/products/single.html', context=ctx)

def category_list(request,slug):
    """ Returns the list of the products that are of the selected category. """

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    ctx = { 'category': category, 'products': products }
    return render(request, 'store/products/category.html', context=ctx)

@login_required
def create_product(request):
    """ Create a new entry of a product. Only a staff or a seller member can perform this action. """  

    if not (request.user.is_staff or request.user.is_seller):
        return redirect('/')

    if request.method == 'POST':
        prodform = AddProductForm(request.POST)
        
        if prodform.is_valid():
            slug = re.sub('\W', '', prodform.cleaned_data['title'].lower())
            Product.objects.create(slug=slug, **prodform.cleaned_data)
            
            return redirect('/')
    else:
        prodform = AddProductForm()
  
    return render(request, 'store/products/createprod.html', { 'form': prodform } )

@login_required
def create_category(request):
    """ Create a new entry of a category. Only a staff or a seller member can perform this action. """

    if not (request.user.is_staff or request.user.is_seller):
        return redirect('/')

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

@login_required
def create_review(request, slug):
    """ Creates a review. Only a normal logged in user can perform this action. """
        
    if request.user.is_staff or request.user.is_seller:
       return redirect('/')

    if request.method == 'POST':
        rateform = AddReviewForm(request.POST)
        
        if rateform.is_valid():
            product = Product.objects.get(slug=slug)
            usr = UserBase.objects.get(username=request.user)
            Review.objects.create(product=product, user=usr, date=datetime.now() ,**rateform.cleaned_data)
            
            return redirect('/')
    else:
        rateform = AddReviewForm()
  
    return render(request, 'store/rating/home.html', { 'form': rateform, 'slug': slug } )

def search(request):
    word = request.GET.get('word')
    
    prods = Product.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")
    cats = Category.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    for cat in cats:
        prods |= Product.objects.filter(category=cat)

    prods |= Product.objects.filter(author__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")
    prods |= Product.objects.filter(description__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    ctx = { 'category': "Searched: "+word, 'products': prods }
    return render(request, 'store/products/category.html', context=ctx)