import pygame

pygame.init()
pygame.font.init()

from model import *
from controller import *
from view import *

try:

    ### Initialisation
    model = Model()
    #modelZombie = Model()
    view = View(model)
    controller = Controller(model)
    #print(map(220,  154))
    
    
    
    
    # les boutons:
    img = pygame.image.load("./ressources/boutons/Peashooter.png").convert_alpha()
    img2 = pygame.image.load("./ressources/boutons/WallNut.jpg").convert_alpha()
    #bouton1 = Bouton("bouton1", 30, 30, 100, 50, "clique")
    PeaShooterBouton = Bouton("PeaShooter", 75, 75,  img, 1)
    WallnutBouton = Bouton("Wallnut", 100, 100,  img2, 1)
    
    
    model.ajouter_bouton(PeaShooterBouton)
    model.ajouter_bouton(WallnutBouton)
    #model.ajouter_bouton()

    # le personnage et son image:
    perso = Personnage(str("perso"),False) #2 attributs, nom et si NPC
    zombie4 = Zombie("zombieX", 4, 0.7, 0.7, 200, 100)
    zombie4 = Zombie("zombieX", 2, 0.7, 0.7, 200, 100)
    zombie4 = Zombie("zombieX", 1, 0.7, 0.7, 200, 100)
    zombie5 = Zombie("zombieFootball", 1, 0.9, 0.2, 200, 100)
    zombie6 = Zombie("zombieFootball", 5, 0.9, 0.2, 200, 100)
    zombie7 = Zombie("zombieGargantuar", 4, 0.1, 0.2, 2000, 100)
    zombie1 = Zombie("zombie1", 1, 0.20, 0.20, 200, 100)  
    zombie2 = Zombie("zombie1", 2, 0.5, 0.5, 200, 100) 
    zombie3 = Zombie("zombie1", 3, 0.5, 0.5, 200, 100) 
    
    perso.set_position((300, 300))
    model.personnage = perso
    #modelZombie.personnage = zombie1
    #modelZombie.persozombie2 = Zombie("zombie1", 2) 

    #vue_perso = ViewPersonnage(perso)
   
    #view.add_elem(vue_perso)
    i = 1
   
    ligne = 1
    clock = pygame.time.Clock()
    ### Boucle du jeu
    # chaque tour de boucle est un 'pas' dans le jeux
    while not model.done:
        clock.tick(60)  #Le jeu est fait pour être joué à 60 FPS
        # d'abord les entrées utilisateur
        controller.gerer_input()
        # puis la logique du jeu
        
        #Pour ajouter au visuelle les zombies et les plantes instances
        if len(PeaShooterActuelles) > NbPlantes: #Si un Peashooter  a été ajoutée...
            view.add_elem(ViewPersonnage(PeaShooterActuelles[-1])) #Ajout du dernier PeaShooter (Pile)
            NbPlantes = len(PeaShooterActuelles) #on réajuste le total
        #print(len(ZombiesActuelles))
        if len(ZombiesActuelles) > NbZombies: 
            for element in ZombiesActuelles:
                view.add_elem(ViewPersonnage(element)) 
                NbZombies = len(ZombiesActuelles) 

          
          
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

        if i%1000 == 0:
            if zombie1.obtenir_tuile() == None:
                if zombie1.obtenir_ligne() >=5:
                    zombie1.apparaitre(1)
                else:
                    zombie1.apparaitre(zombie1.obtenir_ligne()+1)
            if zombie2.obtenir_tuile() == None:
                if zombie2.obtenir_ligne() >=5:
                    zombie2.apparaitre(1)
                else:
                    zombie2.apparaitre(zombie2.obtenir_ligne()+1)
            if zombie3.obtenir_tuile() == None:
                if zombie3.obtenir_ligne() >=5:
                    zombie3.apparaitre(1)
                else:
                    zombie3.apparaitre(zombie3.obtenir_ligne()+1)
        view.draw()
        pygame.display.flip()

except Exception as e:
    pygame.quit()
    raise e

pygame.quit()
print("pygame_quit")
