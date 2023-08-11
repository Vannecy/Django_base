from django.contrib import admin
from gestion.models import Player, Trading, Team


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_team', 'value', 'on_transfert_list')
    list_filter = ('player_team', 'on_transfert_list')

class TradingAdmin(admin.ModelAdmin):
    list_display = ('player', 'buyer', 'seller', 'proposed_value', 'is_accepted')
    list_filter = ('is_accepted',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Trading, TradingAdmin)
admin.site.register(Team, TeamAdmin)