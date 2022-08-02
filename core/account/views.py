from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from orders.views import history 

def registration(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])

            user.country = registerform.cleaned_data['country']
            user.city = registerform.cleaned_data['city']
            user.address = registerform.cleaned_data['address']
            user.phone_num = registerform.cleaned_data['phone_num']
            user.cap_code = registerform.cleaned_data['cap_code']
            
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
    #user.is_active = False  #TODO:ACTIVATE TO DELETE THE USER 
    user.save()
    logout(request)
    return redirect('account:confirmation')

@login_required
def user_history(request):
    orders = history(request)
    ctx = {'orders': orders}

    return render(request, 'account/user_history.html', context=ctx)

@login_required
def add_seller(request):
    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            usr = registerform.save(commit=False)
            usr.email = registerform.cleaned_data['email']
            usr.set_password(registerform.cleaned_data['password'])

            usr.country = registerform.cleaned_data['country']
            usr.city = registerform.cleaned_data['city']
            usr.address = registerform.cleaned_data['address']
            usr.phone_num = registerform.cleaned_data['phone_num']
            usr.cap_code = registerform.cleaned_data['cap_code']
            
            usr.is_active = True
            usr.is_seller = True
            usr.save()
            return redirect('/')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )
