import sys
import os
import pygame

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

from constantes import Constantes
import client
import affichage
import generation_restaurant
import personnage_du_joueur
from personnel import Personnel
from restaurant import Restaurant
import gestion_restaurant
import time_DnK

pygame.font.init()
font = pygame.font.Font('font.ttf', 20)

pygame.init()
fenetre = pygame.display.set_mode(Constantes.taille_fen)
temps = time_DnK.Time()

joueur = personnage_du_joueur.Perso_du_joueur("Hugo")
grille_restaurant = generation_restaurant.gen_restaurant()
restaurant = Restaurant(grille_restaurant)
gestion_restaurant.loop(fenetre,font,restaurant,joueur,temps,pas_de_clients = False)