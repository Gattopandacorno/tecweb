from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from orders.views import history 

def registration(request):
    """  Registra l'utente, se è gia loggato allora verrà redirezionato alla home page. """
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])

            user.country = registerform.cleaned_data['country']
            user.city    = registerform.cleaned_data['city']
            user.address = registerform.cleaned_data['address']
            user.phone_num = registerform.cleaned_data['phone_num']
            user.cap_code  = registerform.cleaned_data['cap_code']
            
            user.is_active = True
            user.save()
            login(request, user)
            
            return redirect('/')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )

@login_required
def profile(request):
    """ Ritorna la pagina col profilo dell'utente. Se non è loggato chiede di fare il login. """

    return render(request, 'account/profile.html')

@login_required
def edit_details(request):
    """ Possono essere cambiati alcuni dei dettagli dell'utente. Username e mail no. """

    if request.method == 'POST':
        userform = UserEditForm(instance=request.user, data=request.POST)

        if userform.is_valid():
            userform.save()
    else:
        userform = UserEditForm(instance=request.user)
    
    return render(request, 'account/edit_details.html', {'form': userform})
    
@login_required
def delete(request):
    """ Cancella l'utente, per motivi di sicurezza possono solo gli utenti non staff. """
    
    if not request.user.is_staff:
        user = UserBase.objects.get(username=request.user)
        user.is_active = False  # ACTIVATE TO DELETE THE USER 
        user.save()
        logout(request)
    
    return redirect('account:confirmation')

@login_required
def user_history(request):
    """ Ritorna la lista degli ordini passati di un utente. """
   
    orders = history(request)
    ctx    = {'orders': orders}

    return render(request, 'account/user_history.html', context=ctx)

@login_required
def add_seller(request):
    """ Viene aggiunto un nuovo membro di venditori. Solo un membro dello staff potrà farlo. """
    
    if not request.user.is_staff:
        return redirect('/')

    if request.user.is_staff and request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])

            user.country = registerform.cleaned_data['country']
            user.city    = registerform.cleaned_data['city']
            user.address = registerform.cleaned_data['address']
            user.phone_num = registerform.cleaned_data['phone_num']
            user.cap_code  = registerform.cleaned_data['cap_code']
            
            user.is_active = True
            user.is_seller = True
            user.save()
            logout(request)
            
            return redirect('/account/login/')
    else:
        registerform = RegistrationForm()
  
    return render(request, 'account/register.html', { 'form': registerform } )