from re import template
from django.urls import path
from django.contrib.auth import views as auth_views


from .forms import UserLoginForm
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', form_class=UserLoginForm), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/', views.registration, name='registration'),
    
]
