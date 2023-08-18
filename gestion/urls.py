from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'gestion'


urlpatterns = [
    
    path('', views.home, name='home'),
    path('profil/', views.profil, name='profil'),


    path('create_player/', views.create_player, name='create_player'),
    path('create_team/', views.create_team, name='create_team'),
    path('player_list/', views.player_list, name='player_list'),
    path('team_list/', views.team_list, name='team_list'),
    path('team_detail/<int:team_id>/', views.team_detail, name='team_detail'),
    path('player_detail/<int:player_id>/', views.player_detail, name='player_detail'),


    path('manage_trading/<int:trading_id>/', views.manage_trading, name='manage_trading'),
    path('trading_list/', views.trading_list, name='trading_list'),
    path('propose_trading/<int:player_id>/', views.propose_trading, name='propose_trading'),
    path('accept_trading/<int:trading_id>/', views.accept_trading, name='accept_trading'),

    path('messagerie/', views.messagerie, name='messagerie'),
    path('create_message/', views.create_message, name='create_message'),
    path('message_detail/<int:messagerie_id>/', views.message_detail, name='message_detail'),
    path('response_message/<int:receiver_id>/<int:trading_number>/<int:message_id>/', views.response_message, name='response_message'),
    
]