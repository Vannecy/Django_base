from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import date
class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=0,default=None,null=True) #prix de vente
    country = models.CharField(max_length=100,default=None,null=True)

    def get_general(self):
        players = Player.objects.filter(player_team=self)
        general_team = 0
        if players:
            for player in players:
                general_team += player.general
            general_team = general_team / len(players)
            return int(general_team)
        else:
            return "No Player"
        
    def get_total_players(self):
        players = Player.objects.filter(player_team=self)
        return len(players)
    
    def get_total_value(self):
        players = Player.objects.filter(player_team=self)
        total_value = 0
        for player in players:    
            total_value += player.value   
         
        return total_value

    def __str__(self):
        return self.name

class Profil(models.Model):
    name =models.CharField(max_length=100)
    user_profil = models.ForeignKey(User, on_delete=models.CASCADE)
    team_profil = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.name

class Player(models.Model):
    POSTE_CHOICES = (('Buteur', 'BU'), ('Ailier_droit', 'AD'), ('Aillier_gauche', 'AG'), ('Milieu_Offensif', 'MO'), ('Milieu_droit', 'MD'), ('Milieu_Gauche', 'MG'), ('Milieu_Centrale','MC'),('Milieu_defensif','MDC'),('Defenseur_Gauche','DG'),('Defenseur_Droit','DD'),('Defenseur_Centrale','DC'),('Goalkipper','GK'))
    FEET_CHOICE = (('Right', 'R'),('Left','L'),('RL','RL'))
    STYLE_CHOICE = (('Random','Random'),('Artiste','Artiste'), ('Dog','Dog'), ('Elegant','Elegant'), ('Killer','Killer'), ('Fidele','Fidele'), ('Leader','Leader'), ('Runner','Runner'), ('Fighter','Fighter'))
    CATEGORIE_CHOICE = (('Random','Random'),('Normal','Normal'), ('Prometteur','Promotteur'), ('Team_Star','Team_Star'), ('Internationnal','Internationnal'), ('Superstar', 'Superstar'), ('Legend','Legend'))

    name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100,default='John',blank=True, null=True)
    nationnality = models.CharField(max_length=100,blank=True, null=True)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=0)  # Ajoutez ce champ pour la valeur du joueur
    on_transfert_list = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    date_de_naissance = models.DateField(blank=True, null=True)
    size= models.PositiveSmallIntegerField(verbose_name="Taille (cm)", validators=[MinValueValidator(150), MaxValueValidator(220)], blank=True, null=True)
    weight = models.DecimalField(verbose_name="Poids (kg)", max_digits=5, decimal_places=2, validators=[MinValueValidator(40), MaxValueValidator(110)], blank=True, null=True)
    feet = models.CharField(max_length=15, choices=FEET_CHOICE, default='R', blank=True, null=True)
    style =models.CharField(max_length=15, choices=STYLE_CHOICE, blank=True, null=True)
    categorie = models.CharField(max_length=15, choices=CATEGORIE_CHOICE, default='Random', blank=True, null=True)

    main_position = models.CharField(max_length=20, choices=POSTE_CHOICES, blank=True, null=True)
    second_position = models.CharField(max_length=20, choices=POSTE_CHOICES, blank=True, null=True)
    third_position = models.CharField(max_length=20, choices=POSTE_CHOICES, blank=True, null=True)

    general = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    defense = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    attaque = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    def get_age():
        return
    def get_main_position_display_full(self):
        # Cette méthode renvoie le libellé complet du poste en fonction de l'abréviation
        for choice in self.POSTE_CHOICES:
            if choice[1] == self.main_position:
                return choice[0]
        return "Inconnu"
    def get_age(self):
        if self.date_de_naissance:
            today = date.today()
            age = today.year - self.date_de_naissance.year - ((today.month, today.day) < (self.date_de_naissance.month, self.date_de_naissance.day))
            return age
        else:
            return None
    def value_visual(self):
        
        nombre_str = str(self.value)
        parties = []
        while nombre_str:
            parties.append(nombre_str[-3:])
            nombre_str = nombre_str[:-3]
        nombre_formate = ' '.join(reversed(parties))
        return nombre_formate

    def __str__(self):
        return self.name

# Modèles (models.py)
class Trading(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('proposed', 'Proposed'),
        ('closed', 'closed'),
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_sent')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trading_received')
    proposed_value = models.DecimalField(max_digits=10, decimal_places=0,) #valeur proposer par acheteur
    sell_price = models.DecimalField(max_digits=10, decimal_places=0,default=None,null=True) #prix de vente
    contre_proposition_price = models.DecimalField(max_digits=10, decimal_places=0,default=None,null=True)
    is_accepted = models.BooleanField(default=False)
    talking_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations',default=None,null=True)
    info = models.CharField(max_length=100, default=None,null=True)
    status_trading = models.CharField(max_length=10, choices=STATUS_CHOICES, default='proposed',null=True)

      
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='non lus')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_original = models.BooleanField(default=False)
    trading_number = models.ForeignKey(Trading, on_delete=models.CASCADE,default=None,null=True)
    
    def get_reply_link(self):
        return reverse('gestion:response_message', args=[self.recever.id, self.trading_number.id,self.id])

    def get_status_display(self):
        if self.status:
            return "Lus"
        else:
            return "Non lus"

    def __str__(self):
        return self.subject
