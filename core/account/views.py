from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, UserEditForm
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
            return redirect('/')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )


@login_required
def profile(request):
    return render(request, 'account/profile.html')

@login_required
def edit_details(request):
    if request.method == 'POST':
        userform = UserEditForm(instance=request.user, data=request.POST)
        if userform.is_valid():
            userform.save()
    else:
        userform = UserEditForm(instance=request.user)
    
    return render(request, 'account/edit_details.html', {'userform': userform})
    
@login_required
def delete(request):
    user = UserBase.objects.get(username=request.user)
    #user.is_active = False
    user.save()
    logout(request)
    return redirect('account:confirmation')
