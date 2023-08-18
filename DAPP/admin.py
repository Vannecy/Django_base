from django.contrib import admin
from gestion.models import Player, Trading, Team, Messagerie, Profil


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_team', 'value', 'on_transfert_list', 'price')
    list_filter = ('player_team', 'on_transfert_list')

class TradingAdmin(admin.ModelAdmin):
    list_display = ('player', 'buyer', 'seller', 'proposed_value','sell_price', 'contre_proposition_price','talking_to', 'is_accepted', 'status_trading','id' )
    list_filter = ('is_accepted',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'budget')

class MessagerieAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recever', 'status','id', 'date')

class ProfilAdmin(admin.ModelAdmin):
    list_display = ('id','user_profil', 'team_profil', 'name',)



admin.site.register(Player, PlayerAdmin)
admin.site.register(Trading, TradingAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(Messagerie, MessagerieAdmin)