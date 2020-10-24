"""
Created on 18 janv. 2016

@author: Hugo
"""
from ..constantes import Constantes


def generation_bibliotheque(fichier_sprite, walkable, objectif):
    bibliotheque = {}
    bibliotheque[Constantes.nom_biblio_sprite] = fichier_sprite
    bibliotheque[Constantes.nom_biblio_walkable] = walkable
    bibliotheque[Constantes.nom_biblio_est_objectif] = objectif
    return bibliotheque


def generation_grille():
    grille = []
    for x in range(Constantes.taille_restaurant[0]):
        grille.append([])
        for y in range(Constantes.taille_restaurant[1]):
            grille[x].append(generation_bibliotheque(None, True, False))
    return grille


def remplir_grille(grille):
    grille[0][1] = generation_bibliotheque(
        Constantes.sprite_evier, False, False
    )
    grille[1][1] = generation_bibliotheque(
        Constantes.sprite_table_de_travail, False, False
    )
    mettre_une_table_simple(grille, (1, 6))
    grille[2][1] = generation_bibliotheque(
        Constantes.sprite_comptoir, False, False
    )
    grille[3][1] = generation_bibliotheque(
        Constantes.sprite_machine_kebab_1, False, False
    )
    grille[3][0] = generation_bibliotheque(
        Constantes.sprite_machine_kebab_2, True, False
    )
    grille[0][3] = generation_bibliotheque(
        Constantes.sprite_meuble_5, False, False
    )
    grille[4][1] = generation_bibliotheque(
        Constantes.sprite_meuble_1, False, False
    )
    grille[4][2] = generation_bibliotheque(
        Constantes.sprite_meuble_2, False, False
    )
    grille[4][3] = generation_bibliotheque(
        Constantes.sprite_meuble_3, False, False
    )
    grille[3][3] = generation_bibliotheque(
        Constantes.sprite_caisse, False, False
    )
    grille[2][3] = generation_bibliotheque(
        Constantes.sprite_meuble_4, False, False
    )
    mettre_une_table_simple(grille, (6, 2))
    mettre_une_table_simple(grille, (6, 4))
    grille[3][7] = generation_bibliotheque(
        Constantes.sprite_tapis_1, True, False
    )
    return grille


def mettre_une_table_simple(grille, pos):
    (x, y) = pos
    grille[x][y] = generation_bibliotheque(
        Constantes.sprite_table_simple, False, False
    )
    grille[x - 1][y] = generation_bibliotheque(
        Constantes.sprite_chaise_right, True, False
    )
    grille[x + 1][y] = generation_bibliotheque(
        Constantes.sprite_chaise_left, True, False
    )
    return


def ajout_sprite_grille(grille, meuble, coordonnees_souris):
    grille[coordonnees_souris[0]][coordonnees_souris[1]] = meuble
    return grille


def gen_restaurant():
    restaurant = remplir_grille(generation_grille())
    return restaurant
