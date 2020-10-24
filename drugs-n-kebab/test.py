import pygame
from .constantes import Constantes
from . import time_DnK
from . import main_fonctions
import math

"""def k_puissance_p(k,p):
    puissance = 1 
    for i in range(p):
        puissance = puissance* k
    return puissance

print(k_puissance_p(2, 8))"""

"""tabl= [0,0,0,0,0,0,0,0]
print(len(tabl))
compteur = 0
for i in range(len(tabl)):
    compteur +=1
    break
print(compteur)
compteur =0
while compteur < len(tabl):
    compteur+=1
print(compteur)"""

"""class Test:
    
    compteur_2 = 0
    
    
    def __init__(self):
        self.compteur = 1
        self.compteur += 1
        Test.compteur_2 += 1
        return

for i in range(5):
    objet = Test()
    print(objet.compteur)

print(Test.compteur_2)"""


def Affichage(a):
    if type(a) == type(1):
        print("Entier : " +str(a))
    return 

def Affichage(a):
    if type(a) == type(.1):
        print("Flotant : " +str(a))
    return 


Affichage(2)