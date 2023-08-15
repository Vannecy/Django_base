from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

# Modèles (models.py)
class Trading(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('proposed', 'Proposed'),
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_sent')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_received')
    proposed_value = models.DecimalField(max_digits=10, decimal_places=2,) #valeur proposer par acheteur
    sell_price = models.DecimalField(max_digits=10, decimal_places=2,default=None,null=True) #prix de vente
    contre_proposition_price = models.DecimalField(max_digits=10, decimal_places=2,default=None,null=True)
    is_accepted = models.BooleanField(default=False)
    status_trading = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"Trading {self.id}"


class Messagerie(models.Model):
    STATUS_CHOICES = (
        ('lus', 'Lus'),
        ('non lus', 'Non lus'),
        ('repondu', 'Repondu'),
       
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recever= models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='repondu')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_original = models.BooleanField(default=False)
    trading_number = models.ForeignKey(Trading, on_delete=models.CASCADE)
    def get_reply_link(self):
        return reverse('gestion:compose_message', args=[self.recever.id, self.trading_number.id])

    def get_status_display(self):
        if self.status:
            return "Lus"
        else:
            return "Non lus"

    def __str__(self):
        return self.subject
