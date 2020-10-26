import pygame

from ..constants import Constantes


class Perso_du_joueur:
    def __init__(self, nom_joueur):
        self.nom_du_joueur = nom_joueur
        self.position = Constantes.spawn_restaurant
        self.orientation = "UP"
        self.sprites = Constantes.sprites_joueur
        self.liste_recettes_debloquees = {
            Constantes.nom_kebab_simple: [Constantes.nom_pain]
        }
        self.satisfaction = 0
        self.notoriete = 0

        self.action = False
        self.debut_temps_action = None
        self.action_liee = None
        self.action_termine = False
        return

    def deplacer_joueur(self, touche_deplacement, grille):
        position_deplacee = self.position
        orientation_precedente = self.orientation

        if touche_deplacement == pygame.K_UP:
            position_deplacee = (self.position[0], self.position[1] - 1)
            self.orientation = "UP"
        elif touche_deplacement == pygame.K_DOWN:
            position_deplacee = (self.position[0], self.position[1] + 1)
            self.orientation = "DOWN"
        elif touche_deplacement == pygame.K_RIGHT:
            position_deplacee = (self.position[0] + 1, self.position[1])
            self.orientation = "RIGHT"
        elif touche_deplacement == pygame.K_LEFT:
            position_deplacee = (self.position[0] - 1, self.position[1])
            self.orientation = "LEFT"

        if position_deplacee != self.position:
            if 0 <= position_deplacee[0] < len(grille):
                if 1 <= position_deplacee[1] < len(grille[0]):
                    if grille[position_deplacee[0]][position_deplacee[1]][
                        Constantes.nom_biblio_walkable
                    ]:
                        self.position = position_deplacee
                        self.action = False
                        self.debut_temps_action = None
                        self.action_liee = None
                        self.action_termine = False
        if orientation_precedente != self.orientation:
            self.action = False
            self.debut_temps_action = None
            self.action_liee = None
            self.action_termine = False
        return

    def get_position_en_face(self):
        (x, y) = self.position
        if self.orientation == "LEFT":
            return x - 1, y
        if self.orientation == "UP":
            return x, y - 1
        if self.orientation == "DOWN":
            return x, y + 1
        else:
            return x + 1, y

    def test_presence_client(self, restaurant, position):
        liste_pos_clients = []
        for client in restaurant.clients:
            liste_pos_clients.append(client.position)
        return position in liste_pos_clients

    def get_biblio_caisse(self, biblios_caisses, position_caisse):
        for biblio_caisse in biblios_caisses:
            if (
                biblio_caisse[Constantes.nom_biblio_position]
                == position_caisse
            ):
                return biblio_caisse

    def update_biblio_caisse(self, temps, biblio_caisse):
        biblio_caisse[Constantes.nom_biblio_client_geree_en_caisse] = True
        biblio_caisse[
            Constantes.nom_biblio_temps_depart_client_geree_en_caisse
        ] = temps.get_time()
        return

    def gestion_actions(self, temps, touche_clavier, restaurant):
        if not self.action:
            if touche_clavier == pygame.K_e:
                (x, y) = self.get_position_en_face()
                if restaurant.grille_meubles[x][y][
                    Constantes.nom_biblio_sprite
                ] == Constantes.sprite_caisse and self.test_presence_client(
                    restaurant, (x, y + 1)
                ):
                    self.action_liee = "vente"
                    self.action = True
                    self.debut_temps_action = temps.get_time()
                    self.update_biblio_caisse(
                        temps,
                        self.get_biblio_caisse(restaurant.pos_caisses, (x, y)),
                    )
                elif (
                    restaurant.grille_meubles[x][y][
                        Constantes.nom_biblio_sprite
                    ]
                    in Constantes.liste_cuisines
                    and restaurant.commande_geree is not None
                ):
                    self.action_liee = "cuisine"
                    self.action = True
                    self.debut_temps_action = temps.get_time()
        else:
            if self.action_liee == "vente":
                if (
                    temps.get_time()
                    >= self.debut_temps_action
                    + Constantes.delai_gestion_client_en_caisse
                ):
                    self.action = False
                    self.debut_temps_action = None
                    self.action_termine = True
            if self.action_liee == "cuisine":
                if (
                    temps.get_time()
                    >= self.debut_temps_action
                    + Constantes.delai_gestion_client_en_caisse
                ):
                    self.action = False
                    self.debut_temps_action = None
                    self.action_termine = True
                    restaurant.cuisine()
        return

    def get_sprite(self):
        if self.orientation == "UP":
            return self.sprites[0]
        elif self.orientation == "DOWN":
            return self.sprites[1]
        elif self.orientation == "RIGHT":
            return self.sprites[2]
        elif self.orientation == "LEFT":
            return self.sprites[3]
