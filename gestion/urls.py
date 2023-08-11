from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'gestion'


urlpatterns = [
    
    path('', views.gestion, name='gestion'),
    path('create_player/', views.create_player, name='create_player'),
    path('create_team/', views.create_team, name='create_team'),
    path('player_list/', views.player_list, name='player_list'),


    path('manage_trading/<int:trading_id>/', views.manage_trading, name='manage_trading'),
    path('trading_list/', views.trading_list, name='trading_list'),
    path('propose_trading/<int:player_id>/', views.propose_trading, name='propose_trading'),
    path('accept_trading/<int:trading_id>/', views.accept_trading, name='accept_trading'),


    
]