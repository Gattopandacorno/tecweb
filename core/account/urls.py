from re import template
from django.urls import path
from django.contrib.auth import views as auth_views


from .forms import UserLoginForm
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/delete/', views.delete, name='delete'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', form_class=UserLoginForm), name='login'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    
]
