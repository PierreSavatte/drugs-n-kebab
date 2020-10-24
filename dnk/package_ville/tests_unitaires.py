import os
import sys

import pygame

from . import affichage, generation_ville

DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_PARENT)

pygame.font.init()
font = pygame.font.Font("font.ttf", 12)

affichage.affichage_ville(font, generation_ville.gen_ville())
