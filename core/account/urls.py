from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/', views.registration, name='registration'),
    
]
