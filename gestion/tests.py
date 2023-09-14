import random
import os
import json
from django.conf import settings


def generate_random_birthdate():
    # Choix aléatoire de l'année de naissance entre 1950 et 2005
    annee = random.randint(2000, 2007)
    
    # Choix aléatoire du mois de naissance entre 1 (janvier) et 12 (décembre)
    mois = random.randint(1, 12)
    
    # Gestion du nombre de jours en fonction du mois
    if mois in [1, 3, 5, 7, 8, 10, 12]:
        jour = random.randint(1, 31)
    elif mois == 2:
        # Février peut avoir 28 ou 29 jours en fonction de l'année bissextile
        if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
            jour = random.randint(1, 29)
        else:
            jour = random.randint(1, 28)
    else:
        jour = random.randint(1, 30)
    
    # Formater la date de naissance
    date_de_naissance = f"{jour}/{mois}/{annee}"
    
    return date_de_naissance

def Recup_Nationnality():
    # Définissez le chemin vers le répertoire où vous stockez vos fichiers JSON
    json_directory = os.path.join(settings.STATIC_ROOT, 'json')

    # Liste des fichiers JSON disponibles dans le répertoire
    json_files = [
        "Europe_name.json",
        "Afrique_name.json",
        "Amerique_name.json",
        "Asian_name.json",
        "Pacific_name.json",
        "Arabic_name.json",
    ]

    # Choisissez un fichier JSON au hasard dans la liste
    json_filename = random.choice(json_files)

    # Construisez le chemin complet vers le fichier JSON
    json_path = os.path.join(json_directory, json_filename)

    # Ouvrez et chargez le fichier JSON
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Choisir une nationalité au hasard parmi la liste des nationalités
    nationalities = [item['pays'] for item in data]  # Obtenez une liste de nationalités
    if nationalities:
        nationality_choisie = random.choice(nationalities)
    else:
        nationality_choisie = None

    print(nationality_choisie)
    return nationality_choisie
def Recup_real_name():

        # Définissez le chemin vers le répertoire où vous stockez vos fichiers JSON
    json_directory = os.path.join(settings.STATIC_ROOT, 'json')

    # Liste des fichiers JSON disponibles dans le répertoire
    """
    json_files = [
        "Europe_name.json",
        "Afrique_name.json",
        "Amerique_name.json",
        "Asian_name.json",
        "Pacific_name.json",
        "Arabic_name.json",
    ]
    """
    json_files = [
        "Europe_name.json",
    ]    
    # Choisissez un fichier JSON au hasard dans la liste
    json_filename = random.choice(json_files)

    # Construisez le chemin complet vers le fichier JSON
    json_path = os.path.join(json_directory, json_filename)

    # Ouvrez et chargez le fichier JSON
    with open(json_path, 'r',encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Choisir une nationalité au hasard parmi la liste des nationalités
    nationalities = [item['pays'] for item in data]  # Obtenez une liste de nationalités
    if nationalities:
        nationality_choisie = random.choice(nationalities)
    else:
        nationality_choisie = None

    
    nb = len(data)
    pays = random.randint(0, nb - 1)

    if 'nom' in data[pays] and 'prenom_masculin' in data[pays]:
        print('sans un s')
        print(data[pays]['pays'])
        print(data[pays]['prenom_masculin'])
        print(data[pays]['nom'])
        civil = {'name': data[pays]['nom'], 'second_name': data[pays]['prenom_masculin'], 'nationnality': data[pays]['pays']}

    elif 'noms' in data[pays] and 'prenoms_masculins' in data[pays]:
        print('avec un s------------------------------')
        print(data[pays]['pays'])
        print(data[pays]['prenoms_masculins'][0])
        print(data[pays]['noms'][0])
        civil = {'name': data[pays]['noms'][0], 'second_name': data[pays]['prenoms_masculins'][0], 'nationnality': data[pays]['pays']}

    else:
        # Handle the case where the keys are missing or have unexpected values
        print('Missing or unexpected keys in data for pays:', data[pays])
        civil = civil = {'name': "114", 'second_name': '55', 'nationnality': '555'}

    return civil

def recup_value():
    random_factor = random.randint(5, 50)
    random_number = random_factor * 10000
    final_number = random_number + 500000
    return final_number

def Recup_name():
    # Chemin vers le fichier JSON

    json_directory = os.path.join(settings.STATIC_ROOT, 'json')
    json_filename = "Top_players.json"
    json_path = os.path.join(json_directory, json_filename)

    # Ouvrir et charger le fichier JSON
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Choisir un joueur au hasard parmi la liste des joueurs
    joueurs = data.get('joueurs', [])  # Assurez-vous que 'joueurs' est la clé correcte dans votre JSON
    if joueurs:
        joueur_choisi = random.choice(joueurs)
    else:
        joueur_choisi = None

    return joueur_choisi

def generate_offensive_player_profile():
    POSTES_CHOICES = (('Buteur', 'BU'), ('Ailier_droit', 'AD'), ('Aillier_gauche', 'AG'), ('Milieu_Offensif', 'MO'), ('Milieu_droit', 'MD'), ('Milieu_Gauche', 'MG'))
    FEET_CHOICE = [('Right', 'R'),('Left','L'),('RL','RL')]
    STYLE_CHOICE = [('Random','Random'),('Artiste','Artiste'), ('Dog','Dog'), ('Elegant','Elegant'), ('Killer','Killer'), ('Fidele','Fidele'), ('Leader','Leader'), ('Runner','Runner'), ('Fighter','Fighter')]
    CATEGORIE_CHOICE = [('Random','Random'),('Normal','Normal'), ('Prometteur','Promotteur'), ('Team_Star','Team_Star'), ('Internationnal','Internationnal'), ('Superstar', 'Superstar'), ('Legend','Legend')]
 
    taille_weights = [
        (1, 0.05),  # 5% d'écart
        (2, 0.10),  # 10% d'écart
        (3, 0.15),  # 15% d'écart
        (4, 0.50),  # 50% d'écart
        (5, 0.15),  # 15% d'écart
        (6, 0.05)   # 5% d'écart
    ]
    feet = random.choices(FEET_CHOICE, weights=[0.80, 0.15,0.05])
    style = random.choices(STYLE_CHOICE, weights=[0.94, 0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
    poste = random.choices(POSTES_CHOICES)
    poste = poste[0][1]
    style = style[0][1]
    feet = feet[0][1]
    civil = Recup_real_name()
    Nationnality = civil['nationnality']
    Name = civil['name']
    Second_name = civil['second_name']
    Value =recup_value()
   
    #categorie = random.choices(CATEGORIE_CHOICE, weights=[0.4,0.2,0.1,0.1,0.1,0.05,0.01])
    # Choisissez aléatoirement une taille parmi les six profils avec les pourcentages spécifiés
    taille, _ = random.choices(taille_weights, weights=[0.05, 0.10, 0.14, 0.54, 0.11, 0.01])[0]

    if taille == 1:
        choice_taille = random.randint(160,165)
    elif taille == 2:
        choice_taille = random.randint(165,170)
    elif taille == 3:
        choice_taille = random.randint(170,178)
    elif taille == 4:
        choice_taille = random.randint(179,184)
    elif taille == 5:
        choice_taille = random.randint(185,188)
    elif taille == 6:
        choice_taille = random.randint(189,194)


    # Obtenez les deux derniers chiffres de la taille en cm
    taille_last_two_digits = choice_taille % 100

    # Générez le poids en ajoutant ou en soustrayant 5 ou 10 kg par rapport aux deux derniers chiffres de la taille
    plage_variation = list(range(-7, 7))
    poids_variation = random.choice(plage_variation )
    poids = taille_last_two_digits + poids_variation
    Birthday = generate_random_birthdate()
    Attaque = random.randint(65,85)
    Defense = random.randint(30,75) 
    Vitesse = random.randint(50,85) 
    Passe = random.randint(50,85) 
    Interception = random.randint(30,75)
    Mental = random.randint(50,85) 
    Physique = random.randint(50,85) 



    General = (Attaque+Defense) / 2
    

    # Créez un dictionnaire de profil de joueur
    player_profile = {
        "taille": choice_taille,
        "poids": poids,
        "Poste":poste,
        "Style":style,
        "Feet":feet,
        "Name":Name,
        "Birthday":Birthday,
        "Attaque": Attaque,
        "Defense":Defense,
        "Vitesse":Vitesse,
        "Passe":Passe,
        "Interception":Interception,
        "Physique":Physique,
        "Mental":Mental,
        "General":General,
        "Nationnality":Nationnality,
        "Second_name":Second_name,
        "Value":Value

        
        # Ajoutez d'autres champs ici si nécessaire
    }


    return player_profile

def generate_defensive_player_profile():
    POSTES_CHOICES = ( ('Milieu_Centrale','MC'),('Milieu_defensif','MDC'),('Defenseur_Gauche','DG'),('Defenseur_Droit','DD'),('Defenseur_Centrale','DC'))
    FEET_CHOICE = [('Right', 'R'),('Left','L'),('RL','RL')]
    STYLE_CHOICE = [('Random','Random'),('Artiste','Artiste'), ('Dog','Dog'), ('Elegant','Elegant'), ('Killer','Killer'), ('Fidele','Fidele'), ('Leader','Leader'), ('Runner','Runner'), ('Fighter','Fighter')]
    CATEGORIE_CHOICE = [('Random','Random'),('Normal','Normal'), ('Prometteur','Promotteur'), ('Team_Star','Team_Star'), ('Internationnal','Internationnal'), ('Superstar', 'Superstar'), ('Legend','Legend')]
 
    taille_weights = [
        (1, 0.05),  # 5% d'écart
        (2, 0.10),  # 10% d'écart
        (3, 0.15),  # 15% d'écart
        (4, 0.50),  # 50% d'écart
        (5, 0.15),  # 15% d'écart
        (6, 0.05)   # 5% d'écart
    ]
    feet = random.choices(FEET_CHOICE, weights=[0.80, 0.15,0.05])
    style = random.choices(STYLE_CHOICE, weights=[0.94, 0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
    poste = random.choices(POSTES_CHOICES)

    poste = poste[0][1]
    style = style[0][1]
    feet = feet[0][1]
    civil = Recup_real_name()
    Nationnality = civil['nationnality']
    Name = civil['name']
    Second_name = civil['second_name']
    Value =recup_value()
    #categorie = random.choices(CATEGORIE_CHOICE, weights=[0.4,0.2,0.1,0.1,0.1,0.05,0.01])
    # Choisissez aléatoirement une taille parmi les six profils avec les pourcentages spécifiés
    taille, _ = random.choices(taille_weights, weights=[0.01, 0.01, 0.05, 0.54, 0.24, 0.15])[0]

    if taille == 1:
        choice_taille = random.randint(160,165)
    elif taille == 2:
        choice_taille = random.randint(165,170)
    elif taille == 3:
        choice_taille = random.randint(170,178)
    elif taille == 4:
        choice_taille = random.randint(179,184)
    elif taille == 5:
        choice_taille = random.randint(185,188)
    elif taille == 6:
        choice_taille = random.randint(189,194)


    # Obtenez les deux derniers chiffres de la taille en cm
    taille_last_two_digits = choice_taille % 100

    # Générez le poids en ajoutant ou en soustrayant 5 ou 10 kg par rapport aux deux derniers chiffres de la taille
    plage_variation = list(range(-5, 9))
    poids_variation = random.choice(plage_variation )
    poids = taille_last_two_digits + poids_variation

    Birthday = generate_random_birthdate()
    Attaque = random.randint(53,85)
    Defense = random.randint(65,85) 
    Vitesse = random.randint(30,85) 
    Passe = random.randint(30,85) 
    Interception = random.randint(50,75)
    Mental = random.randint(50,85) 
    Physique = random.randint(60,85) 
    General = (Attaque+Defense) / 2
    # Créez un dictionnaire de profil de joueur
    player_profile = {
        "taille": choice_taille,
        "poids": poids,
        "Poste":poste,
        "Style":style,
        "Feet":feet,
        "Name":Name,
        "Birthday":Birthday,
        "Attaque": Attaque,
        "Defense":Defense,
        "Vitesse":Vitesse,
        "Passe":Passe,
        "Interception":Interception,
        "Physique":Physique,
        "Mental":Mental,
        "General":General,
        "Nationnality":Nationnality,
        "Second_name":Second_name,
        "Value":Value

        
        # Ajoutez d'autres champs ici si nécessaire
    }


    return player_profile

def generate_goalkipper_player_profile():
    POSTES_CHOICES = ( ('Goalkipper','GK'))
    FEET_CHOICE = [('Right', 'R'),('Left','L'),('RL','RL')]
    STYLE_CHOICE = [('Random','Random'),('Artiste','Artiste'), ('Dog','Dog'), ('Elegant','Elegant'), ('Killer','Killer'), ('Fidele','Fidele'), ('Leader','Leader'), ('Runner','Runner'), ('Fighter','Fighter')]
    CATEGORIE_CHOICE = [('Random','Random'),('Normal','Normal'), ('Prometteur','Promotteur'), ('Team_Star','Team_Star'), ('Internationnal','Internationnal'), ('Superstar', 'Superstar'), ('Legend','Legend')]
 
    taille_weights = [
        (1, 0.05),  # 5% d'écart
        (2, 0.10),  # 10% d'écart
        (3, 0.15),  # 15% d'écart
        (4, 0.50),  # 50% d'écart
        (5, 0.15),  # 15% d'écart
        (6, 0.05)   # 5% d'écart
    ]
    feet = random.choices(FEET_CHOICE, weights=[0.80, 0.15,0.05])
    style = random.choices(STYLE_CHOICE, weights=[0.94, 0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])

    poste = 'GK'
    style = style[0][1]
    feet = feet[0][1]
    Nationnality = Recup_Nationnality()
   
    #categorie = random.choices(CATEGORIE_CHOICE, weights=[0.4,0.2,0.1,0.1,0.1,0.05,0.01])
    # Choisissez aléatoirement une taille parmi les six profils avec les pourcentages spécifiés
    taille, _ = random.choices(taille_weights, weights=[0.01, 0.01, 0.05, 0.24, 0.44, 0.15])[0]

    if taille == 1:
        choice_taille = random.randint(180,181)
    elif taille == 2:
        choice_taille = random.randint(181,182)
    elif taille == 3:
        choice_taille = random.randint(182,183)
    elif taille == 4:
        choice_taille = random.randint(183,186)
    elif taille == 5:
        choice_taille = random.randint(187,190)
    elif taille == 6:
        choice_taille = random.randint(190,197)


    # Obtenez les deux derniers chiffres de la taille en cm
    taille_last_two_digits = choice_taille % 100

    # Générez le poids en ajoutant ou en soustrayant 5 ou 10 kg par rapport aux deux derniers chiffres de la taille
    plage_variation = list(range(-5, 9))
    poids_variation = random.choice(plage_variation )
    poids = taille_last_two_digits + poids_variation
    player_recup = Recup_name()
    Name = player_recup['nom']
    Birthday = generate_random_birthdate()
    Attaque = random.randint(60,75)
    Defense = random.randint(60,75)
    General = (Attaque+Defense) / 2
    # Créez un dictionnaire de profil de joueur
    player_profile = {
        "taille": choice_taille,
        "poids": poids,
        "Poste":poste,
        "Style":style,
        "Feet":feet,
        "Name":Name,
        "Birthday":Birthday,
        "Attaque": Attaque,
        "Defense":Defense,
        "General":General,
        "Nationnality":Nationnality

        
        # Ajoutez d'autres champs ici si nécessaire
    }


    return player_profile



