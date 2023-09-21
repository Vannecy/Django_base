from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import date
from django.core.exceptions import ValidationError







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
    
    def get_players_name(self, id):
        players = Player.objects.filter(player_team=self)
        if id < len(players):     
            return players[id]
        else:
            return ""
    
    def get_total_value(self):
        players = Player.objects.filter(player_team=self)
        total_value = 0
        for player in players:    
            total_value += player.value   
         
        return total_value
    
    def number_is_available(self, number):
        players = Player.objects.filter(player_team=self)
        for player in players:
            if player.number == number:
                return False
            else:
                return True

    
    def __str__(self):
        return self.name
    





class Profil(models.Model):
    name =models.CharField(max_length=100)
    user_profil = models.ForeignKey(User, on_delete=models.CASCADE)
    team_profil = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.name

class Player(models.Model):
    TEAM_POSTES =  (('Remplacent', 'Rp'),('Buteur', 'BU'), ('Ailier_droit', 'AD'), ('Aillier_gauche', 'AG'), ('Milieu_Offensif', 'MO'), ('Milieu_Centrale','MC'),('Milieu_defensif','MDC'),('Defenseur_Gauche','DG'),('Defenseur_Droit','DD'),('Defenseur_Centrale','DC'),('Goalkipper','GK'))
    POSTE_CHOICES = (('Buteur', 'BU'), ('Ailier_droit', 'AD'), ('Aillier_gauche', 'AG'), ('Milieu_Offensif', 'MO'), ('Milieu_droit', 'MD'), ('Milieu_Gauche', 'MG'), ('Milieu_Centrale','MC'),('Milieu_defensif','MDC'),('Defenseur_Gauche','DG'),('Defenseur_Droit','DD'),('Defenseur_Centrale','DC'),('Goalkipper','GK'))
    FEET_CHOICE = (('Right', 'R'),('Left','L'),('RL','RL'))
    STYLE_CHOICE = (('Random','Random'),('Artiste','Artiste'), ('Dog','Dog'), ('Elegant','Elegant'), ('Killer','Killer'), ('Fidele','Fidele'), ('Leader','Leader'), ('Runner','Runner'), ('Fighter','Fighter'))
    CATEGORIE_CHOICE = (('Random','Random'),('Normal','Normal'), ('Prometteur','Promotteur'), ('Team_Star','Team_Star'), ('Internationnal','Internationnal'), ('Superstar', 'Superstar'), ('Legend','Legend'))

    name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100,default='John',blank=True, null=True)
    nationnality = models.CharField(max_length=100,blank=True, null=True)
    player_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)],blank=True, null=True, default=99)
    value = models.DecimalField(max_digits=10, decimal_places=0)  # Ajoutez ce champ pour la valeur du joueur
    on_transfert_list = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    is_starter = models.BooleanField(default=False) #Sur le terrain
    position_on_the_field = models.CharField(max_length=20, choices=TEAM_POSTES, blank=True, null=True)

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
    passe = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    vitesse = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    interception = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    mental = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)
    physique =models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True, null=True)


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
    def value_visual(self): #Pour voir un espace tous les 3 chiffres pour les grands nombres
        
        nombre_str = str(self.value)
        parties = []
        while nombre_str:
            parties.append(nombre_str[-3:])
            nombre_str = nombre_str[:-3]
        nombre_formate = ' '.join(reversed(parties))
        return nombre_formate

    def set_position_on_the_field(self, position):
         # Vérifier si un autre joueur de la même équipe a déjà cette position
        players_with_same_position = Player.objects.filter(
            player_team=self.player_team,
            position_on_the_field=position
        ).exclude(id=self.id)

        if not players_with_same_position.exists():
            print("----------------ok on change")
            self.position_on_the_field = position
        
 
    def exchange_position(self, other_player):
        # Vérifier si les deux joueurs appartiennent à la même équipe
        if self.player_team != other_player.player_team:
            raise ValidationError("Les joueurs n'appartiennent pas à la même équipe.")

        # Échanger les positions sur le terrain
        self_position = self.position_on_the_field
        other_position = other_player.position_on_the_field

        # Si l'un des joueurs est un remplaçant, il prend la position de l'autre joueur
        if self.is_starter and not other_player.is_starter:
            other_player.position_on_the_field = self_position
            self.position_on_the_field = None  # Le joueur devient remplaçant
        elif not self.is_starter and other_player.is_starter:
            self.position_on_the_field = other_position
            other_player.position_on_the_field = None  # L'autre joueur devient remplaçant
        else:
            # Les deux joueurs ne sont pas remplaçants, échange de poste
            self.position_on_the_field, other_player.position_on_the_field = other_position, self_position

        # Enregistrer les changements dans la base de données
        self.save()
        other_player.save()

    def __str__(self):
        name = str(self.name + " " +  self.second_name)
        return name


class Formation(models.Model):


    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,default=None,null=True)
    
    TEAM_POSTES =  (('Remplacent', 'Rp'),('Buteur', 'BU'), ('Ailier_droit', 'AD'), ('Aillier_gauche', 'AG'), ('Milieu_Offensif', 'MO'), ('Milieu_Centrale','MC'),('Milieu_defensif','MDC'),('Defenseur_Gauche','DG'),('Defenseur_Droit','DD'),('Defenseur_Centrale','DC'),('Goalkipper','GK'))

    player1 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player1')
    player1_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player1_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player1_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='GK', blank=True, null=True)

    player2 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player2')
    player2_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player2_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player2_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player3 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player3')
    player3_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player3_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player3_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player4 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player4')
    player4_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player4_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player4_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player5 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player5')
    player5_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player5_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player5_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player6 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player6')
    player6_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player6_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player6_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player7 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player7')
    player7_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player7_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player7_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player8 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player8')
    player8_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player8_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player8_poste = models.CharField(max_length=20, choices=TEAM_POSTES, default='Rp',blank=True, null=True)

    player9 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player9')
    player9_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player9_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player9_poste = models.CharField(max_length=20, choices=TEAM_POSTES, default='Rp',blank=True, null=True)

    player10 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player10')
    player10_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player10_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player10_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)

    player11 = models.ForeignKey(Player, on_delete=models.CASCADE,default=None, blank=True, null=True,related_name='formation_player11')
    player11_x = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player11_y = models.DecimalField(max_digits=10, decimal_places=0,default=None, blank=True, null=True)
    player11_poste = models.CharField(max_length=20, choices=TEAM_POSTES,default='Rp', blank=True, null=True)


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

