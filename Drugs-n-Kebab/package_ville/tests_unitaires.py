import sys
import os
import pygame

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)
import affichage
import generation_ville
import ville_test


pygame.font.init()
font = pygame.font.Font('font.ttf', 12)

affichage.affichage_ville(font,generation_ville.gen_ville())