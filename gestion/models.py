from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)  # Ajoutez ce champ pour la valeur du joueur
    on_transfert_list = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# Modèles (models.py)
class Trading(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_sent')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_received')
    proposed_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_accepted = models.BooleanField(default=False)


