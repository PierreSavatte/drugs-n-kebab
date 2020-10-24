import pygame
from constantes import Constantes
#from interface_devellopeur_map_monde import parcourir_bibliotheque_et_ajouter_stats
import main_fonctions
from interface_devellopeur_map_monde import affichage_sliders_test
from affichage_map_monde import affichage_map
import generation_logo
import time_DnK
from tkinter.constants import END

pygame.display.init()
fenetre = pygame.display.set_mode(Constantes.taille_fen)
pygame.font.init()
font = pygame.font.Font('font.ttf', 12)

"""
    Test interface_devellopeur_map_monde
"""
"""
#print(parcourir_bibliotheque_et_ajouter_stats(fenetre,font))
#affichage_sliders_test(fenetre,font)
temps = time_DnK.Time()
affichage_map(fenetre,temps)
"""
"""
    Test generation_logo
"""
"""
pygame.init()
fenetre = pygame.display.set_mode((500,500))
sprite_logo = generation_logo.main_loop(fenetre)
fenetre.fill((0,0,0))
fenetre.blit(pygame.transform.scale(sprite_logo, (200, 200)),(0,0))
pygame.display.flip()

"""
"""
    Test main fonctions
"""

def test_1():
    print("test_1")
    return 

def test_2():
    print("test_2")
    return 

def test_3():
    print("test_3")
    return
def test_3_qskdnqlskdnf():
    print("test_3")
    return 

menu = main_fonctions.Menu_Deroulant(font,(5,5),'NOM',[test_1,test_2,test_3,test_3_qskdnqlskdnf])
end = True
while end:
    fenetre.fill((255,255,255))
    pos_mouse_clic = main_fonctions.get_pos_clic()
    pos_mouse = main_fonctions.get_pos_mouse()
    menu.Update(fenetre,pos_mouse_clic,pos_mouse)
    pygame.display.flip()

pygame.time_DnK.wait(20000)



"""
rect_saisie = main_fonctions.Rect_Saisie((10,10),0,100)
end = True
while end:
    fenetre.fill((255,255,255))
    pos_mouse_clic = main_fonctions.get_pos_clic()
    pos_mouse = main_fonctions.get_pos_mouse()
    rect_saisie.Update(fenetre,font,pos_mouse)
    pygame.display.flip()
"""
"""
    Test time_DnK
"""
"""
temps = time_DnK.Time()

temps.get_time()
end = True
while end : 
    clavier = main_fonctions.get_clavier()
    if clavier == pygame.K_SPACE:
        if temps.est_en_pause():
            temps.set_continuer()
        else:
            temps.set_pause()
    print((temps.est_en_pause(),temps.decalage,temps.get_temps_horloge()))
"""
