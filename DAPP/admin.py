from django.contrib import admin
from gestion.models import Player, Trading, Team, Messagerie


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_team', 'value', 'on_transfert_list')
    list_filter = ('player_team', 'on_transfert_list')

class TradingAdmin(admin.ModelAdmin):
    list_display = ('player', 'buyer', 'seller', 'proposed_value', 'is_accepted', 'status_trading')
    list_filter = ('is_accepted',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

class MessagerieAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recever')



admin.site.register(Player, PlayerAdmin)
admin.site.register(Trading, TradingAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Messagerie, MessagerieAdmin)