from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authentification'


urlpatterns = [

    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.user_login, name='user_login'),

    path('logout/', views.user_logout, name='user_logout'),

    
]
