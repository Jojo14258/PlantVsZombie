import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()
from model import *
from controller import *
from view import *
from random import randint
try:

    ### Initialisation
    model = Model()
    #modelZombie = Model()
    view = View(model)
    controller = Controller(model)
    compteur = 0
    compteur1 = 0
    frequence = 0
    DelaiAvantVague = 0
    indice_dernierZombie = 0
    indice_dernierSunflower = 0
    zombies_par_niveaux = {1: {"zombie1": 3}, 2:{"zombie1": 5, "zombieFootball":5}, 3:{"zombieFootball":0, "zombieX": 20}, 4:{"zombie1":8, "zombieFootball":7, "zombieX":0}, 4:{"zombie1":15, "zombieFootball":15, "zombieX":0}, 5:{"zombie1":15, "zombieFootball":30, "zombieX":15, "zombieGargantuar":1}, 6:{}} #dictionnaire de la forme {niveau: {zombies:nombre} }. Permet de définir le nombre de zombies par niveaux.
    Temps_par_niveaux = {1:850, 2:(600), 3:(100), 4:(200), 5:(100)}  #Format : {NumeroTuile[Frequence_D'apparition_Zombie]}
    zombies_caracteristiques = {"zombie1":["zombie1", randint(1,5), 0.3, 0.5, 200, 120], "zombieFootball": ["zombieFootball", randint(1,5), 1.1, 0.2, 200, 100], "zombieGargantuar":["zombieGargantuar", 4, 0.1, 0.2, 3000, 100],  "zombieX":["zombieX", 1, 0.7, 0.7, 200, 100]}
    niveau_actuel = 1
    Perdu = False
    Gagne = False
  


    
    #La musique
    pygame.mixer_music.load("ressources/pvzmusique.mp3")
    pygame.mixer_music.play(-1)
    # les boutons:
    img = pygame.image.load("./ressources/boutons/Peashooter.png").convert_alpha()
    img2 = pygame.image.load("./ressources/boutons/WallNut.jpg").convert_alpha()
    img3 = pygame.image.load("./ressources/boutons/JouerBouton.png").convert_alpha()
    img4 = pygame.image.load("./ressources/boutons/pelle.png").convert_alpha()
    img5 = pygame.image.load("./ressources/boutons/sunflower.png").convert_alpha()
    img6 = pygame.image.load("ressources/Invisible.jpg").convert_alpha()
    img7 = pygame.image.load("ressources/Victoire.png").convert_alpha()
    #bouton1 = Bouton("bouton1", 30, 30, 100, 50, "clique")
    PeaShooterBouton = Bouton("PeaShooter", 0, 0,  img, 1)
    WallnutBouton = Bouton("Wallnut", 0, 60,  img2, 1)
    SunflowerBouton = Bouton("Sunflower", 0, 128, img5, 0.78)
    BoutonJouer = Bouton("Jouer",200, 200, img3, 1)
    BoutonEffacer = Bouton("Effacer", 125, 0, img4, 0.5)
    
    model.ajouter_bouton(BoutonJouer)

  
   
    clock = pygame.time.Clock()
    
    #--------------------------------Fonctions essentielles du jeu-------------------#
    
    def jouer():
        """ 
        Une fonction pour charger l'ensemble des instructions essentielles du jeu
        """
        model.ajouter_bouton(PeaShooterBouton)
        model.ajouter_bouton(SunflowerBouton)
        model.ajouter_bouton(WallnutBouton)
        model.ajouter_bouton(BoutonEffacer)
        view.Jouer = True #On active la fenêtre de jeu
        global NbPlantes
        global indice_dernierSunflower
        global NbSunFlowers
        global Perdu
        global indice_dernierZombie
        if len(PlantesActuelles) > NbPlantes: #Si une plante  a été ajoutée...
            view.add_elem(ViewPersonnage(PlantesActuelles[-1])) #Ajout du dernier PeaShooter (Pile)
            NbPlantes = len(PlantesActuelles) #on réajuste le total
        
        global SunFlower
        global indice_dernierZombie
        for sunflower_tuple in SunFlowersActuelles.values():
            if sunflower_tuple[1] >  indice_dernierSunflower:
                indice_dernierSunflower = sunflower_tuple[1]
            
        NbSunFlowers = len(SunFlowersActuelles) 
        for element in dico_zombies.values(): #Cette ligne permet de vérifier qu'un zombie ait passé la pelouse
            for zombies in element.values():
                if zombies.a_Perdu: 
                    Perdu = True  #Alors on arrête le jeu via le changement de cette variable
    

    
            
        for element in view.elems: #parcours des éléments visuels (zombies, plantes...)
            element.personnage.update() #on met à jour leur statut
            element.personnage.modelPerso.update()
            
        indice_projectile = 0
        longueur_projectile_list = len(projectiles)
        #Une boucle qui met à jour les projectiles (pea)
        while indice_projectile < longueur_projectile_list: #Une boucle pour parcourir la list contenant nos projectiles (pea)
            projectiles[indice_projectile].update()
            if (projectiles[indice_projectile].x) >= 870 or (projectiles[indice_projectile].Est_mort):  #Si le projectile sort de la map ou a touché un zombie...
                del projectiles[indice_projectile]  #on supprime le projectile de la list
                longueur_projectile_list = len(projectiles) #Mise à jour longueur list pour éviter un out of range
            indice_projectile += 1
    
    
    def Mettre_a_jour_Zombies():
        """
        Une boucle qui met à jour le compteur de zombies. Le compteur de zombies est utilisé dans 
        la fonction niveau afin de passer d'un niveau en plus quand tous les zombies sont morts.
        """
        global NbZombies
        global indice_dernierZombie
        for zombie_tuple in ZombiesActuelles.values():
            if zombie_tuple[1] >  indice_dernierZombie:
                indice_dernierZombie = zombie_tuple[1]
                view.add_elem(ViewPersonnage(zombie_tuple[0]))
        NbZombies = len(ZombiesActuelles) 
         
    def ajouter_monnaie():
        """
        Une fonction pour ajouter de l'argent à chaque intervalle de temps.
        """
        global compteur
        compteur += 1+0.35*NbSunFlowers
        if compteur > 900: #Note : 600 tics correspondent à 10 secondes
            compteur = 0
            model.boutons["PeaShooter"].monnaie += 50

    def niveau():
        """ 
        Une fonction qui gère l'organisation des niveaux (difficultés, vague...)
        """
        global NbZombies
        global compteur1
        global DelaiAvantVague
        global zombies_par_niveaux
        global niveau_actuel
        global zombies_caracteristiques
        global frequence
        Passer_niveau_suivant = True
        for zombie, nombre in zombies_par_niveaux[niveau_actuel].items():
            Mettre_a_jour_Zombies()
            if niveau_actuel != 6: #lorsque le joueur atteint le niveau 6, il a gagné.
                if zombies_par_niveaux[niveau_actuel][zombie] > 0:
                    compteur1 += 1
                    DelaiAvantVague += 1 
                    if (DelaiAvantVague > 400):
                        frequence += 1
                        if randint(Temps_par_niveaux[niveau_actuel]-1,Temps_par_niveaux[niveau_actuel]+4 ) < frequence: 
                            frequence = 0
                            nom, ligne, vitesse_marche, vitesse, pv, degats = zombies_caracteristiques[zombie][0], randint(1, 5), zombies_caracteristiques[zombie][2], zombies_caracteristiques[zombie][3], zombies_caracteristiques[zombie][4], zombies_caracteristiques[zombie][5]
                            Zombie(nom, ligne, vitesse_marche, vitesse, pv, degats)
                            zombies_par_niveaux[niveau_actuel][zombie] -= 1
                            compteur1 = 0
                
                elif (NbZombies == 0) and (not(niveau_actuel >= 6)):
                    for nombre in zombies_par_niveaux[niveau_actuel].values():
                        if nombre >0:
                            Passer_niveau_suivant = False # Ici on fixe un ancien bug : on s'assure qu'il n'y ait plus de zombies à spawn
                    Mettre_a_jour_Zombies() #On vérifie une dernière fois que tous les zombies ont été tués 
                    if (NbZombies == 0 and Passer_niveau_suivant):
                        DelaiAvantVague = 400
                        niveau_actuel += 1  

        
        
    
    ### Boucle du jeu
    # chaque tour de boucle est un 'pas' dans le jeux
    
    #-------------------------------Boucle de jeu---------------------------------#
    
    while not model.done:
        clock.tick(60)  #Le jeu est fait pour être joué à 60 FPS
        controller.gerer_input()
        if (BoutonJouer.est_Clique) and (not(Perdu) and not(Gagne)):
            jouer() #Le bug doit se trouver ici
            ajouter_monnaie()
            niveau()
            if niveau_actuel >= 6:
                Gagne = True
            NbSunFlowers = 0
            
        elif Perdu:
            zombies_stocker = []
            for tuiles in dico_zombies.values():
                for zombies in tuiles:
                    zombies_stocker.append(zombies)
            for zombies in zombies_stocker:
                zombies.Mourir()
            View.jouer = False
            model.reinitialiser_boutons()
            if (dico_zombies != {}) or (dico_plantes != {}):
                dico_zombies = {}
                dico_plantes = {}
            BoutonPerdu = Bouton("Perdu",200, 200, img6, 1)
            model.ajouter_bouton(BoutonPerdu)
            
        elif Gagne:
            zombies_stocker = []
            for tuiles in dico_zombies.values():
                for zombies in tuiles:
                    zombies_stocker.append(zombies)
            for zombies in zombies_stocker:
                zombies.Mourir()
            View.jouer = False
            model.reinitialiser_boutons()
            if (dico_zombies != {}) or (dico_plantes != {}):
                dico_zombies = {}
                dico_plantes = {}
            BoutonPerdu = Bouton("Gagne", 120,120, img7, 2)
            model.ajouter_bouton(BoutonPerdu)
             
        view.draw()
        pygame.display.flip()

except Exception as e:
    pygame.quit()
    raise e

pygame.quit()
print("pygame_quit")
