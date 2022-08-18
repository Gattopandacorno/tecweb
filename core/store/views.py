from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
import re

from account.models import UserBase
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, AddReviewForm
from .models import Category, Product, Review


def categories(request):
    """ Ritorna tutte le categorie nel database. """

    return { 'categories': Category.objects.all() }

def product_all(request): 
    """ 
        Ritorna tutti i prodotti nel database.
        Serve per la home page.
    """

    products = Product.objects.all()
    ctx = { 'products': products, 'recommend': recommend(request) }
    return render(request, template_name='store/home.html', context=ctx)

def all_reviews(request, slug):
    """ Ritorna le review per un certo prodotto """

    prod = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product=prod)
    
    
    ctx = {'reviews': reviews}
    return ctx

def product_detail(request, slug):
    """ 
        Ritorna in dettaglio un singolo prodotto.
        Oltre agli attributi di Product vengono passate le review di quel prodotto. 
    """

    product = get_object_or_404(Product, slug=slug)
    ctx = all_reviews(request=request,slug=slug)

    ctx.update({ 'product': product })
    return render(request, 'store/products/single.html', context=ctx)

def category_list(request,slug):
    """ Ritorna la lista di prodotti appartenenti a quella categoria. """

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    ctx = { 'category': category, 'products': products }
    return render(request, 'store/products/category.html', context=ctx)

@login_required
def create_product(request):
    """ 
        Crea un nuovo prodotto.
        Se invece il titolo è di un prodotto gia esistente allora ne cambia i dati.
        Solo un membro dello staff o dei venditori(seller) possono farlo.
        Se l'utente non appartiene ad uno dei due tipi di membro viene mandato alla home page.
    """  

    if not (request.user.is_staff or request.user.is_seller):
        return redirect('/')

    if request.method == 'POST':
        prodform = AddProductForm(request.POST)
        
        if prodform.is_valid():
            slug = re.sub('\W', '', prodform.cleaned_data['title'].lower())
            
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
        Crea una nuova categoria.
        Se esiste gia una categoria con quel nome allora redirecta l'utente alla home page.
        Come per create_product, solo un membro dello staff o un seller può creare nuove categorie.
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
        Crea una nuova revisione.
        Solo un utente normalmente loggato può lasciare una review.
        Se un membro dello staff o un seller provano a farne una allora verranno redirezionati nella home page.
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
        Viene fatta una ricerca della parola data in titolo, autore e descrizione per ogni prodotto.
        Viene inoltre cercato se la parola è all'interno del nome della categoria.
        Se non viene passato nulla allora si viene redirezionati nella homepage.
    """
    
    word = request.GET.get('word')

    if not word :
        return redirect('/')

    prods = Product.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")
    cats  = Category.objects.filter(slug__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    for cat in cats:
        prods |= Product.objects.filter(category=cat)

    prods |= Product.objects.filter(author__regex=r"(\w|\W)*( )*" + str(word) + "(\w|\W)*( )*")
    prods |= Product.objects.filter(description__regex=r"(\w|\W)*" + str(word) + "(\w|\W)*")

    ctx = { 'category': "Searched: " + word, 'products': prods }
    return render(request, 'store/products/category.html', context=ctx)

@login_required
def recommend(request):
    """
        La raccomandazione viene fatta vedere solo da utenti loggati.
        Per prima cosa vengono cercati tutti i prodotti con una media di piu di 2 stelle.
        Poi viene fatta una ricerca di tutti i prodotti comprati per capirne la categoria preferita
        e passare quindi i prodotti con quella categoria non ancora comprati.
    """

    products = list(Product.objects.filter(in_stock=True))
    prods = set()

    for product in products:
        if Review.objects.filter(product=product).exists():
            if Review.objects.filter(product=product).aggregate(Avg('rate'))['rate__avg'] > 2:
                prods.add(product)

    for order in Order.objects.filter(user=request.user):

        for oi in OrderItem.objects.filter(order=order) :
            p = Product.objects.get(title=oi.product)
                
            for product in Product.objects.filter(category=p.category):
                prods.add(product)

        for oi in OrderItem.objects.filter(order=order) :
            prods.discard(oi.product)

    prods.discard(None)
    return { 'products': list(prods)[:6] }