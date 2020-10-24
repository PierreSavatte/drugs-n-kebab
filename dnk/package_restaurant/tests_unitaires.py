import pygame

from . import (
    generation_restaurant,
    personnage_du_joueur,
    gestion_restaurant,
)
from .restaurant import Restaurant
from .. import time_DnK
from ..constantes import Constantes

pygame.font.init()
font = pygame.font.Font("font.ttf", 20)

pygame.init()
fenetre = pygame.display.set_mode(Constantes.taille_fen)
temps = time_DnK.Time()

joueur = personnage_du_joueur.Perso_du_joueur("Hugo")
grille_restaurant = generation_restaurant.gen_restaurant()
restaurant = Restaurant(grille_restaurant)
gestion_restaurant.loop(
    fenetre, font, restaurant, joueur, temps, pas_de_clients=False
)
