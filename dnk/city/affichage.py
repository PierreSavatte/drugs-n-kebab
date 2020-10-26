import pygame

from .groupe_sprite import Groupe_sprite
from .. import main_fonctions
from ..constants import Constantes


def coordonnees_en_position(coordonnees):
    (x, y) = coordonnees
    return (
        (x - y) * (1 / 2 * Constantes.taille_sprite_ville_x)
        + 1 / 2 * Constantes.taille_fen[0],
        (y + x) * (1 / 2 * Constantes.taille_sprite_ville_y + 0.5)
        + Constantes.taille_sprite_ville_y,
    )


def position_en_coordonnees(position):
    (x, y) = position
    return (
        int(
            (
                (1 / 2 * Constantes.taille_fen[0])
                / Constantes.taille_sprite_ville_x
            )
            - (x / Constantes.taille_sprite_ville_x)
            + (3 / (Constantes.taille_sprite_ville_y + 1)) * y
        )
        - 2,
        int(
            -(
                x * (1 / Constantes.taille_sprite_ville_x)
                - (1 / (Constantes.taille_sprite_ville_y + 1)) * y
                - (
                    (1 / 2 * Constantes.taille_fen[0])
                    / Constantes.taille_sprite_ville_x
                )
                - Constantes.taille_sprite_ville_y
                / (1 / 2 * Constantes.taille_sprite_ville_y + 0.5)
            )
        )
        - 2,
    )


def add_sprites_sol(groupe):
    for x in range(Constantes.taille_ville[0] + 1):
        for y in range(Constantes.taille_ville[1] + 1):
            add_sprite(
                groupe, [Constantes.nom_sprite_terrain], (x, y), sol=True
            )
    return


def add_sprites_batiments(ville, groupe):
    for x in range(Constantes.taille_ville[0] + 1):
        for y in range(Constantes.taille_ville[1] + 1):
            if ville[x][y] is not None:
                add_sprite(groupe, ville[x][y], (x, y))


def add_sprite(groupe, objet_batiment, coordonnees, sol=False):
    nom_sprites = objet_batiment[0]
    image_sprite = pygame.image.load(nom_sprites)
    taille_image = image_sprite.get_rect().size
    image_sprite = image_sprite.convert()

    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface(taille_image)
    sprite.image.set_colorkey((0, 0, 0))

    sprite.image.blit(image_sprite, ((0, 0), taille_image))
    sprite.rect = sprite.image.get_rect()
    position = coordonnees_en_position(coordonnees)

    sprite.rect.midleft = (
        position[0],
        position[1]
        - 1 / 2 * (taille_image[1] - Constantes.taille_sprite_ville_y),
    )
    if sol:
        groupe.add(sprite)
    else:
        groupe.add(sprite, objet_batiment, coordonnees)

    return


def create_groupe_batiment():
    return Groupe_sprite()


def create_groupe_sol():
    return pygame.sprite.OrderedUpdates()


def applique_deplacement(rect, tabl_deplacement):
    return pygame.Rect(
        rect.left + tabl_deplacement[0],
        rect.top + tabl_deplacement[1],
        rect.width,
        rect.height,
    )


def gest_deplacement_map(
    fenetre,
    groupe_sol,
    groupe_batiment,
    temps_dernier_mvt,
    acceleration,
    old_mouvement,
):
    orientation_mouvement = main_fonctions.get_orientation_mouvement()
    if old_mouvement == orientation_mouvement:
        acceleration += Constantes.aceleration_mouvement_ville
    else:
        acceleration = Constantes.vitesse_mouvement_ville_0
    old_mouvement = orientation_mouvement
    (tabl_deplacement, temps_dernier_mvt) = main_fonctions.get_rect_mouvement(
        orientation_mouvement, temps_dernier_mvt, acceleration
    )
    for groupe in [groupe_sol, groupe_batiment]:
        if groupe == groupe_sol:
            sprites = groupe.sprites()
        else:
            sprites = groupe.groupe.sprites()
        for sprite in sprites:
            sprite.rect = applique_deplacement(sprite.rect, tabl_deplacement)
    return temps_dernier_mvt, old_mouvement, acceleration


def gest_mouse(fenetre, font, ville, groupe_batiment):
    pos_mouse = pygame.mouse.get_pos()
    batiment = None
    groupe_sprites = groupe_batiment.groupe.sprites()
    for i in range(len(groupe_sprites)):
        sprite = groupe_sprites[i]
        if sprite.rect.collidepoint(pos_mouse):
            stat_bat = groupe_batiment.get_stat_batiment(sprite)
            est_bat_deco = stat_bat[0] in Constantes.noms_sprites_deco
            if not est_bat_deco:
                batiment = sprite
                coloriser_batiment(fenetre, sprite)
                affichage_mini_fenetre_info(
                    fenetre,
                    font,
                    (pos_mouse[0] + 10, pos_mouse[1] + 10),
                    stat_bat,
                )
                break

    if pygame.mouse.get_pressed()[0]:
        if batiment is not None:
            position = groupe_batiment.get_pos_tabl(batiment)
            ville[position[0]][position[1]][1][Constantes.stat_achete] = True
    return


def coloriser_batiment(fenetre, sprite):
    image_a_afficher = pygame.Surface(sprite.image.get_size())
    x_max = image_a_afficher.get_width()
    y_max = image_a_afficher.get_height()
    for x in range(x_max):
        for y in range(y_max):
            color = sprite.image.get_at((x, y))
            image_a_afficher.set_at((x, y), main_fonctions.highlight(color))
    image_a_afficher.set_colorkey((50, 50, 50))
    fenetre.blit(image_a_afficher, sprite.rect.topleft)
    return


def affichage_mini_fenetre_info(fen, font, pos, batiment):
    if batiment is not None:
        if not (batiment[0] in Constantes.noms_sprites_deco):
            font_height = font.size("")[1]
            textes = []
            long_max = 0
            for stat in batiment[1]:
                # if stat != Constantes.stat_achete:
                texte = font.render(
                    str(stat) + " = " + str(batiment[1][stat]),
                    False,
                    (0, 0, 0),
                )
                textes.append(texte)
                long_texte = texte.get_width()
                if long_texte > long_max:
                    long_max = long_texte
            i = 0
            rect = (
                pos,
                (long_max + 10, (len(textes) + 0.5) * font_height + 10),
            )
            pygame.draw.rect(fen, (245, 245, 220), rect)
            pygame.draw.rect(fen, (0, 0, 0), rect, 1)
            for i in range(len(textes)):
                fen.blit(textes[i], (pos[0] + 5, pos[1] + 5 + i * font_height))


def draw_groupes(fenetre, groupe_sol, groupe_batiment):
    for groupe in [groupe_sol, groupe_batiment]:
        groupe.draw(fenetre)


def affichage_ville(font, ville):
    pygame.init()
    fenetre = pygame.display.set_mode(Constantes.taille_fen)
    pygame.key.set_repeat(50, 50)

    groupe_sol = create_groupe_sol()
    groupe_batiment = create_groupe_batiment()

    add_sprites_sol(groupe_sol)
    add_sprites_batiments(ville, groupe_batiment)

    temps_dernier_mvt = 0
    acceleration = Constantes.vitesse_mouvement_ville_0
    old_mouvement = None

    end = False
    while not end:
        fenetre.fill((255, 255, 255))
        draw_groupes(fenetre, groupe_sol, groupe_batiment)
        (
            temps_dernier_mvt,
            old_mouvement,
            acceleration,
        ) = gest_deplacement_map(
            fenetre,
            groupe_sol,
            groupe_batiment,
            temps_dernier_mvt,
            acceleration,
            old_mouvement,
        )
        gest_mouse(fenetre, font, ville, groupe_batiment)
        pygame.display.flip()
