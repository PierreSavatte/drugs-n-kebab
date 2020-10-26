import random
import time

from . import affichage
from .boutons_actions_employes import Boutons_actions_employes
from .client import Client
from .personnel import Personnel
from .. import main_fonctions
from ..constantes import Constantes


def get_valeur_alea(tabl):
    return tabl[random.randint(0, len(tabl) - 1)]


def loop(fenetre, font, restaurant, joueur, temps, pas_de_clients=False):

    # temps_horloge = temps.get_temps_horloge()

    temps_deplacement = time.time()
    temps_spawn = time.time()

    nb_chaises = compter_chaises(restaurant.grille_meubles)
    coord_sortie = get_coord_sortie(restaurant.grille_meubles)
    quitter = False
    # action_joueur = False
    boutons_affichees = False
    boutons = None

    """
        #Definition d'un employe pour les tests
    """
    restaurant.employes.append(
        Personnel(
            Constantes.nom_arabes,
            Constantes.nom_homme,
            Constantes.nom_categorie_chef_cuisinier,
            restaurant.pos_caisses,
        )
    )
    restaurant.employes[0].avancer_d_un_pas()

    while not (quitter):
        touche = affichage.get_clavier()
        pos_mouse_clic = main_fonctions.get_pos_clic()

        joueur.gestion_actions(temps, touche, restaurant)
        joueur.deplacer_joueur(touche, restaurant.grille_meubles)

        """
            #Gestion Spawn Clients
        """
        if not (pas_de_clients) and not (temps.est_en_pause()):
            if temps_spawn + Constantes.delai_spawn_client <= temps.get_time():
                temps_spawn = temps.get_time()
                if len(restaurant.clients) < nb_chaises:
                    restaurant.clients = spawn_clients(restaurant.clients)
        """
        """

        if (
            temps_deplacement + Constantes.delai_deplacement_client
            <= temps.get_time()
            and not (temps.est_en_pause())
        ):
            temps_deplacement = temps.get_time()
            gest_depl_individus(restaurant)

            for biblio_caisse in restaurant.pos_caisses:
                restaurant.gestion_client_en_caisse(
                    biblio_caisse,
                    fenetre,
                    font,
                    temps,
                    joueur,
                    action_du_joueur=True,
                )

            for client in restaurant.clients:
                client.Update(temps, restaurant)

        (boutons, boutons_affichees) = Gestion_boutons_ordres_employes(
            restaurant,
            fenetre,
            temps,
            font,
            pos_mouse_clic,
            boutons_affichees,
            boutons,
        )

        if len(restaurant.employes) > 0 and not (temps.est_en_pause()):
            for employe in restaurant.employes:
                employe.Update(temps, restaurant, fenetre, font)

        affichage.affichage_restaurant(
            restaurant, fenetre, font, joueur, boutons, temps
        )
        quitter = test_fin_loop(coord_sortie, joueur)
    return


def Gestion_boutons_ordres_employes(
    restaurant,
    fenetre,
    temps,
    font,
    pos_mouse_clic,
    boutons_affichees,
    boutons,
):
    if pos_mouse_clic is not None:
        if not boutons_affichees:
            coord_mouse = affichage.position_en_coordonnees(
                pos_mouse_clic,
                affichage.get_taille_sprite(restaurant.grille_meubles),
            )
            for employe in restaurant.employes:
                if employe.position == coord_mouse:
                    boutons = Boutons_actions_employes(
                        font, employe, pos_mouse_clic, restaurant, temps
                    )
                    boutons_affichees = True
        else:
            if boutons.fin:
                boutons_affichees = False
                boutons = None

    if boutons_affichees:
        boutons.Update(fenetre, pos_mouse_clic)
    return boutons, boutons_affichees


def compter_chaises(restaurant):
    compteur = 0
    for x in range(0, len(restaurant)):
        for y in range(0, len(restaurant[0])):
            if (
                restaurant[x][y][Constantes.nom_biblio_sprite]
                in Constantes.sprites_chaise
            ):
                compteur += 1
    return compteur


def get_coord_sortie(grille_meubles):
    for x in range(0, len(grille_meubles)):
        for y in range(0, len(grille_meubles[0])):
            if (
                grille_meubles[x][y][Constantes.nom_biblio_sprite]
                == Constantes.sprite_tapis_1
            ):
                return x, y


def test_fin_loop(coord_sortie, joueur):
    return joueur.position == coord_sortie and joueur.orientation == "DOWN"


def gest_depl_individus(restaurant):
    for entitees in [restaurant.clients, restaurant.employes]:
        i = 0
        if len(entitees) != 0:
            for entitee in entitees:
                entitee.get_objectif()
                entitee.modifier_chemin(
                    restaurant,
                    entitee.objectif,
                    get_liste_pos_pathfinding(restaurant.clients),
                )
                entitee.deplacer(
                    restaurant, get_liste_pos_pathfinding(restaurant.clients)
                )
                if entitee.test_despawn(restaurant.grille_meubles):
                    restaurant.clients.pop(i)
                i += 1


def spawn_clients(liste_clients):
    """
    A MODIFIER
    """
    liste_recettes_debloquees = Constantes.biblio_recettes
    liste_clients.append(
        Client(
            get_valeur_alea(Constantes.ethnic_table),
            get_valeur_alea(Constantes.tableau_sexe),
            liste_recettes_debloquees,
        )
    )
    return liste_clients


def get_liste_pos_pathfinding(liste_clients):
    liste = []
    for client in liste_clients:
        # if len(client.chemin) == 0 and (client.objectif !=Constantes.sprite_caisse):
        liste.append(client.position)
    return liste


def calcul_nombre_maximum_clients(heure, restaurant, joueur):

    nombre_chaises = compter_chaises(restaurant)
    temps_int = calcul_parametre_temps(heure)
    satisfaction_int = parametre_en_entier(joueur.satisfaction)
    proprete_int = parametre_en_entier(restaurant.proprete)
    notoriete = joueur.notoriete
    nb_maximum_clients = (
        1
        + temps_int
        + (satisfaction_int + proprete_int)
        + int(notoriete / 1000)
    )

    if nb_maximum_clients > nombre_chaises:
        nb_maximum_clients = nb_maximum_clients - nombre_chaises
    return nb_maximum_clients


def calcul_parametre_temps(temps):
    """Cette fonction est utilisee pour donner un entier selon l'heure du jeu, cet entier vaut 1 ou 2"""
    heures = int(temps[:2])
    temps_int = 1
    if (11 <= heures <= 13) or (19 <= heures <= 21):
        temps_int = 2
    return temps_int


def parametre_en_entier(parametre):
    """Cette fonction est utilisee pour passer les parametres de proprete et de satisfaction, qui sont comptes entre 0
    et 100, en entiers comptes entre 0 et 6"""
    parametre_int = 0
    if parametre <= 17 and parametre <= 32:
        parametre_int = 1
    elif parametre <= 33 and parametre <= 48:
        parametre = 2
    elif parametre <= 49 and parametre <= 64:
        parametre = 3
    elif parametre <= 65 and parametre <= 80:
        parametre = 4
    elif parametre <= 81 and parametre <= 96:
        parametre = 5
    elif parametre <= 97 and parametre <= 100:
        parametre = 6
    return parametre_int
