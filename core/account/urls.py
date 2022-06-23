from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.registration, name='registration'),
    
]
