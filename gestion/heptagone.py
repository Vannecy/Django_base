"""
    Calculez la différence entre les coordonnées de l'extrémité finale et de l'extrémité initiale du trait :
        Δx=200−200=0Δx=200−200=0
        Δy=200−0=200Δy=200−0=200

    Multipliez ΔxΔx et ΔyΔy par 0,6 (60 %) pour obtenir la portion de la longueur que vous souhaitez :
        Δx60%=0×0,6=0Δx60%​=0×0,6=0
        Δy60%=200×0,6=120Δy60%​=200×0,6=120

    Ajoutez Δx60%Δx60%​ et Δy60%Δy60%​ aux coordonnées initiales pour obtenir les coordonnées du point à 60 % le long du trait :
        x60%=200+0=200x60%​=200+0=200
        y60%=0+120=120y60%​=0+120=120


        <polygon class="heptagon" points="200,0 360,80 380,240 280,360 120,360 20,240 40,80" />
        """


A = (360,80)
xA, yA = A[0], A[1]





def coordonnes_point(pourcentage,ATTAQUE, VITESSE, PHYSIQUE, DEFENSE, INTERCEPTION, PASSE, MENTAL):
    list_note = [ATTAQUE, VITESSE, PHYSIQUE, DEFENSE, INTERCEPTION, PASSE, MENTAL]
    # <polygon class="heptagon" points="250,50 410,130 430,290 330,410 170,410 70,290 90,130" />
    A,B,C,D,E,F,G = (250,50), (410,130), (430,290) ,(330,410) ,(170,410) ,(70,290), (90,130)
    liste_points_extremites = [A,B,C,D,E,F,G]
    CENTRE  = (250,250)
    x_centre = CENTRE[0]
    y_centre = CENTRE[1]
    liste_points = []
    i = 0
    for point in liste_points_extremites:
        #x2 = extremite[0]
        #y2 = extremite[1]
        x2 = point[0]
        y2 = point[1]
        Delta_x = x2 - x_centre
        Delta_y = y2 - y_centre
        Delta_x *= (list_note[i]/100)
        Delta_y *= (list_note[i]/100)
        i+=1
        coordonnes_x_pourcentage = x_centre + Delta_x
        coordonnes_y_pourcentage = y_centre + Delta_y
        liste_points.append((coordonnes_x_pourcentage,coordonnes_y_pourcentage))
    point = ( coordonnes_x_pourcentage, coordonnes_y_pourcentage)
    return liste_points


def coordonnes_point_50_pourcent():
    # <polygon class="heptagon" points="250,50 410,130 430,290 330,410 170,410 70,290 90,130" />
    A,B,C,D,E,F,G = (250,50), (410,130), (430,290) ,(330,410) ,(170,410) ,(70,290), (90,130)
    liste_points_extremites = [A,B,C,D,E,F,G]
    CENTRE  = (250,250)
    x_centre = CENTRE[0]
    y_centre = CENTRE[1]
    liste_points = []
    i = 0
    for point in liste_points_extremites:
        #x2 = extremite[0]
        #y2 = extremite[1]
        x2 = point[0]
        y2 = point[1]
        Delta_x = x2 - x_centre
        Delta_y = y2 - y_centre
        Delta_x *= (50/100)
        Delta_y *= (50/100)
        i+=1
        coordonnes_x_pourcentage = x_centre + Delta_x
        coordonnes_y_pourcentage = y_centre + Delta_y
        liste_points.append((coordonnes_x_pourcentage,coordonnes_y_pourcentage))
    point = ( coordonnes_x_pourcentage, coordonnes_y_pourcentage)
    print(liste_points)
    return liste_points















class Joueur:
    def __init__(self, nom, age, poste,nation,feet ):
        self.nom = nom
        self.nationality = nation
        self.attaque= age
        self.feet = feet

        self.poste = poste
        self.attaque, self.defense, self.physique, self.interception, self.passe, self.vitesse, self.mental =0,0,0,0,0,0,0
        
    
    def enregistrer_statistique(self,attaque, defense, physique, interception , passe, vitesse, mental):
        self.attaque, self.defense, self.physique, self.interception, self.passe, self.vitesse, self.mental = attaque, defense, physique, interception , passe, vitesse, mental
    def afficher():
        print(self.nom, self.poste, self.attaque)









