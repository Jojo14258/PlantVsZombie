# Auteurs:

### Model
# Ce module comporte tout l'état interne et la logique du jeu

import pygame, view
import time
# des constantes
STEP_SIZE = 20
test = 0
test += 1
vitesse = 0.04
PlantesActuelles = [] #Création d'une pile : La dernière plante arrivée est ajouté au visuelle (voir main)
SunFlowersActuelles = {} #Tableau utilisé pour cumuler les boosts d'argent des sunflowers
ZombiesActuelles = {}
indice_zombie = 0 #permet de répertorier l'ordre d'ajout des zombies dans le dictionnaire ZombiesActuelles
indice_sunflowers = 0 #Pour répertorier l'ordre d'ajout des sunflowers dans le dictionnaire SunFlowersActuelles
NbPlantes = len(PlantesActuelles)
NbZombies = len(ZombiesActuelles)
NbSunFlowers = len(SunFlowersActuelles)
Monnaie = 100
def carteVersMatrice(x, y):
    """
    x - int : Coordonnée en abscisse de la 1ere tuile (en haut à gauche).
    y - int : Coordonnée en ordonnée de la 1ere tuile.
    Sortie : dict - Dictionnaire dont chaque clé correspond au numéro d'une tuile. La valeur contenue contient est un double tuple de tuple
    de la forme (abscisse_origine, (abscisse_arrivée), (ordonnee_origine), (ordonnee_arrivee). Cela permet de récupérer les coordonées
    graphique d'une tuile.
    """
    longueur = 64  #debut = 284 - 220 
    largeur = 81  #235 - 154
    departy = (y-largeur)
    dictTuiles = {}
    for y in range(0,5):
        departx = x
        numero = 9*(y)+1
        while numero <= 9*y+9:
            dictTuiles[numero] = [departx, departx+longueur], [departy, departy+largeur]
            departx += longueur
            numero += 1
        departy += largeur
    return dictTuiles

dico_plantes = {}
dico_zombies = {i: {} for i in range(1, 46)} #dictionnaire de dictionnaire qui répertorie la position de l'ensemble des zombies à la tuile près au format {self:self}
dictiTuile = carteVersMatrice(220,  155) #génération d'une matrice
dictiTuile = {1: ([220, 284], [74, 155]), 2: ([284, 358], [74, 155]), 3: ([358, 422], [74, 155]), 4: ([422, 501], [74, 155]), 5: ([501, 565], [74, 155]), 6: ([565, 629], [74, 155]), 7: ([629, 693], [74, 155]), 8: ([693, 757], [74, 155]), 9: ([757, 821], [74, 155]), 10: ([218, 282], [155, 236]), 11: ([282, 353], [155, 236]), 12: ([353, 427], [155, 236]), 13: ([427, 491], [155, 236]), 14: ([491, 565], [155, 236]), 15: ([565, 629], [155, 236]), 16: ([629, 693], [155, 236]), 17: ([693, 760], [155, 236]), 18: ([760, 824], [155, 236]), 19: ([215, 291], [236, 317]), 20: ([291, 353], [236, 317]), 21: ([353, 432], [236, 317]), 22: ([432, 496], [236, 317]), 23: ([496, 560], [236, 317]), 24: ([560, 639], [236, 317]), 25: ([639, 703], [236, 317]), 26: ([703, 767], [236, 317]), 27: ([767, 831], [236, 317]), 28: ([215, 294], [317, 398]), 29: ([294, 358], [317, 398]), 30: ([358, 432], [317, 398]), 31: ([432, 496], [317, 398]), 32: ([496, 565], [317, 398]), 33: ([565, 629], [317, 398]), 34: ([629, 693], [317, 398]), 35: ([693, 772], [317, 398]), 36: ([772, 836], [317, 398]), 37: ([210, 294], [398, 479]), 38: ([294, 358], [398, 479]), 39: ([358, 422], [398, 479]), 40: ([422, 491], [398, 479]), 41: ([491, 560], [398, 479]), 42: ([560, 629], [398, 479]), 43: ([629, 698], [398, 479]), 44: ([698, 772], [398, 479]), 45: ([772, 836], [398, 479])}

#On corrige les imperfections liés aux irrégularités du terrain (voir le commit 04.5 du Github pour la correction manuelle avec le code)
def obtenir_tuile(x, y):
    """
    x - int : La position en abscisse de la souris.
    y - int : La position en ordonnee de la souris.
    Sortie - Int : Retourne le numéro de la tuile lorsque la souris clique sur la matrice d'herbe. None est retourné
    si la souris clique en dehors. Utilisé dans controller.py
    """
    for keys, values in dictiTuile.items():
        if (values[0][0] <= x <= values[0][1]) and (values[1][0] <= y <= values[1][1]):
            return keys 
        #print("Erreur de code")
    return None


class Model:
    """
    Une classe qui contient tous les éléments logiques du jeux
    """

    def __init__(self):

        # on initialise les attributs necessaires
        self.personnage = None
        self.boutons = {} #Les clés sont le nom du bouton, les valeurs ; son instance
        # un booleen qui dit si le jeu est fini
        self.done = False

    def done(self):
        """
        Renvoie si le jeu est fini
        """
        return done

    def ajouter_bouton(self, bouton):
        """
        Fonction qui permet de rajouter un bouton a la liste des boutons
        """
        if bouton.nom not in self.boutons.keys():
            self.boutons[bouton.nom] = bouton
            
    def reinitialiser_boutons(self):
        """
        Fonction qui enlève tous les boutons de la liste.
        """
        boutons_a_supp = []
        for boutons in self.boutons.values(): #on ne peut pas modif un dictionnaire en itération
            if boutons.nom != "Jouer":
                boutons_a_supp.append(boutons.nom)
        for boutons_nom in boutons_a_supp:
            del self.boutons[boutons_nom]
            
    
    def update(self):
        """
        Fonction appellée à chaque tour de simulation du jeu
        """
        # on update chaque éléments
        self.personnage.update()


class Personnage:
    """
    Une classe qui modélise un personnage
    NOTE: ca ne concerne pas l'affichage (View), que le modéle (M)
    """

    def __init__(self, nom, NPC=True):
        """
        NPC - : Bool, True si il s'agit d'un personnage contrôlable par le joueur, fase sinon.
        """
        self.x = 0
        self.y = 0
        self.nom = nom
        self.NPC = NPC
        self.modelPerso = Model() #initialisation graphique
        self.modelPerso.personnage = self
        self.Est_mort = False
    def get_position(self):
        return (self.x, self.y)

    def obtenir_tuile(self):
        """
       Sortie - int : Retourne le numéro sur lequel se trouve l'entité. Si l'entité n'est pas sur une tuile d'herbe, None est retourné.
        """
        for keys, values in dictiTuile.items():
            if (values[0][0] <= self.x <= values[0][1]) and (values[1][0] <= self.y <= values[1][1]):
                return keys 
        #print("Erreur de code")
        return None
    
    def obtenir_ligne(self):
        """
        Sortie - int : Retourne le numéro de la ligne sur laquelle est présent le personnage.
        """
        nbTuiles = 0
        for ligne in range(1, 6):
            nbTuiles += 9
            for tuile in range(nbTuiles-8, nbTuiles+1):
                if self.obtenir_tuile() == None: #cela signifie que le zombie est sorti horizontalement de la matrice
                    DerniereTuileParcourue = self.tuilesParcourues[-1]
                    return (DerniereTuileParcourue//9)+1
                elif (dictiTuile[tuile][0][0] <= self.x <= dictiTuile[tuile][0][1]) and (dictiTuile[tuile][1][0] <= self.y <= dictiTuile[tuile][1][1]):
                    return ligne
                    
    def set_position(self, pos):
        self.x, self.y = pos
                

    def update(self):
        if self.NPC:
            self.x -= vitesse #vitesse déplacement
            self.set_position((self.x, self.y))
            
class Zombie(Personnage):
    """
    Une sous classe enfant de la classe Personnage.
    """
    def __init__(self, nom, ligne, vitesse_marche, vitesse, pv, degats):
        super().__init__(nom, NPC=True)
        self.ligne = ligne
        self.nom = nom
        self.vitesse = vitesse
        self.vitesse_marche, self.vitesse_sauvegarde = vitesse_marche, vitesse_marche  #la vitesse du zombie tend à varier, on garde donc en mémoire une variable de sauvegarde
        self.tuilesParcourues = [ligne*9]
        self.longueur_Tuile = len(self.tuilesParcourues)
        self.pv = pv
        self.degats = degats
        self.collider = None #valeur assigné dans le viewPersonnage
        self.manger = False
        self.time = 0
        self.a_Perdu = False
        global indice_zombie
        indice_zombie += 1
        ZombiesActuelles[self] = (self, indice_zombie)
        dico_zombies[self.tuilesParcourues[-1]][self] = self
        self.apparaitre(self.ligne)
      
    
    def apparaitre(self, ligne):
        Ligne_depart = 9
        Ligne_depart = Ligne_depart*ligne
        if Ligne_depart in dictiTuile.keys():
            self.x = (dictiTuile[Ligne_depart][0][1])
            self.y = ((dictiTuile[Ligne_depart][1][0]+dictiTuile[Ligne_depart][1][1])//2)
        
    def est_presentPlante(self):
            if self.collider != None:
                tuile = self.tuilesParcourues[-1]
                if tuile in dico_plantes.keys():
                    collisionPlante = dico_plantes[tuile].collider
                    if self.collider.colliderect(collisionPlante):
                        return True
                return False
    
    def Mourir(self):
        """
        Fonction qui retire toute référence à l'objet dans les variables globales et rend l'objet inactif.
        """
        del dico_zombies[self.tuilesParcourues[-1]][self]
        del ZombiesActuelles[self]
        self.Est_mort = True
        
    def endommagerPlante(self):
        """
        Fonction qui s'occupe de réduire la vie d'une plante lorsqu'elle celle-ci entre en collision avec un zombie
        Modifie par effet de bord l'attribut vie de la plante.
        """
        PeaShooter = dico_plantes[self.tuilesParcourues[-1]]
        PeaShooter.pv -= self.degats
        
    def update(self): #surcharge de la classe précédente 
        if not(self.Est_mort):
            self.x -= self.vitesse_marche #vitesse déplacement
            self.set_position((self.x, self.y)) #On change constamment la position graphique du zombie
            self.time += 0.1
            self.vitesse_marche = self.vitesse_sauvegarde #On réinitialise constamment la vitesse
            if self.pv <= 0:
                self.Mourir()
            if (self.obtenir_tuile() != None) and not(self.obtenir_tuile() in (self.tuilesParcourues)): #si le zombie n'est pas sorti de la map et que sa position n'a pas été ajouté...
                self.tuilesParcourues.append(self.obtenir_tuile())
                dico_zombies[self.tuilesParcourues[-1]][self] = self #on met à jour la position du zombie dans le dictionnaire
                if self in dico_zombies[self.tuilesParcourues[-2]].keys():
                    del dico_zombies[self.tuilesParcourues[-2]][self]  #on supprime son ancienne position
            if self.est_presentPlante():
                self.vitesse_marche = 0 #On arrête de faire marcher le zombie pendant qu'il mange
                self.manger = True   
                if self.time >= 10: #si 5 secondes ont passé...
                    self.endommagerPlante()  
                    self.time = 0
            if not(self.est_presentPlante()):
                self.manger = False   #On met fin au mode "manger"
            if self.x <= 196 and self.a_Perdu == False:
                self.a_Perdu = True
            

class PeaShooter(Personnage):
    """
    Une sous classe PeaShooter (plante) enfant de la classe Personnage.
    """
    def __init__(self, nom, tuile,vitesse, pv, degats, recharge):
        super().__init__(nom, NPC=True)
       
        self.tuile = tuile
        self.ligne = self.obtenir_ligne()
        self.nom = nom
        self.vitesse = vitesse
        self.tirer = False
        self.pv = pv
        self.degats = degats
        self.recharge = recharge
        self.collider = None #valeur assigné dans le viewPersonnage
        dico_plantes[tuile] = self
        PlantesActuelles.append(self)
        
        
    def apparaitre(self, tuile):
        self.x = ((dictiTuile[tuile][0][1]+dictiTuile[tuile][0][0])//2)
        self.y = ((dictiTuile[tuile][1][0]+dictiTuile[tuile][1][1])//2)
        
    def obtenir_ligne(self):
        """
        Sortie - int : Retourne le numéro de la ligne sur laquelle est située la plante (en partant de 1).
        """
        nbTuiles = 0
        nbTotal = 0
        for ligne in range(1, 6):
            nbTuiles += 9
            for tuile in range(nbTuiles-8, nbTuiles+1):
                nbTotal += 1
                if nbTotal == self.tuile:
                    return ligne
                
    def Mourir(self):
        """
        Supprime toute les références à l'instance afin de supprimer l'instance complètement.
        """
        del dico_plantes[self.tuile] #on supprime toute les références à l'objet
        self.Est_mort = True

        
        
    def est_presentZombie(self):
        """
        Sortie - bool : Retourne True si un zombie se situe devant le plante. False si aucun zombie
        n'est situé devant (cas où il n'y a aucun zombie ou bien les zombies sont derrière)
        """
        for tuiles in dico_zombies.values():
            for zombie in tuiles.keys():
                if (zombie.tuilesParcourues[-1] >= self.tuile) and (zombie.tuilesParcourues[-1]//9 == self.tuile//9): #Si un zombie se situe à une tuile supérieur/egale à notre PeaShooter, alors...
                    if(zombie.x) >= 219: #On vérifie que le zombie ne soit pas en dehors de la map
                        if zombie.tuilesParcourues[-1]//9+1 == self.ligne: #Zombie sur la même ligne que le PeaShooter ? 
                            return True
                elif (zombie.tuilesParcourues[-1]%9) == 0: #cas où le zombie est sur la dernière tuile
                    if zombie.tuilesParcourues[-1]//9 == self.ligne:
                        return True
        return False
        
                    
    def update(self): #surcharge de la classe précédente 
        
        if not(self.Est_mort):
            if self.pv <= 0:
                self.Mourir()
            elif self.est_presentZombie():
                self.tirer = True
            else:
                self.tirer = False

class SunFlower(Personnage):
    """
    Une sous classe PeaShooter (plante) enfant de la classe Personnage.
    """
    def __init__(self, nom, tuile,vitesse, pv):
        super().__init__(nom, NPC=True)
       
        self.tuile = tuile
        self.ligne = self.obtenir_ligne()
        self.nom = nom
        self.vitesse = vitesse
        self.tirer = False
        self.pv = pv
        self.collider = None #valeur assigné dans le viewPersonnage
        dico_plantes[tuile] = self
        global indice_sunflowers
        SunFlowersActuelles[self] = (self, indice_sunflowers)
        PlantesActuelles.append(self)
        
    def apparaitre(self, tuile):
        self.x = ((dictiTuile[tuile][0][1]+dictiTuile[tuile][0][0])//2)
        self.y = ((dictiTuile[tuile][1][0]+dictiTuile[tuile][1][1])//2)
        
    def obtenir_ligne(self):
        """
        Sortie - int : Retourne le numéro de la ligne sur laquelle est située la plante (en partant de 1).
        """
        nbTuiles = 0
        nbTotal = 0
        for ligne in range(1, 6):
            nbTuiles += 9
            for tuile in range(nbTuiles-8, nbTuiles+1):
                nbTotal += 1
                if nbTotal == self.tuile:
                    return ligne
                
    def Mourir(self):
        """
        Supprime toute les références à l'instance afin de supprimer l'instance complètement.
        """
        del dico_plantes[self.tuile] #on supprime toute les références à l'objet
        del SunFlowersActuelles[self]
        self.Est_mort = True

        
                    
    def update(self): #surcharge de la classe précédente 
        if not(self.Est_mort):
            if self.pv <= 0:
                self.Mourir()
class Pea(Personnage):
    """
    Une sous classe enfant de la classe Personnage. Il s'agit du projectile envoyé par les PeaShooters.
    """
    def __init__(self, tuile, vitesse, degats, nom):
        super().__init__(nom,  NPC=True)
        self.vitesse = 10
        self.tuile = tuile
        self.degats = degats
        self.nom = nom 
        self.apparaitre(self.tuile)
        self.Tuiles_Parcourues = []
        self.image = view.image_pea
        self.collider = self.image.get_rect() #on initialise la collision du projectile
        self.collider.x, self.collider.y = self.get_position()
        self.collider.topleft = (self.x, self.y)
     
          
        
    def est_presentZombie(self):
        """
        Sortie - Bool : Renvoi True si un zombie est présent sur la même tuile que le projectile. False sinon.
        """
        if self.collider != None:
            tuile = self.Tuiles_Parcourues[-1]
            if len(dico_zombies[tuile]) != 0: #si la tuile où se trouve le projectile n'est pas vide...
                return True
        return False
        
    def endommagerZombie(self):
        tuile = self.Tuiles_Parcourues[-1]
        for mort_vivants in dico_zombies[tuile].keys():  
            if mort_vivants.collider != None: #Sécurité en cas de problème avec la collision
                if self.collider.colliderect(mort_vivants.collider) and not(self.Est_mort):
                    mort_vivants.pv -= self.degats
                    self.Est_mort = True
                
    def apparaitre(self, tuile):
        self.x = ((dictiTuile[tuile][0][1]+dictiTuile[tuile][0][0])//2)
        self.y = ((dictiTuile[tuile][1][0]+dictiTuile[tuile][1][1])//2)
    

        
    def update(self):

        self.collider.x, self.collider.y = self.get_position() #synchronisation de la collision avec l'image
        self.collider.topleft = (self.x, self.y)
        if not(self.Est_mort):
            self.x += self.vitesse #vitesse déplacement
            self.set_position((self.x, self.y))
            if (self.obtenir_tuile() != None) and (not(self.obtenir_tuile() in (self.Tuiles_Parcourues))):
                self.Tuiles_Parcourues.append(self.obtenir_tuile())
            if self.est_presentZombie():
                self.endommagerZombie()

class Wallnut(Personnage):
    """
    Une sous classe Wallnut (noix) enfant de la classe Personnage.

    """
    def __init__(self, nom, tuile,vitesse, pv):
        super().__init__(nom, NPC=True)
       
        self.tuile = tuile
        self.ligne = self.obtenir_ligne()
        self.nom = nom
        self.pv = pv
        self.collider = None #valeur assigné dans le viewPersonnage
        self.vitesse = vitesse #vitesse d'animation
        dico_plantes[tuile] = self
        PlantesActuelles.append(self)
        
        
    def apparaitre(self, tuile):
        self.x = ((dictiTuile[tuile][0][1]+dictiTuile[tuile][0][0])//2)
        self.y = ((dictiTuile[tuile][1][0]+dictiTuile[tuile][1][1])//2)
        
    def obtenir_ligne(self):
        """
        Sortie - int : Retourne le numéro de la ligne sur laquelle est située la plante (en partant de 1).
        """
        nbTuiles = 0
        nbTotal = 0
        for ligne in range(1, 6):
            nbTuiles += 9
            for tuile in range(nbTuiles-8, nbTuiles+1):
                nbTotal += 1
                if nbTotal == self.tuile:
                    return ligne
                
    def Mourir(self):
        """
        Supprime toute les références à l'instance afin de supprimer l'instance complètement.
        """
        del dico_plantes[self.tuile] #on supprime toute les références à l'objet
        self.Est_mort = True

        
        
    def est_presentZombie(self):
        """
        Sortie - bool : Retourne True si un zombie se situe devant le plante. False si aucun zombie
        n'est situé devant (cas où il n'y a aucun zombie ou bien les zombies sont derrière)
        """
        for tuiles in dico_zombies.values():
            for zombie in tuiles.keys():
                if (zombie.tuilesParcourues[-1] >= self.tuile) and (zombie.tuilesParcourues[-1]//9 == self.tuile//9): #Si un zombie se situe à une tuile supérieur/egale à notre PeaShooter, alors...
                    if(zombie.x) >= 219: #On vérifie que le zombie ne soit pas en dehors de la map
                        if zombie.tuilesParcourues[-1]//9+1 == self.ligne: #Zombie sur la même ligne que le PeaShooter ? 
                            return True
                elif (zombie.tuilesParcourues[-1]%9) == 0: #cas où le zombie est sur la dernière tuile
                    if zombie.tuilesParcourues[-1]//9 == self.ligne:
                        return True
        return False
        
                    
    def update(self): #surcharge de la classe précédente 
        
        if not(self.Est_mort):
            if self.pv <= 0:
                self.Mourir()

