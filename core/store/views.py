from datetime import datetime
from urllib import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
import re

from account.models import UserBase
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, AddReviewForm
from .models import Category, Product, Review


def categories(request):
    """ Returns all the categories created that are in the database. """

    return { 'categories': Category.objects.all() }

def product_all(request): 
    """ 
        Returns all the products created that are in the database.
        This will be displayed in the home page.
    """

    products = Product.objects.all()
    ctx = { 'products': products, 'recommend': recommend(request) }
    return render(request, template_name='store/home.html', context=ctx)

def all_reviews(request, slug):
    """ Returns all the reviews for a certain product. """

    prod = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product=prod)
    
    
    ctx = {'reviews': reviews}
    return ctx

def product_detail(request, slug):
    """ 
        Returns the datail of a product. 
        It will be showned reviews, price, quantity available, title,... 
    """

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
    """ 
        Create a new entry of a product.  
        If the product already exists then it will be edited instead.
        Only a staff or a seller member can perform this action. 
    """  

    if not (request.user.is_staff or request.user.is_seller):
        return redirect('/')

    if request.method == 'POST':
        prodform = AddProductForm(request.POST)
        
        if prodform.is_valid():
            slug = re.sub('\W', '', prodform.cleaned_data['title'].lower())
            
            print(prodform.cleaned_data)

            if not Product.objects.filter(slug=slug).exists():
                Product.objects.create(slug=slug, **prodform.cleaned_data)

            else:
                Product.objects.filter(slug=slug).update(**prodform.cleaned_data)

            if prodform.cleaned_data['available'] > 0:
                Product.objects.filter(slug=slug).update(in_stock=True)
            else:
                Product.objects.filter(slug=slug).update(in_stock=False)


                        
            return redirect('/')
    else:
        prodform = AddProductForm()
  
    return render(request, 'store/products/createprod.html', { 'form': prodform } )

@login_required
def create_category(request):
    """ 
        Create a new entry of a category. 
        If the category already exists it redirects the user in the homepage.
        Only a staff or a seller member can perform this action. 
    """

    if not (request.user.is_staff or request.user.is_seller):
        return redirect('/')

    if request.method == 'POST':
        catform = AddCategoryForm(request.POST)
        
        if catform.is_valid():
            name = catform.cleaned_data['name']
            slug = re.sub('\W', '', name.lower())
            
            if not Category.objects.filter(slug=slug).exists():
                Category.objects.create(slug=slug, name=name)
            
            return redirect('/')
    else:
        catform = AddCategoryForm()
  
    return render(request, 'store/products/createcat.html', { 'form': catform } )

@login_required
def create_review(request, slug):
    """ 
        Creates a review. 
        Only a normal logged in user can perform this action. 
        If a staff or seller member try to do a review it will be redirected in the homepage.
    """
        
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
    """
        Given the word it performs a search in title, author, description of all the products
        and in the name of all the category.
        If nothing is searched it will redirects in the homepage.
    """
    
    word = request.GET.get('word')

    if not word :
        return redirect('/')

    prods = Product.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")
    cats = Category.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    for cat in cats:
        prods |= Product.objects.filter(category=cat)

    prods |= Product.objects.filter(author__regex=r"(\w|\W)*( )*" + str(word) + "(\w|\W)*( )*")
    prods |= Product.objects.filter(description__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    ctx = { 'category': "Searched: "+word, 'products': prods }
    return render(request, 'store/products/category.html', context=ctx)

def recommend(request):
    """
        The displayed recommendation in the homepage of a one logged user.
        First it searches all the products with more than 2 stars (avg).
        Secondly it search category's products bought by the user to recommend manga not bought 
        for the same category.
    """

    products = list(Product.objects.filter(in_stock=True))
    prods = set()

    for product in products:
        if Review.objects.filter(product=product).exists():
            if Review.objects.filter(product=product).aggregate(Avg('rate'))['rate__avg'] > 2:
                prods.add(product)

    if request.user.is_authenticated :
        for order in Order.objects.filter(user=request.user):

            for oi in OrderItem.objects.filter(order=order) :
                p = Product.objects.get(title=oi.product)
                
                for product in Product.objects.filter(category=p.category):
                    prods.add(product)

            for oi in OrderItem.objects.filter(order=order) :
                    prods.discard(oi.product)

    prods.discard(None)
    return { 'products': list(prods)[:6] }