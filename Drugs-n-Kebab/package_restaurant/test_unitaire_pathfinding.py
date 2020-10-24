import sys
import os
import pygame

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from constantes import Constantes
import affichage
import generation_restaurant
import personnage_du_joueur
import pathfinding_A_etoile

"""
pygame.init()
fenetre = pygame.display.set_mode(Constantes.taille_fen)
joueur = personnage_du_joueur.Perso_du_joueur("Hugo")

affichage.affichage_restaurant(restaurant,fenetre,joueur)
print("Constantes.spawn_restaurant")
print(Constantes.spawn_restaurant)
"""
restaurant = generation_restaurant.gen_restaurant()
chemin = pathfinding_A_etoile.pathfinding(restaurant,Constantes.spawn_restaurant,(3,2))
print(chemin)