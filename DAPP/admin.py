from django.contrib import admin
from gestion.models import Player, Trading, Team, Messagerie, Profil, Formation


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'player_team', 'value', 'on_transfert_list', 'price','get_main_position_display', 'style','general','size','weight', 'date_de_naissance','position_on_the_field')
    list_filter = ('player_team', 'on_transfert_list')

class TradingAdmin(admin.ModelAdmin):
    list_display = ('player', 'buyer', 'seller', 'proposed_value','sell_price', 'contre_proposition_price','talking_to', 'is_accepted', 'status_trading','id' )
    list_filter = ('is_accepted',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'budget', 'id')

class MessagerieAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recever', 'status','id', 'date')

class ProfilAdmin(admin.ModelAdmin):
    list_display = ('id','user_profil', 'team_profil', 'name',)

class FormationAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'id')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Trading, TradingAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(Messagerie, MessagerieAdmin)
admin.site.register(Formation, FormationAdmin)
