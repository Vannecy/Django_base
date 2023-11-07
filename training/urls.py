from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'training'


urlpatterns = [
    
    path('/<int:player_id>', views.training, name='training'),


    
]