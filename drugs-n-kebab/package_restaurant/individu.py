from pathfinding_A_etoile import pathfinding
from constantes import Constantes
import main_fonctions
import random
import time_DnK

class Individu:
    
    tabl_positions = []
    
    def __init__(self,couleur_argument,sexe_arg):
        self.couleur = couleur_argument
        self.sexe = sexe_arg
        (self.nom,self.sprites) = self.get_nom()
        self.position = Constantes.spawn_restaurant
        self.orientation = "UP"
        self.orientation_but = "UP"
        self.chemin = []
        self.objectif = 'Aucun'
        self.coordonnees_objectif = None
        
        self.indice_tabl_positions = len(Individu.tabl_positions)
        Individu.tabl_positions.append(self.position)
        return
    
    def MAJ_pos_tabl_positions(self):
        Individu.tabl_positions[self.indice_tabl_positions] = self.position
        return
    
    def clean_objectifs(self):
        self.objectif = None
        self.coordonnees_objectif = None
        return
    
    def get_nom(self):
        nom = None
        nom_sprite = ""
        sprites = []
        if self.couleur in Constantes.tableau_couleurs:
            if self.couleur == Constantes.nom_arabes:
                if self.sexe == Constantes.nom_femme:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_femme_arabes)
                else:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_homme_arabes)
                sprites = self.get_tabl_sprite(Constantes.nom_noir)
            elif self.couleur == Constantes.nom_asiats:
                if self.sexe == Constantes.nom_femme:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_femme_asiats)
                else:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_homme_asiats)
                sprites = self.get_tabl_sprite(Constantes.nom_asiats)
            elif self.couleur == Constantes.nom_blanc:
                if self.sexe == Constantes.nom_femme:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_femme_blanc)
                else:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_homme_blanc)
                sprites = self.get_tabl_sprite(Constantes.nom_blanc)
            elif self.couleur == Constantes.nom_noir:
                if self.sexe == Constantes.nom_femme:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_femme_noir)
                else:
                    nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_homme_noir)
                sprites = self.get_tabl_sprite(Constantes.nom_noir)
            else:
                #attribution secondaire
                self.couleur = Constantes.nom_blanc
                nom = main_fonctions.get_val_aleatoire_parmis(Constantes.tableau_noms_homme_blanc)
                sprites = self.get_tabl_sprite(Constantes.nom_blanc)
        return (nom,sprites)
    
    def get_tabl_sprite(self,constante_race):
        sprites = []
        nom_sprite = "Sprites/"+constante_race+'_'+self.sexe+'_1_'
        for orientation in ["up","down","right","left"]:
            sprites.append(nom_sprite+orientation+".png")
        return sprites
    
    def avancer_d_un_pas(self):
        (x,y) = self.position
        self.position = (x,y-1)
        self.orientation = "UP"
        return
    
    def test_despawn(self,grille):
        (x,y) = self.position
        return (grille[x][y][Constantes.nom_biblio_sprite] == Constantes.sprite_tapis_1)
    
    def get_liste_pos_clients(self,liste_clients):
        liste = []
        for client in liste_clients:
            liste.append(client.position)
        return liste
    
    def deplacer(self,restaurant,liste_pos_clients):
        if len(self.chemin) != 0:
            position_precedente = self.position
            position_suivante= self.chemin[0]
            if not((position_suivante[0],position_suivante[1]) in liste_pos_clients):
                self.position = position_suivante
                if position_precedente[0] < self.position[0]:
                    self.orientation = 'RIGHT'
                elif position_precedente[0] > self.position[0] :
                    self.orientation = 'LEFT'
                else:
                    if position_precedente[1] < self.position[1]:
                        self.orientation = 'DOWN'
                    else:
                        self.orientation = 'UP'
                self.chemin.pop(0)
            if len(self.chemin) == 0:
                (x,y) = self.position
                case = restaurant.grille_meubles[x][y]
                case[Constantes.nom_biblio_est_objectif] = False
                self.put_bonne_orientation(case)
        self.MAJ_pos_tabl_positions()
        return
    
    def put_bonne_orientation(self,case):
        """
        Constantes : 
        sprites_chaise = [sprite_chaise_up,sprite_chaise_down,sprite_chaise_left,sprite_chaise_right]
        """
        orientation = ['UP','DOWN','LEFT','RIGHT']
        (x,y) = self.position
        nom_sprite = case[Constantes.nom_biblio_sprite]
        if nom_sprite in Constantes.sprites_chaise:
            for i in range(0,len(Constantes.sprites_chaise)):
                if nom_sprite == Constantes.sprites_chaise[i]:
                    self.orientation = orientation[i]
                    return
        else:
            self.orientation = self.orientation_but
    
    def set_position_but(self,restaurant,but,liste_position_personnages,est_personnel):
        self.coordonnees_objectif = None
        objectif_trouve = False
        for x in range(len(restaurant.grille_meubles)):
            for y in range(len(restaurant.grille_meubles[0])):
                if not(objectif_trouve):
                    if but ==  Constantes.sprite_tapis_1:
                        if restaurant.grille_meubles[x][y][Constantes.nom_biblio_sprite] == Constantes.sprite_tapis_1:
                            self.coordonnees_objectif = (x,y)
                            self.orientation_but = 'DOWN'
                            objectif_trouve = True
                    elif but ==  Constantes.sprite_chaise_left:
                        if restaurant.grille_meubles[x][y][Constantes.nom_biblio_sprite] in Constantes.sprites_chaise:
                            if not(restaurant.grille_meubles[x][y][Constantes.nom_biblio_est_objectif]):
                                if not((x,y) in liste_position_personnages):
                                    restaurant.grille_meubles[x][y][Constantes.nom_biblio_est_objectif] = True
                                    self.coordonnees_objectif = (x,y)
                                    objectif_trouve = True
                    elif but ==  Constantes.sprite_caisse:
                        if restaurant.grille_meubles[x][y][Constantes.nom_biblio_sprite] == Constantes.sprite_caisse:
                            if est_personnel :
                                self.coordonnees_objectif = (x,y-1)
                                self.orientation_but = 'DOWN'
                                objectif_trouve = True
                            else:
                                self.coordonnees_objectif = (x,y+1)
                                self.orientation_but = 'UP'
                                objectif_trouve = True
                    elif but ==  Constantes.sprite_machine_kebab_1:
                        if restaurant.grille_meubles[x][y][Constantes.nom_biblio_sprite] == Constantes.sprite_machine_kebab_1:
                            self.coordonnees_objectif = (x,y+1)
                            self.orientation_but = 'UP'
                            objectif_trouve = True
        return
    
    def test_set_objectif(self,pos,grille_meubles,liste_position_personnages):
        test = False
        (x,y) = pos
        if not((x,y) in liste_position_personnages):
            grille_meubles[x][y][Constantes.nom_biblio_est_objectif] = True
            self.coordonnees_objectif = (x,y)
            test = True
        return test
    
    def modifier_chemin(self,restaurant,but,liste_position_personnages,est_personnel = False):
        if self.coordonnees_objectif == None:
            self.set_position_but(restaurant,but,liste_position_personnages,est_personnel)
            if self.coordonnees_objectif == None:
                return False
        if self.coordonnees_objectif != None:
            if self.position != self.coordonnees_objectif:
                if self.objectif == Constantes.sprite_caisse:
                    self.chemin = pathfinding(restaurant.grille_meubles,self.position,self.coordonnees_objectif,[])
                else:
                    self.chemin = pathfinding(restaurant.grille_meubles,self.position,self.coordonnees_objectif,liste_position_personnages)
        else:
            self.chemin = [self.position]
            """print(self)
            print('Ne bouge plus')"""
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