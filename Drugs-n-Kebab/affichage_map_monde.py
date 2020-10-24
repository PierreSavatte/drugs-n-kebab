from constantes import Constantes
import pygame
import main_fonctions
import time
import random
import math
import interface_devellopeur_map_monde

def recolore_main_color(sprite,couleur_arrivee):
    couleur_a_changer = main_fonctions.get_main_color(sprite)
    return main_fonctions.recolore(sprite,couleur_a_changer,couleur_arrivee)

def redim_sprite_dim_fenetre(sprite,dimensions_fenetre):
    dimensions_sprite = sprite.get_size()
    rapports =(dimensions_fenetre[0]*1.0/dimensions_sprite[0],dimensions_fenetre[1]*1.0/dimensions_sprite[1])
    if rapports[0] < 1 or rapports[1] < 1:
        rapport = min(rapports[0],rapports[1])
        dimensions_sprite_prime = (int(rapport*dimensions_sprite[0]),int(rapport*dimensions_sprite[1]))
        return pygame.transform.scale(sprite, dimensions_sprite_prime)
    else:
        return sprite

def add_city_with_click(bibliotheque):
    pos = main_fonctions.get_pos_clic()
    if (pos != None) : 
        new_pos = (pos[0]-5,pos[1]-5)
        nom = raw_input("Nom de la ville : ")
        bibliotheque[nom] = new_pos
    return (pos != None)

def draw_mini_fenetre(fenetre,font,pos_rect,nom_ville):
    surface_texte = font.render(nom_ville, True, (0,0,0))
    hauteur_rect = surface_texte.get_height()+4
    pos_rect_prime = (pos_rect[0],pos_rect[1]-hauteur_rect)
    size_rect = (surface_texte.get_width()+4,hauteur_rect)
    pygame.draw.rect(fenetre, (255,255,255), (pos_rect_prime,size_rect))
    pygame.draw.rect(fenetre, (0,0,0), (pos_rect_prime,size_rect), 1)
    fenetre.blit(surface_texte,(pos_rect_prime[0]+2,pos_rect_prime[1]+2))
    return

def gest_mouse(fenetre,font,bibliotheque_villes):
    pos_mouse = main_fonctions.get_pos_mouse()
    for nom_ville in bibliotheque_villes:
        pos_ville = bibliotheque_villes[nom_ville]
        rect_bouton_ville = pygame.Rect(pos_ville,Constantes.taille_sprite_point)
        if rect_bouton_ville.collidepoint(pos_mouse):
            draw_mini_fenetre(fenetre,font,pos_mouse,nom_ville)
    return

def get_tabl_nom_villes(bibliotheque_villes):
    tabl = []
    for ville in bibliotheque_villes:
        tabl.append(ville)
    return tabl

def gest_vehicule(fenetre,font,bibliotheque_villes,tabl_vehicule,temps):
    if random.randint(0,100)>=98 and not(temps.est_en_pause()):
        tabl_nom_villes = get_tabl_nom_villes(bibliotheque_villes)
        ville_depart = main_fonctions.get_val_aleatoire_parmis(tabl_nom_villes)
        ville_fin = main_fonctions.get_val_aleatoire_parmis(tabl_nom_villes)
        while ville_fin == ville_depart:
            ville_fin = main_fonctions.get_val_aleatoire_parmis(tabl_nom_villes)
        nom_ligne = ville_depart+' - '+ville_fin
        tabl_vehicule.append(Vehicule(nom_ligne,bibliotheque_villes[ville_depart],bibliotheque_villes[ville_fin],Constantes.sprite_avion,temps))
    indice_vehicule = 0
    for vehicule in tabl_vehicule:
        fenetre.blit(vehicule.sprite, vehicule.get_postion(temps))
        #pygame.draw.rect(fenetre, (0,0,0), (vehicule.get_postion(),(12,12)))
        if vehicule.test_fin_deplacement():
            tabl_vehicule.pop(indice_vehicule)
        indice_vehicule += 1
        vehicule.gest_affichage_info(main_fonctions.get_pos_mouse(),fenetre,font)
    return tabl_vehicule

def affichage_temps(fenetre,temps,affichage_pause,temps_affichee):
    temps_a_afficher = temps.get_temps_horloge()
    surface_temps = pygame.font.Font('font.ttf', 20).render(temps_a_afficher, True, (0,0,0))
    fenetre.blit(surface_temps,(5,5))
    if temps.est_en_pause():
        if affichage_pause:
            surface_pause = pygame.font.Font('font.ttf', 30).render('PAUSE', True, (255,255,255))
            taille_fenetre = fenetre.get_size()
            taille_surface_pause = surface_pause.get_size()
            fenetre.blit(surface_pause,(taille_fenetre[0]/2-taille_surface_pause[0]/2,taille_fenetre[1]- 1.5 * taille_surface_pause[1]))
        if temps_affichee == None:
            temps_affichee = time.time()
        if time.time() >= temps_affichee + Constantes.delai_clique_logo:
            temps_affichee = None
            affichage_pause = not(affichage_pause)
    else:
        affichage_pause
    return (affichage_pause,temps_affichee)

def affichage_map(fenetre,temps,mode_devellopeur = False):
    
    sprite_map = pygame.image.load(Constantes.sprite_map_monde)
    sprite_map_prime = redim_sprite_dim_fenetre(sprite_map,fenetre.get_size())
    sprite_point = pygame.image.load(Constantes.sprite_point)
    sprite_map_prime = recolore_main_color(sprite_map_prime,(0,178,0))
    
    tabl_vehicule = []
    bibliotheque_villes = Constantes.villes
    end = False
    font_mouse = pygame.font.Font('font.ttf', 12)
    affichage_pause = True
    temps_affichee = None
    while not(end) :
        fenetre.fill((0,0,255))
        fenetre.blit(sprite_map_prime,(0,0))
        
        clavier = main_fonctions.get_clavier()
        if clavier == pygame.K_SPACE:
            temps.inverser()
        
        for nom_ville in bibliotheque_villes:
            pos_ville = bibliotheque_villes[nom_ville]
            fenetre.blit(sprite_point,pos_ville)
        if mode_devellopeur:
            add_city_with_click(bibliotheque_villes)
            interface_devellopeur_map_monde.affichage_interface(fenetre)
        gest_mouse(fenetre,font_mouse,bibliotheque_villes)
        tabl_vehicule = gest_vehicule(fenetre,font_mouse,bibliotheque_villes,tabl_vehicule,temps)
        (affichage_pause,temps_affichee) = affichage_temps(fenetre,temps,affichage_pause,temps_affichee)
        pygame.display.flip()
    return

class Vehicule:
    
    def __init__(self,nom_ligne,pos_depart,pos_arrive,sprite,temps,transparent = True):
        self.nom_ligne = nom_ligne
        taille_point = Constantes.taille_sprite_point
        self.pos_depart = main_fonctions.get_centre(pos_depart,taille_point)
        self.pos_arrive = main_fonctions.get_centre(pos_arrive,taille_point)
        self.distance = main_fonctions.distance_entre_deux_points(pos_depart,pos_arrive)
        self.temps_deplacement = self.distance/Constantes.vitesse_vehicule
        self.transparent = transparent
        self.sprite = self.get_sprite(sprite,transparent)
        self.rect_arrivee = pygame.Rect(self.pos_arrive,Constantes.taille_sprite_point)
        self.temps_depart = temps.get_time()
        self.temps_arrrive = self.temps_depart+self.temps_deplacement
        self.ratio = 0
        self.position = self.get_postion(temps)
        self.rect = pygame.Rect(self.position,self.sprite.get_rect().size)
        self.place_stockage = random.randint(1,10)
        return
    
    def get_delta_coord(self,i):
        return (self.pos_arrive[i] - self.pos_depart[i])
    
    def get_postion(self,temps):
        self.ratio = (temps.get_time()-self.temps_depart)/(self.temps_arrrive - self.temps_depart)
        x = self.get_delta_coord(0)*self.ratio + self.pos_depart[0]
        y = self.get_delta_coord(1)*self.ratio + self.pos_depart[1]
        taille_rect_sprite = self.sprite.get_rect().size
        self.rect = pygame.Rect((x,y),taille_rect_sprite)
        self.position =(x,y)
        return self.position
    
    def test_fin_deplacement(self):
        (x,y) = self.position
        (x_fin,y_fin) = self.pos_arrive
        constante_fin = 2
        return (x_fin + constante_fin >= x and x_fin - constante_fin <= x) and (y_fin + constante_fin >= y and y_fin - constante_fin <= y)  #(self.rect.colliderect(self.rect_arrivee) == 1)
    
    def gest_affichage_info(self,pos_mouse,fenetre,font):
        if  self.rect.collidepoint(pos_mouse):
            draw_mini_fenetre(fenetre,font,self.position,self.nom_ligne+' : '+ str(self.place_stockage))
        return
    
    def calcul_angle(self):
        norme = main_fonctions.distance_entre_deux_points(self.pos_depart,self.pos_arrive)
        hauteur = self.pos_depart[0]-self.pos_arrive[0]
        largeur = self.pos_depart[1]-self.pos_arrive[1]
        
        Angle_sin= math.degrees(math.asin(hauteur/norme))
        Angle_cos = math.degrees(math.acos(largeur/norme))
        
        if Angle_sin == 0:
            Angle_sin = 1
        if Angle_cos == 0:
            Angle_cos = 1
        
        if Angle_sin/math.fabs(Angle_sin) == Angle_cos/math.fabs(Angle_cos):
            return Angle_cos
        else:
            return -Angle_cos
    
    def get_sprite(self,sprite,transparent):
        sprite = pygame.image.load(sprite)
        couleur_avion_secondaire_arivee = main_fonctions.get_couleur_aleatoire()
        #sprite = main_fonctions.recolore(sprite,Constantes.couleur_avion_secondaire_depart,couleur_avion_secondaire_arivee)
        couleur_arrivee = main_fonctions.highlight(couleur_avion_secondaire_arivee)
        #sprite = main_fonctions.recolore(sprite,Constantes.couleur_avion_main_depart,couleur_arrivee)
        sprite = pygame.transform.rotate(sprite, self.calcul_angle())
        #if transparent:
            #sprite.set_alpha(95)
        return sprite