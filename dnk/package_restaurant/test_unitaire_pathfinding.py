from . import (
    generation_restaurant,
    pathfinding_A_etoile,
)
from ..constantes import Constantes


"""
pygame.init()
fenetre = pygame.display.set_mode(Constantes.taille_fen)
joueur = personnage_du_joueur.Perso_du_joueur("Hugo")

affichage.affichage_restaurant(restaurant,fenetre,joueur)
print("Constantes.spawn_restaurant")
print(Constantes.spawn_restaurant)
"""
restaurant = generation_restaurant.gen_restaurant()
chemin = pathfinding_A_etoile.pathfinding(
    restaurant, Constantes.spawn_restaurant, (3, 2)
)
print(chemin)
