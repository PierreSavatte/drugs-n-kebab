import time

import pygame

from .. import main_fonctions
from ..constantes import Constantes


def coordonnees_en_position(coordonnees, taille_sprite):
    """
    Fonction convertissant des coordonnées dans un quadrillage en position dans la fenetre
    @return: position dans la fenetre, tupple d'entiers
    """
    return (
        coordonnees[0] * taille_sprite[0] + Constantes.larg_cadre_interface,
        coordonnees[1] * taille_sprite[1],
    )


def position_en_coordonnees(position, taille_sprite):
    """
    Fonction convertissant des coordonnées dans un quadrillage en position dans la fenetre
    @return: position dans la fenetre, tupple d'entiers
    """
    return (
        int(
            (position[0] - Constantes.larg_cadre_interface) / taille_sprite[0]
        ),
        int(position[1] / taille_sprite[1]),
    )


def affichage_sprites(Surface, sprite, coordonnees):
    """
    Fonction permettant l'affichage d'un sprite
    @param Surface: surface dans laquelle afficher le sprite, surface pygame
    @param sprite: sprite a afficher, image pygame
    @param coordonnees: coordonnees du sprite a afficher dans le quadrillage
    """
    Surface.blit(sprite, (coordonnees, Constantes.taille_bouton))
    return


def affichage_rect(Surface, coordonnees, couleur):
    """
    Fonction permettant l'affichage d'un sprite
    @param Surface: surface dans laquelle afficher le sprite, surface pygame
    @param sprite: sprite a afficher, image pygame
    @param coordonnees: coordonnees du sprite a afficher dans le quadrillage
    """
    pygame.draw.rect(
        Surface, couleur, (coordonnees, Constantes.taille_bouton), 2
    )
    return


def affichage_bouton(Surface, sprite, position):
    """
    Fonction permettant l'affichage d'un bouton
    @param Surface: surface dans laquelle afficher le sprite, surface pygame
    @param sprite: sprite du bouton, image pygame
    @param position: coordonnée haut droite du bouton dans la fenetre
    """
    pygame.draw.rect(
        Surface,
        Constantes.couleur_rect_boutons,
        (position, Constantes.taille_bouton),
        width=1,
    )
    Surface.blit(sprite, (position, position, Constantes.taille_bouton))
    return


def get_clavier():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return event.key
    else:
        return None


def add_sprites(groupe, nom_sprite):
    sprite_block = pygame.sprite.Sprite()

    sprite_block.image = pygame.Surface((16, 16))
    sprite_block.image.set_colorkey((0, 0, 0))
    image_sprite = pygame.image.load(nom_sprite).convert()
    sprite_block.image.blit(
        image_sprite, ((0, 0), (16, 16))
    )  # fill((255,255,255))
    sprite_block.rect = sprite_block.image.get_rect()

    groupe.add(sprite_block)
    return


def create_groupe():
    return pygame.sprite.Group()


def get_taille_sprite(grille_meubles):
    taille_resto_x = len(grille_meubles)
    taille_resto_y = len(grille_meubles[0])
    (taille_fen_x, taille_fen_y) = Constantes.taille_fen
    taille_sprite = min(
        int(taille_fen_x / taille_resto_x), int(taille_fen_y / taille_resto_y)
    )
    return (taille_sprite, taille_sprite)


def affichage_restaurant(
    restaurant, fenetre, font, joueur, boutons_actions_employes, temps
):
    fenetre.fill((255, 255, 255))
    pygame.display.set_icon(pygame.image.load(Constantes.icone))
    pygame.display.set_caption("Drugs'n'Kebab")
    taille_sprite = get_taille_sprite(restaurant.grille_meubles)
    affichage_fond(fenetre, taille_sprite)
    affichage_interface(fenetre, font, temps.get_temps_horloge())
    for x in range(Constantes.taille_restaurant[0]):
        for y in range(Constantes.taille_restaurant[1]):
            if (
                restaurant.grille_meubles[x][y][Constantes.nom_biblio_sprite]
                is not None
            ):
                sprite = pygame.image.load(
                    restaurant.grille_meubles[x][y][
                        Constantes.nom_biblio_sprite
                    ]
                )
                affichage_sprites(
                    fenetre,
                    redim_sprite(sprite, taille_sprite),
                    coordonnees_en_position((x, y), taille_sprite),
                )
                """
                    #Affichage des rects pour l'affichage des objectifs
                """
                """
                if restaurant.grille_meubles[x][y][Constantes.nom_biblio_est_objectif]:
                    affichage_rect(fenetre,coordonnees_en_position((x,y),taille_sprite),(255,0,0))
                """
    affichage_joueur(
        fenetre, temps, joueur, restaurant.grille_meubles, taille_sprite
    )
    if len(restaurant.clients) != 0:
        for client in restaurant.clients:
            affichage_client(
                fenetre,
                temps,
                client,
                restaurant.grille_meubles,
                taille_sprite,
                font,
            )
    if len(restaurant.employes) != 0:
        for employe in restaurant.employes:
            affichage_employe(
                fenetre,
                employe,
                restaurant.grille_meubles,
                taille_sprite,
                font,
            )
    for biblio in restaurant.pos_caisses:
        if biblio[Constantes.nom_biblio_client_geree_en_caisse]:
            print(biblio[Constantes.nom_biblio_client_geree_en_caisse])
            (x, y) = biblio[Constantes.nom_biblio_position]
            temps_final = (
                biblio[
                    Constantes.nom_biblio_temps_depart_client_geree_en_caisse
                ]
                + Constantes.delai_gestion_client_en_caisse
            )
            affichage_barre_attente(
                fenetre,
                (x, y - 1),
                biblio[
                    Constantes.nom_biblio_temps_depart_client_geree_en_caisse
                ],
                temps_final,
                time.time(),
                taille_sprite,
            )

    affichage_fenetre_actions_avec_personnel(fenetre, boutons_actions_employes)

    pygame.display.flip()
    return


def affichage_fenetre_actions_avec_personnel(
    fenetre, boutons_actions_employes
):
    if boutons_actions_employes is not None:
        boutons_actions_employes.Update(fenetre, None)


def affichage_barre_attente(
    fenetre, position, temps_debut, temps_fin, temps_actuel, taille_sprite
):
    long = (
        (temps_actuel - temps_debut) / (temps_fin - temps_debut)
    ) * taille_sprite[0]
    if long <= taille_sprite[0]:
        pygame.draw.rect(
            fenetre,
            (255, 0, 0),
            (
                coordonnees_en_position(position, taille_sprite),
                (long, Constantes.hauteur_barre_chargement),
            ),
        )
        pygame.draw.rect(
            fenetre,
            (0, 0, 0),
            (
                coordonnees_en_position(position, taille_sprite),
                (long, Constantes.hauteur_barre_chargement),
            ),
            2,
        )
    return


def affichage_interface(fenetre, font, temps_horloge):
    sprite_heure = font.render("Time : " + temps_horloge, True, (0, 0, 0))
    affichage_sprites(fenetre, sprite_heure, (0, 0))
    return


def redim_sprite(image, taille_sprite):
    return pygame.transform.scale(image, taille_sprite)


def affichage_fond(fenetre, taille_sprite):
    fond_sol = pygame.image.load(Constantes.sprite_sol)
    fond_mur = pygame.image.load(Constantes.sprite_mur)
    for x in range(Constantes.taille_restaurant[0]):
        for y in range(Constantes.taille_restaurant[1]):
            affichage_sprites(
                fenetre,
                redim_sprite(fond_sol, taille_sprite),
                coordonnees_en_position((x, y), taille_sprite),
            )
            if y < 2:
                affichage_sprites(
                    fenetre,
                    redim_sprite(fond_mur, taille_sprite),
                    (
                        x * taille_sprite[0] + Constantes.larg_cadre_interface,
                        y * taille_sprite[1] - 5,
                    ),
                )
    return


def affichage_joueur(fenetre, temps, joueur, grille, taille_sprite):
    coordonnees = coordonnees_en_position(joueur.position, taille_sprite)
    affichage_sprites(
        fenetre,
        redim_sprite(pygame.image.load(joueur.get_sprite()), taille_sprite),
        (coordonnees[0], coordonnees[1] - 5),
    )
    if joueur.action and joueur.action_liee != "vente":
        affichage_barre_attente(
            fenetre,
            joueur.position,
            joueur.debut_temps_action,
            joueur.debut_temps_action
            + Constantes.delai_gestion_client_en_caisse,
            temps.get_time(),
            taille_sprite,
        )
    return


def affichage_client(fenetre, temps, client, grille, taille_sprite, font):
    coordonnees = coordonnees_en_position(client.position, taille_sprite)
    sprite = redim_sprite(
        pygame.image.load(client.get_sprite()), taille_sprite
    )
    coord_haut_droite_sprite_client = (coordonnees[0], coordonnees[1] - 5)
    affichage_sprites(fenetre, sprite, coord_haut_droite_sprite_client)
    afficher_nom_individu(
        fenetre, font, client, coord_haut_droite_sprite_client, sprite
    )
    if client.test_si_mange():
        if client.coordonnees_objectif == client.position:
            affichage_barre_attente(
                fenetre,
                client.position,
                client.temps_depart_repas,
                client.temps_depart_repas + Constantes.delai_repas_client,
                temps.get_time(),
                taille_sprite,
            )
    return


def afficher_nom_individu(
    fenetre, font, employe, coord_haut_droite_sprite_client, sprite
):
    rect_sprite_client = pygame.Rect(
        coord_haut_droite_sprite_client, sprite.get_rect().size
    )
    if rect_sprite_client.collidepoint(pygame.mouse.get_pos()):
        surface_nom = font.render(employe.nom, True, (0, 0, 0))
        rect = pygame.Rect((0, 0), surface_nom.get_rect().size)
        rect_surface_nom = surface_nom.get_rect()
        rect_surface_nom.midbottom = rect_sprite_client.midtop
        surface_bottom = pygame.Surface((rect.width + 10, rect.height + 10))
        surface_bottom.fill((255, 255, 255))
        surface_bottom.set_alpha(155)
        surface_bottom.blit(surface_nom, (5, 5))
        fenetre.blit(surface_bottom, rect_surface_nom)
    return


def affichage_employe(fenetre, employe, grille, taille_sprite, font):
    coordonnees = coordonnees_en_position(employe.position, taille_sprite)
    sprite = redim_sprite(
        pygame.image.load(employe.get_sprite()), taille_sprite
    )
    coord_haut_droite_sprite_employe = (coordonnees[0], coordonnees[1] - 5)
    affichage_sprites(fenetre, sprite, coord_haut_droite_sprite_employe)
    afficher_nom_individu(
        fenetre, font, employe, coord_haut_droite_sprite_employe, sprite
    )
    if employe.action:
        affichage_barre_attente(
            fenetre,
            employe.position,
            employe.temps_debut_action,
            employe.temps_debut_action + employe.get_temps_action(),
            time.time(),
            taille_sprite,
        )
    return


"""
    #Gestion de la mini_fenetre
"""


def return_commande_1():
    return "commande 1"


def return_commande_2():
    return "commande 2"


def return_quitter_resto():
    return "Aucune"


def get_ingredients_from_biblio(biblio):
    tabl_chaine_caractere = []
    chaine_caractere = ""
    i = 0
    nb_ingredient_sur_la_ligne = 0
    for ingredient in biblio:
        if i < len(biblio) - 1:
            chaine_caractere += (
                ingredient + " = " + str(biblio[ingredient]) + " , "
            )
            nb_ingredient_sur_la_ligne += 1
        else:
            chaine_caractere += ingredient + " = " + str(biblio[ingredient])
        i += 1

        if nb_ingredient_sur_la_ligne == 3:
            nb_ingredient_sur_la_ligne = 0
            tabl_chaine_caractere.append(chaine_caractere)
            chaine_caractere = ""
    tabl_chaine_caractere.append(chaine_caractere)
    return tabl_chaine_caractere


def affichage_infos_recettes(fenetre, font, commande, position_rect, resize):

    surface_texte = font.render(
        "Prix de vente : " + str(commande[1][1]) + "$", True, (0, 0, 0)
    )
    taille_texte = surface_texte.get_size()
    surface_texte = pygame.transform.scale(
        surface_texte,
        (int(taille_texte[0] * resize), int(taille_texte[1] * resize)),
    )
    fenetre.blit(surface_texte, position_rect)
    position_rect = (
        position_rect[0],
        position_rect[1] + surface_texte.get_size()[1] + 5,
    )

    surface_texte = font.render("Ingredients : ", True, (0, 0, 0))
    taille_texte = surface_texte.get_size()
    surface_texte = pygame.transform.scale(
        surface_texte,
        (int(taille_texte[0] * resize), int(taille_texte[1] * resize)),
    )
    fenetre.blit(surface_texte, position_rect)
    position_rect = (
        position_rect[0],
        position_rect[1] + surface_texte.get_size()[1] + 5,
    )

    tabl_ingredients_commande = get_ingredients_from_biblio(commande[1][0])
    for chaine_caractere in tabl_ingredients_commande:
        surface_texte = font.render(chaine_caractere, True, (0, 0, 0))
        taille_texte = surface_texte.get_size()
        surface_texte = pygame.transform.scale(
            surface_texte,
            (int(taille_texte[0] * resize), int(taille_texte[1] * resize)),
        )
        fenetre.blit(surface_texte, position_rect)
        position_rect = (
            position_rect[0],
            position_rect[1] + surface_texte.get_size()[1] + 5,
        )
    return position_rect


def mini_fenetre_commande(restaurant, temps, commandes, fenetre, font):
    """
    ((('grande frite', ({'patate': 3, 'sauce': 1}, 2)),
    ('pizza_baltique', ({'pate_pizza': 1, 'fromage': 1, 'thon': 1, 'creme': 1, 'tomate': 1, 'saumon': 1}, 5.5)))
    , 'algerienne')
    """
    resize = 0.75
    taille_fenetre = fenetre.get_size()
    position_rect = (
        int(taille_fenetre[0] / 2 - 1.5 * Constantes.larg_cadre_interface),
        int(taille_fenetre[1] / 2 - 1.5 * Constantes.larg_cadre_interface),
    )
    larg_rect = (
        4 * Constantes.larg_cadre_interface,
        2 * Constantes.larg_cadre_interface,
    )

    surface_texte = font.render(
        "Gestion de la commande du client :", True, (0, 0, 0)
    )
    pygame.draw.rect(fenetre, (255, 255, 255), (position_rect, larg_rect))
    pygame.draw.rect(fenetre, (0, 0, 0), (position_rect, larg_rect), 2)
    position_rect = (position_rect[0] + 10, position_rect[1] + 10)
    fenetre.blit(surface_texte, position_rect)
    position_rect = (
        position_rect[0],
        position_rect[1] + surface_texte.get_size()[1] + 5,
    )

    boutons = []
    if restaurant.test_ressources_suffisantes(commandes[0][0], commandes[1]):
        couleur_bouton_arg = Constantes.couleur_vert
        actif = True
    else:
        couleur_bouton_arg = Constantes.couleur_rouge
        actif = False
    boutons.append(
        main_fonctions.Bouton(
            font,
            position_rect,
            commandes[0][0][0],
            return_commande_1,
            couleur_bouton=couleur_bouton_arg,
            actif=actif,
        )
    )
    position_rect = (
        position_rect[0],
        position_rect[1] + boutons[0].get_hauteur() + 5,
    )

    position_rect = affichage_infos_recettes(
        fenetre, font, commandes[0][0], position_rect, resize
    )

    if restaurant.test_ressources_suffisantes(commandes[0][1], commandes[1]):
        couleur_bouton_arg = Constantes.couleur_vert
        actif = True
    else:
        couleur_bouton_arg = Constantes.couleur_rouge
        actif = False
    boutons.append(
        main_fonctions.Bouton(
            font,
            position_rect,
            commandes[0][1][0],
            return_commande_2,
            couleur_bouton=couleur_bouton_arg,
            actif=actif,
        )
    )
    position_rect = (
        position_rect[0],
        position_rect[1] + boutons[1].get_hauteur() + 5,
    )

    position_rect = affichage_infos_recettes(
        fenetre, font, commandes[0][1], position_rect, resize
    )

    boutons.append(
        main_fonctions.Bouton(
            font,
            position_rect,
            "Faire sortir le client",
            return_quitter_resto,
            couleur_bouton=(255, 255, 255),
        )
    )
    position_rect = (
        position_rect[0],
        position_rect[1] + boutons[2].get_hauteur() + 5,
    )

    commande_selectionee = None
    temps.set_pause()
    while commande_selectionee is None:
        pos_clic = main_fonctions.get_pos_clic()
        commandes_temp = []
        for bouton in boutons:
            commandes_temp.append(bouton.Update(fenetre, pos_clic))
        for commande_temp in commandes_temp:
            if commande_temp is not None:
                commande_selectionee = commande_temp
        """
        if commande_selectionee != None:
            print()
            print (commande_selectionee)
        """
        pygame.display.flip()
    commande_effective = None
    if commande_selectionee == "commande 1":
        commande_effective = commandes[0][0]
    elif commande_selectionee == "commande 2":
        commande_effective = commandes[0][1]
    temps.set_continuer()
    return commande_effective
