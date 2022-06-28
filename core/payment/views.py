from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.

@login_required
def CartView(request):
    return render(request, 'payment/home.html')


