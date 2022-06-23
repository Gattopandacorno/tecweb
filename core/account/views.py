from django.shortcuts import render, redirect

from .froms import RegistrationForm

def registration(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password'])
            user.save()
    else:
        registerform = RegistrationForm()
        ctx = { 'form': registerform }
        return render(request, 'account/register.html', context=ctx )