from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from store.views import all_reviews
from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from orders.views import history 
from orders.models import OrderItem
from store.models import Product, Review

def registration(request):
    """ Used to register a user. 
        If it is already registered it will only be redirected in the home page.
        """
    
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
    """ Redirects the user in the profile action. Every user can do a set of actions that depends on the 
        type of the account.
        Only those who are logged can be allowed in this section.
    """

    return render(request, 'account/profile.html')

@login_required
def edit_details(request):
    """ Redirects the user in the account settings. In this section a logged user can edit some details like
        the country name or the cap code.
        Note that username and email cannot be edited.
    """

    if request.method == 'POST':
        userform = UserEditForm(instance=request.user, data=request.POST)

        if userform.is_valid():
            userform.save()
    else:
        userform = UserEditForm(instance=request.user)
    
    return render(request, 'account/edit_details.html', {'form': userform})
    
@login_required
def delete(request):
    """ Use to delete a user account. This method fakes the deletion but 72 line can be de-commented. """
    
    if not request.user.is_staff:
        user = UserBase.objects.get(username=request.user)
        #user.is_active = False  #TODO: ACTIVATE TO DELETE THE USER 
        user.save()
        logout(request)
    
    return redirect('account:confirmation')

@login_required
def user_history(request):
    """ Returns a list of the user's orders to display in the history section. """
   
    orders = history(request)
    ctx = {'orders': orders}

    return render(request, 'account/user_history.html', context=ctx)

@login_required
def add_seller(request):
    """ This section is admin only, this is due to security reasons. This method register a new  seller account.
        To do so sets user.is_seller to True.
    """
    
    if request.user.is_staff and request.method == 'POST':
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
            user.is_seller = True
            user.save()
            return redirect('/')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )