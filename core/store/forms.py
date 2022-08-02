from email.mime import image
from random import choices
from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Category, Product

class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(label='Enter name', help_text='required', required=True)

    class Meta:
        model = Category
        fields = {'name'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Name'})




class AddProductForm(forms.ModelForm):
    category     = forms.ModelChoiceField(queryset=Category.objects.all())
    title        = forms.CharField(label='Enter title', max_length=255, help_text='Required')
    author       = forms.CharField(initial="Not found", max_length=255, required=False)
    description  = forms.Textarea()
    image        = forms.ImageField(initial="images/default.png")
    available    = forms.IntegerField(initial=1)
    price        = forms.DecimalField(max_digits=4, decimal_places=2, initial=4.50)

    
    

    class Meta:
        model = Product
        fields = {'category', 'title', 'author', 'description', 'image', 'available', 'price'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Category'})
        self.fields['title'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Title'})
        self.fields['author'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Author'})
        self.fields['available'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Available'})
        self.fields['price'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Price'})
