from random import choices
from secrets import choice
from django import forms

from .models import Review, RATE_CHOICES

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())
    rate = forms.CharField(widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = { 'text', 'rate'}