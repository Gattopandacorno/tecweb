from django import forms

from .models import Category, Product, Review, RATE_CHOICES


class AddCategoryForm(forms.ModelForm):
    """ Reppresenta i campi da riempire per una Category """

    name = forms.CharField(label='Enter name', help_text='required', required=True)

    class Meta:
        model  = Category
        fields = {'name'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Name'})



class AddProductForm(forms.ModelForm):
    """ Rappresenta i campi da riempire per un Product. """

    category    = forms.ModelChoiceField(queryset=Category.objects.all())
    title       = forms.CharField(label='Enter title', max_length=255, help_text='Required')
    author      = forms.CharField(initial="Not found", max_length=255, required=False)
    description = forms.Textarea()
    image       = forms.ImageField(initial="images/default.png")
    available   = forms.IntegerField(initial=1)
    price       = forms.DecimalField(max_digits=4, decimal_places=2, initial=4.50)
    
    

    class Meta:
        model  = Product
        fields = {'category', 'title', 'author', 'description', 'image', 'available', 'price'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Category'})
        self.fields['title'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Title'})
        self.fields['author'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Author'})
        self.fields['available'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Available'})
        self.fields['price'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Price'})



class AddReviewForm(forms.ModelForm):
    """ Rappresenta come compilare i campi per una Review. """

    text = forms.Textarea()
    rate = forms.ChoiceField(choices=RATE_CHOICES, required=True)

    class Meta:
        model  = Review
        fields = {'text', 'rate'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Text'})
        self.fields['rate'].widget.attrs.update({ 'class': 'form-control form-control-lg', 'placeholder': 'Rate'})