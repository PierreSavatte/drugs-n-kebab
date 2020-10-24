import pygame

from .constantes import Constantes
from .main_fonctions import Slider

"""
taille_case = Constantes.taille_case
decalage_entre_cases = Constantes.decalage_entre_cases
larg_entre_slide = Constantes.larg_entre_slide
x_start = Constantes.x_start
y_start = Constantes.y_start
"""


def affichage_sliders_test(fenetre, font):
    sliders = []
    pos_slider = (40, 20)
    for i in range(10):
        if i == 1:
            val_depart = 100
            sliders.append(
                Slider(
                    (40, 170),
                    val_depart=val_depart,
                    val_max=100,
                    nom_slider="",
                    horizontal_arg=True,
                )
            )
        else:
            val_depart = 0
            sliders.append(
                Slider(
                    pos_slider,
                    val_depart=val_depart,
                    val_max=100,
                    nom_slider="",
                    horizontal_arg=False,
                )
            )
        pos_slider = (pos_slider[0] + 40, pos_slider[1])
    end = False
    while not end:
        fenetre.fill((255, 255, 255))
        for slider in sliders:
            slider.Update(tabl_sliders_lies=sliders)
            slider.afficher(fenetre, font)
        pygame.display.flip()
    return


# def affichage_interface():
#     font = pygame.font.Font("font.ttf", 12)
#     taille_fenetre_developpeur = Constantes.taille_fen
#     if taille_fenetre_developpeur:
#         fenetre = pygame.display.set_mode(taille_fenetre_developpeur)
#
#
# def gestion_outils(fenetre, font, curseurs, mouse):
#     curseur_temp = curseurs[:]
#     tabl_rect_sliders = []
#     for i in range(len(curseurs)):
#         affichage_texte(
#             fenetre,
#             font,
#             Constantes.tableau_couleurs[i][:6],
#             (pos_col(i)[0], 5),
#         )
#         rect = pygame.Rect(
#             pos_col(i), (Constantes.taille_slide_x, Constantes.taille_slide_y)
#         )
#         pygame.draw.rect(fenetre, (0, 0, 0), rect, 1)
#         pygame.draw.rect(
#             fenetre,
#             (0, 0, 0),
#             (
#                 percent_to_pos(curseurs[i], i),
#                 (Constantes.taille_curseur_x, Constantes.taille_curseur_y),
#             ),
#         )
#         tabl_rect_sliders.append(rect)
#
#     if mouse != None:
#         j = 0
#         for rect in tabl_rect_sliders:
#             if rect.collidepoint(mouse):
#                 nouvelle_val = pos_to_percent(mouse)
#                 ancienne_val = curseur_temp[j]
#                 difference = nouvelle_val - ancienne_val
#                 if nouvelle_val != ancienne_val:
#                     curseur_temp[j] = nouvelle_val
#                     curseurs_modifiables = []
#                     modif_temp = -difference / (len(curseur_temp) - 1)
#                     for i in range(len(curseurs)):
#                         val_temp_i = curseur_temp[i] + modif_temp
#                         if val_temp_i >= 0 and val_temp_i <= 100:
#                             curseurs_modifiables.append(i)
#                     modif_pour_autres_curseurs = -difference / (
#                         len(curseurs_modifiables)
#                     )
#                     for j in curseurs_modifiables:
#                         curseur_temp[j] += modif_pour_autres_curseurs
#             j += 1
#     return curseur_temp
#
#
# def parcourir_bibliotheque_et_ajouter_stats(fenetre, font):
#     biblio = Constantes.villes
#     nombre_faits = 0
#     for nom_ville in biblio:
#         biblio_ville = {}
#         curseurs = [25, 25, 25, 25, 0, 0, 0, 0, 0, 0]
#         end = False
#         while not (end):
#             fenetre.fill((255, 255, 255))
#             affichage_texte(fenetre, font, nom_ville + " : ", (5, 5))
#             affichage_texte(
#                 fenetre,
#                 font,
#                 str(int(nombre_faits / len(biblio) * 100)) + " %",
#                 (15, 25),
#             )
#             mouse = get_pos_clic()
#             curseurs = gestion_outils(fenetre, font, curseurs, mouse)
#             pygame.display.flip()
#             somme = 0
#             for i in range(len(curseurs)):
#                 somme += curseurs[i]
#             clavier = get_clavier()
#             if clavier == pygame.K_SPACE:
#                 end = True
#         biblio_ville["taille_ville"] = (20, 20)
#         i = 0
#         for couleur in Constantes.tableau_couleurs:
#             print(couleur)
#             biblio_ville[couleur] = int(curseurs[i])
#             i += 1
#         biblio[nom_ville] = biblio_ville
#         print(nom_ville + " : ")
#         print(biblio[nom_ville])
#         nombre_faits += 1
#     return biblio
