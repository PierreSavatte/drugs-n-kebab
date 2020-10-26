import pygame

from .constants import Constantes
from .main_fonctions import get_clavier


def coord_to_pos(coord):
    return (
        coord[0] * (Constantes.taille_case + Constantes.decalage_entre_cases)
        + Constantes.x_start,
        coord[1] * (Constantes.taille_case + Constantes.decalage_entre_cases)
        + Constantes.y_start,
    )


def pos_col(num_col):
    return (
        Constantes.x_tabl_max
        + (Constantes.decalage_entre_cases + Constantes.larg_entre_slide)
        * (num_col - 1)
        + ((1 / 2) * Constantes.larg_entre_slide - Constantes.taille_slide_x)
        * num_col,
        Constantes.y_start,
    )


def pos_saisie_col(num_col):
    return (
        Constantes.x_tabl_max
        - 0.5 * Constantes.taille_slide_x
        + Constantes.decalage_entre_cases * num_col
        + (Constantes.larg_entre_slide + Constantes.taille_slide_x * 0.5)
        * (num_col - 1),
        Constantes.y_start_saisie_couleur,
    )


def couleur_to_pos(couleur, num_col):
    x = (
        pos_col(num_col)[0]
        - (Constantes.taille_curseur_x - Constantes.taille_slide_x) / 2
    )
    y = (
        (-(couleur / 255) + 1) * Constantes.taille_slide_y
        + Constantes.y_start
        - (0.5 * Constantes.taille_curseur_y)
    )
    return (x, y)


def pos_to_couleur(pos):
    y = pos[1]
    return int(
        ((-(y - Constantes.y_start) / Constantes.taille_slide_y) + 1) * 255
    )


def pos_to_coord(pos):
    return (
        (pos[0] - Constantes.x_start)
        / (Constantes.taille_case + Constantes.decalage_entre_cases),
        (pos[1] - Constantes.y_start)
        / (Constantes.taille_case + Constantes.decalage_entre_cases),
    )


def gest_grille_vide():
    tabl = []
    for x in range(Constantes.taille_logo[0]):
        ligne_tabl = []
        for y in range(Constantes.taille_logo[1]):
            ligne_tabl.append([255, 255, 255])
        tabl.append(ligne_tabl)
    return tabl


def get_mouse():
    pygame.event.get()
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return event.pos
    """
    tabl_get_pressed = pygame.mouse.get_pressed()
    tabl_return = []
    for case in tabl_get_pressed:
        tabl_return.append(case == 1)
    return (tabl_return, pygame.mouse.get_pos())


def dessiner_grille(fenetre, grille, mouse, color_curseurs, color_gomme):
    for y in range(len(grille)):
        for x in range(len(grille[0])):
            rect = pygame.Rect(
                coord_to_pos((x, y)),
                (Constantes.taille_case, Constantes.taille_case),
            )

            if mouse[0][0]:
                if rect.collidepoint(mouse[1]):
                    grille[x][y] = color_curseurs
            if mouse[0][2]:
                if rect.collidepoint(mouse[1]):
                    grille[x][y] = color_gomme
            pygame.draw.rect(fenetre, grille[x][y], rect)
            pygame.draw.rect(fenetre, (0, 0, 0), rect, 1)
    return


def decaler_rect(rect):
    return (rect[0] + 1, rect[1] + 1, rect[2] - 1, rect[3] - 1)


def afficher_saisie(fenetre, font, valeur, num_col):
    pos = pos_saisie_col(num_col)
    surface = font.render(str(valeur), False, (0, 0, 0))
    pygame.draw.rect(
        fenetre,
        (255, 255, 255),
        (
            pos,
            (Constantes.larg_entre_slide, Constantes.taille_saisie_couleur_y),
        ),
    )
    pygame.draw.rect(
        fenetre,
        Constantes.couleur_gris,
        decaler_rect(
            (
                pos[0],
                pos[1],
                Constantes.larg_entre_slide,
                Constantes.taille_saisie_couleur_y,
            )
        ),
        1,
    )
    pygame.draw.rect(
        fenetre,
        (0, 0, 0),
        (
            pos,
            (Constantes.larg_entre_slide, Constantes.taille_saisie_couleur_y),
        ),
        1,
    )
    fenetre.blit(surface, (pos[0] + 2, pos[1] + 2))
    return


def saisie(fenetre, font, val_curseur, k):
    mouse = get_mouse()
    key = get_clavier()
    chaine_saisie = str(val_curseur)
    while (
        not (mouse[0][0])
        and (key != pygame.K_RETURN)
        and (key != pygame.K_KP_ENTER)
    ):
        afficher_saisie(fenetre, font, chaine_saisie + "|", k + 1)
        key = get_clavier()
        if key == pygame.K_BACKSPACE:
            chaine_saisie = chaine_saisie[:-1]
        if len(chaine_saisie) < 3:
            if key == pygame.K_KP0:
                chaine_saisie += "0"
            elif key == pygame.K_KP1:
                chaine_saisie += "1"
            elif key == pygame.K_KP2:
                chaine_saisie += "2"
            elif key == pygame.K_KP3:
                chaine_saisie += "3"
            elif key == pygame.K_KP4:
                chaine_saisie += "4"
            elif key == pygame.K_KP5:
                chaine_saisie += "5"
            elif key == pygame.K_KP6:
                chaine_saisie += "6"
            elif key == pygame.K_KP7:
                chaine_saisie += "7"
            elif key == pygame.K_KP8:
                chaine_saisie += "8"
            elif key == pygame.K_KP9:
                chaine_saisie += "9"
            if chaine_saisie != "":
                if int(chaine_saisie) > 255:
                    chaine_saisie = "255"
        mouse = get_mouse()
        pygame.display.flip()
    return int(chaine_saisie)


def gestion_outils(
    fenetre, font, curseurs, color_gomme, mouse, sprites, grille
):
    curseur_temp = curseurs[:]
    tabl_rect_sliders = []
    tabl_rect_saisie = []
    for i in range(1, 4, 1):
        color = [0, 0, 0]
        color[i - 1] = curseurs[i - 1]
        rect = pygame.Rect(
            pos_col(i), (Constantes.taille_slide_x, Constantes.taille_slide_y)
        )
        pygame.draw.rect(fenetre, (0, 0, 0), rect, 1)
        pygame.draw.rect(
            fenetre,
            color,
            (
                couleur_to_pos(curseurs[i - 1], i),
                (Constantes.taille_curseur_x, Constantes.taille_curseur_y),
            ),
        )
        tabl_rect_sliders.append(rect)

        rect = pygame.Rect(
            pos_saisie_col(i),
            (Constantes.larg_entre_slide, Constantes.taille_saisie_couleur_y),
        )
        pygame.draw.rect(fenetre, (255, 0, 0), rect, 1)
        tabl_rect_saisie.append(rect)

        afficher_saisie(fenetre, font, curseur_temp[i - 1], i)

    rect_bouton_fleche = pygame.Rect(
        Constantes.x_start_bouton_fleche,
        Constantes.y_start_bouton_fleche,
        Constantes.taille_boutons,
        Constantes.taille_boutons,
    )
    rect_bouton_pipette = pygame.Rect(
        (
            coord_to_pos((Constantes.taille_logo[0] + 1, 0))[0]
            + Constantes.taille_couleur_x
            + Constantes.decalage_entre_cases,
            Constantes.y_start_carre_couleur_1
            + 0.5 * Constantes.taille_couleur_y
            - 0.5 * Constantes.taille_boutons,
        ),
        (Constantes.taille_boutons, Constantes.taille_boutons),
    )

    rect_couleur_1 = (
        (
            coord_to_pos((Constantes.taille_logo[0] + 1, 0))[0],
            Constantes.y_start_carre_couleur_1,
        ),
        (Constantes.taille_couleur_x, Constantes.taille_couleur_y),
    )
    rect_couleur_2 = (
        (
            coord_to_pos((Constantes.taille_logo[0] + 1, 0))[0],
            Constantes.y_start_carre_couleur_2,
        ),
        (Constantes.taille_couleur_x, Constantes.taille_couleur_y),
    )
    pygame.draw.rect(fenetre, curseurs, rect_couleur_1)
    pygame.draw.rect(fenetre, (0, 0, 0), rect_couleur_1, 1)
    fenetre.blit(sprites[0], rect_bouton_pipette)
    fenetre.blit(sprites[1], rect_bouton_fleche)
    pygame.draw.rect(fenetre, color_gomme, rect_couleur_2)
    pygame.draw.rect(fenetre, (0, 0, 0), rect_couleur_2, 1)

    if mouse[0][0]:
        j = 0
        for rect in tabl_rect_sliders:
            if rect.collidepoint(mouse[1]):
                curseur_temp[j] = pos_to_couleur(mouse[1])
            j += 1
        k = 0
        for rect in tabl_rect_saisie:
            if rect.collidepoint(mouse[1]):
                curseur_temp[k] = saisie(fenetre, font, curseur_temp[k], k)
            k += 1

        if rect_bouton_fleche.collidepoint(mouse[1]):
            color_gomme = curseurs

        if rect_bouton_pipette.collidepoint(mouse[1]):
            pygame.time.wait(300)
            mouse = get_mouse()
            pygame.draw.rect(fenetre, (255, 0, 0), rect_bouton_pipette, 1)
            pygame.display.flip()
            while not (mouse[0][0]) and not (mouse[0][2]):
                mouse = get_mouse()
            for x in range(len(grille[0])):
                for y in range(len(grille)):
                    rect = pygame.Rect(
                        coord_to_pos((x, y)),
                        (Constantes.taille_case, Constantes.taille_case),
                    )
                    if rect.collidepoint(mouse[1]) and mouse[0][0]:
                        curseur_temp = grille[x][y]
                    if rect.collidepoint(mouse[1]) and mouse[0][2]:
                        color_gomme = grille[x][y]
            pygame.time.wait(1)
    return (curseur_temp, color_gomme)


def post_processing(grille):
    taille_x = len(grille)
    taille_y = len(grille[0])
    surface = pygame.Surface((taille_x, taille_y))
    for x in range(taille_x):
        for y in range(taille_y):
            surface.set_at((x, y), grille[x][y])
    return surface


def main_loop(fenetre):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 15)
    grille = gest_grille_vide()
    curseurs = [0, 0, 0]
    color_gomme = [255, 255, 255]
    sprites = (
        pygame.image.load(Constantes.sprite_pipette),
        pygame.image.load(Constantes.sprite_fleche),
    )
    sprite_bouton_save = pygame.image.load(Constantes.sprite_quit)
    rect_bouton_save = pygame.Rect(
        coord_to_pos((0, len(grille[0]) + 1)),
        sprite_bouton_save.get_rect().size,
    )
    end = False
    while not (end):
        fenetre.fill((255, 255, 255))
        mouse = get_mouse()
        dessiner_grille(fenetre, grille, mouse, curseurs, color_gomme)
        (curseurs, color_gomme) = gestion_outils(
            fenetre, font, curseurs, color_gomme, mouse, sprites, grille
        )
        fenetre.blit(sprite_bouton_save, rect_bouton_save)
        if mouse[0][0]:
            if rect_bouton_save.collidepoint(mouse[1]):
                end = True
        pygame.display.flip()
    return post_processing(grille)
