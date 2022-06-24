from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .models import UserBase

def registration(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account/dashboard')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')