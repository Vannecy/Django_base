from django.shortcuts import render
from django.http import JsonResponse
from gestion.models import Player, Team
import json
from django.urls import reverse
from django.http import HttpResponse

def training(request, player_id):
    
    # Récupérer les détails du joueur en fonction de l'ID du joueur
    player = Player.objects.get(id=player_id)
    
    if request.method == 'POST':
        #if player.can_train():
        data = json.loads(request.body)
        skill_name = data['skill_name']
        player.update_skill_progress(skill_name)
        player.update_last_trained()
        player.general = int((player.attaque + player.defense + player.vitesse + player.passe + player.mental + player.interception + player.physique) / 7)
        player.save()
        general = player.general
        
        player.save()
        
        return JsonResponse({'new_value': getattr(player, f'{skill_name.lower()}_progress'), f'player_{skill_name.lower()}': getattr(player, skill_name.lower()), "date":player.last_trained.strftime("%Y-%m-%d %H:%M"), "general":general})

    # Passer le joueur en tant que contexte lors du rendu du modèle
    return render(request, 'training.html',  {'player': player})

