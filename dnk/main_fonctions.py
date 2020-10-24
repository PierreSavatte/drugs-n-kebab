import math
import random
import time

import pygame

from .constantes import Constantes


def get_val_aleatoire_parmis(tabl):
    """
    @param tabl: tableau : tableau de valeurs
    @return: une valeur parmis le tableau envoye
    """
    return tabl[random.randint(0, len(tabl) - 1)]


def get_val_aleatoire_parmis_bibliotheque(bibliotheque):
    """
    @param bibliotheque: bibliotheque : tableau de valeurs
    @return: une valeur parmis le tableau envoye
    """
    nb_alea = random.randint(0, len(bibliotheque) - 1)
    i = 0
    for element_biblio in bibliotheque:
        if i == nb_alea:
            indice = element_biblio
        i += 1
    return indice, bibliotheque[indice]


def get_valeur_multiple_de_5(valeur):
    return int(valeur / 10) * 10 + get_val_aleatoire_parmis([0, 5])


def distance_entre_deux_points(a, b):
    """
    @param a: tupple : coordonnees
    @param b: tupple : coordonnees
    @return: entier : distance entre le point a et le point b
    """
    Delta_x = a[0] - b[0]
    Delta_y = a[1] - b[1]
    return math.sqrt(Delta_x ** 2 + Delta_y ** 2)


def get_centre(point, taille):
    """
    @param point: tupple : coordonnees du centre du rectangle (point,taille)
    @param taille: tupple : taille du rectangle (point,taille)
    @return: tupple : coordonnees haut droite du rectange (point,taille)
    """
    (h, l) = taille
    (x, y) = point
    return int(x - 0.5 * h), int(y - 0.5 * l)


def affichage_texte(surface, font, texte, pos):
    """
    @param surface: pygame.surface : surface dans laquelle le texte sera blit
    @param font : pygame.font : police avec laquelle on ecrit le texte
    @param pos : tupple (x,y) : position d'affichage dans la surface du texte
    @return: None : mais necessite de display.flip()
    """
    surf_nom = font.render(texte, True, (0, 0, 0))
    surface.blit(surf_nom, pos)
    return


def get_pos_clic():
    """
    @return: tupple (x,y) : position de la souris au clic
    """
    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        return pygame.mouse.get_pos()


def get_pos_mouse():
    """
    @return: tupple (x,y) : position de la souris
    """
    pygame.event.get()
    return pygame.mouse.get_pos()


def get_clavier():
    """
    @return: pygame.key : valeur de la touche pour pygame
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            return event.key


def get_orientation_mouvement():
    """
    @return: string : orientation du mouvement voulu par le joueur
    """
    pygame.event.get()
    clavier = pygame.key.get_pressed()
    if clavier[pygame.K_UP]:
        return "N"
    if clavier[pygame.K_DOWN]:
        return "S"
    if clavier[pygame.K_LEFT]:
        return "O"
    if clavier[pygame.K_RIGHT]:
        return "E"


def get_main_color(sprite):
    """
    @param sprite: pygame.surface : surface depuis laquelle on cherche la couleur prncipale
    @return: main_couleur : tupple de dimension 3 : couleur principale
    """
    biblio = {}
    for x in range(0, sprite.get_width()):
        for y in range(0, sprite.get_height()):
            color = sprite.get_at((x, y))
            indice = tuple(color)[:-1]
            if indice in biblio:
                biblio[indice] += 1
            else:
                biblio[indice] = 1
    max_reccurence = 0
    main_couleur = (0, 0, 0)
    for color in biblio:
        if biblio[color] > max_reccurence and color != (0, 0, 0):
            max_reccurence = biblio[color]
            main_couleur = color
    return main_couleur


def recolore(sprite, couleur_depart, couleur_arrivee):
    """
    @param sprite: pygame.surface : surface depuis laquelle on cherche la couleur prncipale
    @param couleur_depart: tupple de dimension 3 : couleur a recolorer
    @param couleur_arrivee: tupple de dimension 3 : couleur de recoloration
    @return: sprite : pygame.surface : surface recolore
    """
    for x in range(0, sprite.get_width()):
        for y in range(0, sprite.get_height()):
            if sprite.get_at((x, y)) == couleur_depart:
                sprite.set_at((x, y), couleur_arrivee)
    return sprite


def get_couleur_aleatoire():
    """
    @return: couleur : tableau : couleur aleatoire
    """
    return [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    ]


def highlight(color):
    color[0] += 50 if color[0] < 205 else 0
    color[1] += 50 if color[1] < 205 else 0
    color[2] += 50 if color[2] < 205 else 0
    return color


def move_rect(Rect, orientation_mouvement, temps_dernier_mvt, acceleration):
    """
    @param Rect: pygame.rect : rectange qui est a bouger
    @param orientation_mouvement : string : orientation du mouvement voulu par le joueur
    @param temps_dernier_mvt : float : temps du dernier mouvement a l'ecran
    @param acceleration : float : acceleration
    @return: (Rect,temps_dernier_mvt) :
        Rect : pygame.rect : rectange une fois deplace
        temps_dernier_mvt : float : temps du dernier mouvement a l'ecran, mis a jour
    """
    (x, y) = (0, 0)
    horloge = time.time()
    if temps_dernier_mvt + Constantes.temp_refresh < horloge:
        temps_dernier_mvt = horloge
        if orientation_mouvement == "N":
            (x, y) = (0, -int(acceleration))
        elif orientation_mouvement == "S":
            (x, y) = (0, int(acceleration))
        elif orientation_mouvement == "E":
            (x, y) = (int(acceleration), 0)
        elif orientation_mouvement == "O":
            (x, y) = (-int(acceleration), 0)
    Rect = Rect.move(x, y)
    return Rect, temps_dernier_mvt


def get_rect_mouvement(orientation_mouvement, temps_dernier_mvt, acceleration):
    """
    @param orientation_mouvement : string : orientation du mouvement voulu par le joueur
    @param temps_dernier_mvt : float : temps du dernier mouvement a l'ecran
    @param acceleration : float : acceleration
    @return: (Rect,temps_dernier_mvt) :
        Rect : pygame.rect : rectange une fois deplace
        temps_dernier_mvt : float : temps du dernier mouvement a l'ecran, mis a jour
    """
    return move_rect(
        pygame.Rect(0, 0, 0, 0),
        orientation_mouvement,
        temps_dernier_mvt,
        acceleration,
    )


class Menu_Deroulant:
    """
    Classe de menu deroulant :
        Un bouton, lorsque l'on clique dessus des boutons apparaissent dessous. Si l'on clique sur un de ces derniers,
        la fonction associe sera execute
    """

    def __init__(
        self, font, position_rect, nom, tabl_fonctions_dans_deroulements
    ):
        """
        Constructeur
        @param font : pygame.font : police de l'interieur des boutons
        @param position_rect : tupple : position du rectangle principal
        @param nom : string : nom du bouton principal
        @param tabl_fonctions_dans_deroulements : tableau : tableau rempli des fonctions executables
        """
        self.position_rect = position_rect
        self.nom = nom
        self.temps_depart_clic = None
        self.deroulee = False
        self.temps_dernier_clic = time.time()
        self.temps_deroule = time.time()
        self.ancien_bouton = None
        self.image_fleche = pygame.image.load(
            Constantes.sprite_fleche_menu_deroulant
        )

        self.main_bouton = Bouton(
            font, self.position_rect, self.nom, self.Derouler
        )
        bottomleft = self.main_bouton.rect.bottomleft
        self.position_rect_deroulement = (
            bottomleft[0] + self.image_fleche.get_rect().size[0] * 2,
            bottomleft[1] + Constantes.decalage_bouton_main_deroulement_y,
        )

        (self.tabl_boutons, self.rect_sous_boutons) = self.def_boutons(
            font, tabl_fonctions_dans_deroulements
        )
        return

    def def_boutons(self, font, tabl_fonctions_dans_deroulements):
        """
        definit l'ensemble des sous-boutons ainsi que le rectangle dans lequel ils sont
        @param font : pygame.font : police de l'interieur des boutons
        @param tabl_fonctions_dans_deroulements : tableau : tableau rempli des fonctions executables
        @return: (tabl_boutons,rect_sous_boutons) :
            tabl_boutons : tableau : tableau de Boutons
            rect_sous_boutons : pygame.rect : rectangle sur lequel est situe l'ensemble des boutons
        """
        size_rect = [0, 0]
        pos_temp = self.position_rect_deroulement
        tabl_boutons = []
        for i in range(len(tabl_fonctions_dans_deroulements)):
            fonction = tabl_fonctions_dans_deroulements[i]
            tabl_boutons.append(
                Bouton(font, pos_temp, fonction.__name__, fonction)
            )
            hauteur_bouton = tabl_boutons[i].rect.size[1]
            largeur_bouton = tabl_boutons[i].rect.size[0]
            pos_temp_1 = pos_temp[1]
            hauteur_total = (
                Constantes.decalage_entre_boutons_y + hauteur_bouton
            )
            pos_temp_1 += hauteur_total
            pos_temp = (pos_temp[0], pos_temp_1)
            size_rect[1] += hauteur_total
            if size_rect[0] < largeur_bouton:
                size_rect[0] = largeur_bouton
        size_rect[0] += (
            self.position_rect_deroulement[0] - self.position_rect[0]
        )
        rect_sous_boutons = pygame.Rect(
            (self.position_rect[0], self.position_rect_deroulement[1]),
            size_rect,
        )

        return tabl_boutons, rect_sous_boutons

    def Update(self, surface, pos_mouse_clic, pos_mouse):
        """
        Met a jour le menu deroulant :
            affiche les boutons si le menu est deroule
        @param surface : pygame.surface : fenetre dans laquelle afficher le menu deroulant
        @param pos_mouse_clic : tupple : position de la souris au clic
        @param pos_mouse : tupple : position de la souris (sans forcement de clic)
        @return: None
        """
        temps = time.time()
        self.main_bouton.Update(surface, pos_mouse_clic)
        if self.deroulee:
            if pos_mouse is not None:
                if (
                    not (self.rect_sous_boutons.collidepoint(pos_mouse))
                    and temps - self.temps_deroule
                    >= Constantes.delai_clique_logo
                ):
                    self.deroulee = False
            # pygame.draw.rect(surface,(0,0,0),self.rect_sous_boutons)
            for bouton in self.tabl_boutons:
                pos_bouton = bouton.position
                surface.blit(
                    self.image_fleche,
                    (
                        pos_bouton[0] - self.image_fleche.get_rect().size[0],
                        pos_bouton[1] + 2,
                    ),
                )
                bouton.afficher(surface)
            if pos_mouse_clic is not None:
                for bouton in self.tabl_boutons:
                    if bouton.rect.collidepoint(pos_mouse) == 1:
                        if (
                            self.ancien_bouton != bouton
                            or self.temps_dernier_clic
                            + Constantes.delai_clique_logo
                            <= temps
                        ):
                            self.ancien_bouton = bouton
                            self.temps_dernier_clic = temps
                            bouton.Update(surface, pos_mouse)
        return

    def Derouler(self):
        """
        defini self.deroulee sur Vrai
        @return: None
        """
        self.deroulee = True
        self.temps_deroule = time.time()
        return


class Slider:
    """
    Classe de slider :
        Un curseur et un rectangle dans lequel il se deplace, la position du curseur dans le rectangle defini la valeur

    """

    def __init__(
        self,
        pos,
        val_depart=0,
        val_max=100,
        num_couleur_arg=None,
        nom_slider="",
        horizontal_arg=False,
    ):
        """
        Constructeur
        @param pos: tupple (x,y) : position du slider
        @param val_depart : int : valeur de depart du slider
        @param val_max: int : valeur que peut prendre le slider au maximum
        @param num_couleur_arg : int : si le slider defini une teinte de couleur (soit rouge, soit bleu ou soit vert) on peut
            passer en argument le numero de couleur;
            Remarque : meme si le slider ne correspond pas a une couleur, le fait de donner Vrai en argument fera que le curseur
            sera colore quand meme en fonction de la valeur du slider
        @param nom_slider: string : nom associe au slider
        @param horizontal_arg : booleen : defini si le slider est affiche horizontalement ou non
        """
        self.horizontal = horizontal_arg
        self.num_couleur = num_couleur_arg
        self.nom = nom_slider
        self.taille_slide_x = Constantes.taille_slide_x
        self.taille_slide_y = Constantes.taille_slide_y
        self.taille_curseur_x = Constantes.taille_curseur_x
        self.taille_curseur_y = Constantes.taille_curseur_y

        self.position_start_slider = pos
        self.rect_slider = self.get_rect_slider()
        self.valeur = val_depart
        self.valeur_max = val_max
        return

    def apply_modif_valeurs(self, tabl_sliders_lies, valeur_temp):
        """
        Fonction qui permet d'appliquer une mise a jour de la valeur du slider
        @param tabl_sliders_lies: tableau de Slider : tableau de Slider lies a ce slider
        @param valeur_temp : int : valeur temporaire a mettre a jour
        @return: None
        """
        if tabl_sliders_lies is None:
            self.valeur = valeur_temp
        else:
            """
            #Debut get_tabl_valeurs_sliders_lies
            """
            tabl_valeurs_sliders_lies = []
            for slider in tabl_sliders_lies:
                tabl_valeurs_sliders_lies.append(slider.valeur)
            """
                #Fin get_tabl_valeurs_sliders_lies
            """
            """
                #Debut get_valeur_diff
            """
            nouvelle_val = valeur_temp
            ancienne_val = self.valeur
            difference = nouvelle_val - ancienne_val
            if nouvelle_val != ancienne_val:
                self.valeur = nouvelle_val
                curseurs_modifiables = []
                modif_temp = -difference / (len(tabl_valeurs_sliders_lies) - 1)
                for i in range(len(tabl_valeurs_sliders_lies)):
                    val_temp_i = tabl_sliders_lies[i].valeur + modif_temp
                    if 0 <= val_temp_i <= 100:
                        curseurs_modifiables.append(tabl_sliders_lies[i])
                modif_pour_autres_curseurs = -difference / (
                    len(curseurs_modifiables)
                )

                """'
                    #Fin get_valeur_diff
                """
                """
                    #Debut application_valeur_diff
                """
                self.valeur = nouvelle_val
                for slider in curseurs_modifiables:
                    slider.valeur += modif_pour_autres_curseurs
            """
                #Fin application_valeur_diff
            """
        return

    def Update(self, tabl_sliders_lies=None):
        """
        Fonction qui permet de mettre a jour la valeur du slider
        @param tabl_sliders_lies: tableau de Slider : tableau de Slider lies a ce slider
        @return: None
        """
        pos_mouse = get_pos_clic()
        if pos_mouse is not None:
            if self.rect_slider.collidepoint(pos_mouse):
                if self.horizontal:
                    x = pos_mouse[0]
                    x_start = self.position_start_slider[0]
                    valeur_temp = int(
                        ((-(x - x_start) / self.taille_slide_y) + 1)
                        * self.valeur_max
                    )
                    self.apply_modif_valeurs(tabl_sliders_lies, valeur_temp)
                else:
                    y = pos_mouse[1]
                    y_start = self.position_start_slider[1]
                    valeur_temp = int(
                        ((-(y - y_start) / self.taille_slide_y) + 1)
                        * self.valeur_max
                    )
                    self.apply_modif_valeurs(tabl_sliders_lies, valeur_temp)
        return

    def get_rect_slider(self):
        """
        Fonction qui rends le rectangle du slider
        @return: pygame.Rect : rectangle du slider
        """
        if self.horizontal:
            rect = pygame.Rect(
                self.position_start_slider,
                (self.taille_slide_y, self.taille_slide_x),
            )
        else:
            rect = pygame.Rect(
                self.position_start_slider,
                (self.taille_slide_x, self.taille_slide_y),
            )
        return rect

    def get_rect_curseur(self):
        """
        Fonction qui rends le rectangle du curseur
        @return: pygame.Rect : rectangle du curseur
        """
        if self.horizontal:
            x = (
                (-(self.valeur / self.valeur_max) + 1) * self.taille_slide_y
                + self.position_start_slider[0]
                - (0.25 * self.taille_curseur_x)
            )
            y = (
                self.position_start_slider[1]
                - (self.taille_curseur_y - self.taille_slide_x) / 2
                - (self.taille_curseur_y)
            )
            rect = pygame.Rect(
                (x, y), (self.taille_curseur_y, self.taille_curseur_x)
            )
        else:
            x = (
                self.position_start_slider[0]
                - (self.taille_curseur_x - self.taille_slide_x) / 2
            )
            y = (
                (-(self.valeur / self.valeur_max) + 1) * self.taille_slide_y
                + self.position_start_slider[1]
                - (0.5 * self.taille_curseur_y)
            )
            rect = pygame.Rect(
                (x, y), (self.taille_curseur_x, self.taille_curseur_y)
            )
        return rect

    def afficher(self, surface, font):
        """
        Fonction qui rends le rectangle du curseur
        @param surface: pygame.surface : surface dans laquelle afficher le slider
        @param font: pygame.font : police utilise pour aficher le nom du slider
        @return: None
        """
        if self.nom != "":
            surf_nom = font.render(self.nom, True, (0, 0, 0))
            if self.horizontal:
                size_surf = surf_nom.get_rect().size
                position = (
                    self.position_start_slider[0] - size_surf[0],
                    self.position_start_slider[1],
                )
            else:
                size_surf = surf_nom.get_rect().size
                position = (
                    self.position_start_slider[0] - size_surf[0] / 4,
                    self.position_start_slider[1] - size_surf[1],
                )
            surface.blit(surf_nom, position)
        pygame.draw.rect(surface, (0, 0, 0), self.rect_slider, 1)
        if self.num_couleur is not None:
            couleur_curseur = [0, 0, 0]
            if 255 >= self.valeur >= 0:
                couleur_curseur[self.num_couleur] = self.valeur
            else:
                couleur_curseur = (0, 0, 0)
        else:
            couleur_curseur = (0, 0, 0)
        pygame.draw.rect(surface, couleur_curseur, self.get_rect_curseur())
        return


class Bouton:
    """
    Classe de bouton :
        Un bouton clickable, si clique, une fonction est execute

    """

    def __init__(
        self,
        font,
        pos,
        nom,
        fonction_retour,
        resize=None,
        couleur_bouton=(255, 255, 255),
        actif=True,
    ):
        """
        Constructeur
        @param font: pygame.font : police utilise pour l'affichage du nom dans le bouton
        @param pos : tupple : position du bouton (haut droite)
        @param nom: string : nom a afficher dans le bouton
        @param fonction_retour : fonction : fonction appelee lors de l'appuie sur le bouton
        """
        self.nom = nom
        self.actif = actif
        self.couleur = couleur_bouton
        self.position = pos
        self.sprite = self.get_sprite(font, resize)
        self.rect = pygame.Rect(pos, self.sprite.get_rect().size)
        self.fonction_retour = fonction_retour
        return

    def afficher(self, surface):
        """
        Affiche le bouton
        @param surface: pygame.surface : surface dans laquelle afficher le bouton
        @return: None
        """
        surface.blit(self.sprite, self.position)
        return

    def get_sprite(self, font, resize):
        """
        Affiche le bouton
        @param font: pygame.font : police utilise pour l'affichage du nom dans le bouton
        @return: surface_sprite : pygame.surface : surface contenant le bouton
        """
        surface_texte = font.render(self.nom, True, (0, 0, 0))
        size = surface_texte.get_rect().size
        new_size = (size[0] + 10, size[1] + 10)
        surface_sprite = pygame.Surface(new_size)
        surface_sprite.fill((255, 255, 255))
        pygame.draw.rect(surface_sprite, self.couleur, ((0, 0), new_size))
        pygame.draw.rect(
            surface_sprite,
            Constantes.couleur_gris,
            ((0, 0), (new_size[0] - 2, new_size[1] - 2)),
            2,
        )
        pygame.draw.rect(
            surface_sprite,
            Constantes.couleur_gris_light,
            ((2, 2), (new_size[0] - 2, new_size[1] - 2)),
            2,
        )
        pygame.draw.rect(
            surface_sprite, (0, 0, 0), ((0, 0), (new_size[0], new_size[1])), 2
        )
        surface_sprite.blit(surface_texte, (5, 5))
        if resize is not None:
            taille_surface_sprite = surface_sprite.get_rect().size
            surface_sprite = pygame.transform.scale(
                surface_sprite,
                (
                    int(taille_surface_sprite[0] * resize),
                    int(taille_surface_sprite[1] * resize),
                ),
            )
        return surface_sprite

    def get_long(self):
        return self.rect.size[0]

    def get_hauteur(self):
        return self.rect.size[1]

    def Update(self, surface, pos_mouse_clic):
        """
        Met a jour le bouton
        @param fenetre: pygame.surface : surface dans laquelle afficher le bouton
        @param pos_mouse: tupple : position de la souris au clic
        @return:
            fonction_retour : fonction : fonction a appeller si le bouton est active
            OU
            None : sinon
        """
        self.afficher(surface)
        if pos_mouse_clic is not None and self.actif:
            if self.rect.collidepoint(pos_mouse_clic):
                return self.fonction_retour()
            else:
                return


class Rect_Saisie:
    """
    Classe de rectangle de saisie :
        Un rectangle dans lequel on peut saisir une valeur

    """

    def __init__(self, pos, val_arg, val_max_arg):
        """
        Constructeur
        @param pos : tupple : position du rectangle de saisie (haut droite)
        @param val_arg : entier : valeur de depart dans le rectangle de saisie
        @param val_max_arg : entier : valeur maximale que peut prendre le rectangle de saisie
        """
        self.valeur = val_arg
        self.val_max = val_max_arg
        self.taille = (
            len(str(self.val_max)) * Constantes.taille_police_ecriture,
            1.5 * Constantes.taille_police_ecriture,
        )
        self.rectangle_noir = pygame.Rect(pos, self.taille)
        self.rectangle_gris = pygame.Rect(
            (pos[0] + 1, pos[1] + 1), (self.taille[0] - 1, self.taille[1] - 1)
        )
        self.position_texte = (pos[0] + 3, pos[1] + 3)
        return

    def afficher(
        self, surface, font, couleur_valeur_saisie=(0, 0, 0), valeur_temp=None
    ):
        """
        Permet d'afficher le rectangle de saisie
        @param surface : pygame.surface : surface dans laquelle afficher le rectangle de saisie
        @param font : pygame.font : police d'ecriture utilisee pour ecrire la valeur dans le rectangle de saisie
        @param couleur_valeur_saisie : tupple : Si une valeur est passee, la valeur du rectangle de saisie sera affichee de
            cette derniere. Sinon, la valeur sera affichee en noir
        @param valeur_temp : entier : valeur temporaire a afficher dans le rechangle de saisie
        @return: None
        """
        if valeur_temp is not None:
            valeur = valeur_temp
        else:
            valeur = self.valeur
        surf_nom = font.render(str(valeur), True, couleur_valeur_saisie)
        pygame.draw.rect(
            surface, Constantes.couleur_gris, self.rectangle_gris, 1
        )
        pygame.draw.rect(surface, (0, 0, 0), self.rectangle_noir, 1)
        surface.blit(surf_nom, self.position_texte)
        return

    def mode_saisie(self, surface, font):
        """
        Fonction activant le mode de saisie si l'utilisateur a clicke dans le rectangle de saisie
        @param surface : pygame.surface : surface dans laquelle afficher le rectangle de saisie
        @param font : pygame.font : police d'ecriture utilisee pour ecrire la valeur dans le rectangle de saisie
        @return: None
        """
        mouse = get_pos_clic()
        key = get_clavier()
        chaine_saisie = str(self.valeur)
        if mouse is not None:
            temps_debut_mode_saisie = time.time()
            saisie = True
        else:
            saisie = False
        while saisie and not (
            (key == pygame.K_RETURN) or (key == pygame.K_KP_ENTER)
        ):
            pygame.draw.rect(surface, (255, 255, 255), self.rectangle_noir)
            self.afficher(
                surface,
                font,
                couleur_valeur_saisie=(255, 0, 0),
                valeur_temp=chaine_saisie,
            )
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
                    if int(chaine_saisie) > self.val_max:
                        chaine_saisie = str(self.val_max)
            mouse = get_pos_clic()
            if (
                mouse is not None
                and temps_debut_mode_saisie + Constantes.delai_clique_logo
                <= time.time()
            ):
                saisie = False
            pygame.display.flip()
        self.valeur = int(chaine_saisie)
        return

    def Update(self, surface, font, pos_mouse_clic, valeur_MAJ=None):
        """
        Fonction mettant a jour le rectangle de saisie
        @param surface : pygame.surface : surface dans laquelle afficher le rectangle de saisie
        @param font : pygame.font : police d'ecriture utilisee pour ecrire la valeur dans le rectangle de saisie
        @param pos_mouse : tupple : position de la souris au clic
        @param valeur_MAJ : entier : une valeur de mise a jour peut etre passee en argument
        @return: None
        """
        self.afficher(surface, font)
        if valeur_MAJ is not None:
            self.valeur = valeur_MAJ
        if self.rectangle_noir.collidepoint(pos_mouse_clic):
            return self.mode_saisie(surface, font)
        else:
            return
