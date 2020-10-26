import glob
import pickle
import random

from ..constants import Constantes
from ..main_fonctions import get_val_aleatoire_parmis


def gen_stats(type_bat):
    if type_bat == Constantes.stat_occupe:
        return {
            Constantes.nom_type: None,
            Constantes.stat_cout: None,
            Constantes.stat_achete: False,
            Constantes.stat_occupe: True,
        }
    else:
        return {
            Constantes.nom_type: type_bat,
            Constantes.stat_cout: get_val_cout_batiment(type_bat),
            Constantes.stat_achete: False,
            Constantes.stat_occupe: True,
        }


def get_val_cout_batiment(type_bat):
    if type_bat == Constantes.type_maison:
        valeur = random.randint(
            Constantes.val_min_cout_type_maison,
            Constantes.val_max_cout_type_maison,
        )
    if type_bat == Constantes.type_appartement_small:
        valeur = random.randint(
            Constantes.val_min_cout_type_appartement_small,
            Constantes.val_max_cout_type_appartement_small,
        )
    if type_bat == Constantes.type_appartement_tall:
        valeur = random.randint(
            Constantes.val_min_cout_type_appartement_tall,
            Constantes.val_max_cout_type_appartement_tall,
        )
    if type_bat == Constantes.type_buildings:
        valeur = random.randint(
            Constantes.val_min_cout_type_buildings,
            Constantes.val_max_cout_type_buildings,
        )
    return valeur


def gen_ville_vide():
    tabl_ville = []
    for x in range(Constantes.taille_ville[0] + 1):
        tabl_ville.append([])
        for y in range(Constantes.taille_ville[1] + 1):
            tabl_ville[x].append(None)
    return tabl_ville


def get_liste_sprite(addresse_relative_fichier):
    return glob.glob(addresse_relative_fichier + "/*.png")


def gen_route(ville):
    nb_max = int(
        Constantes.taille_ville[0] / 4 + Constantes.taille_ville[1] / 4
    )
    for num_noeud in range(random.randint(3, nb_max + 3)):
        if random.randint(0, 1) == 0:
            y = random.randint(2, Constantes.taille_ville[1] - 2)
            if (
                ville[0][y] is None
                and ville[0][y - 1] is None
                and ville[0][y + 1] is None
            ):
                for x in range(Constantes.taille_ville[0] + 1):
                    if ville[x][y] is not None:
                        if ville[x][y][0] == Constantes.nom_sprite_route_y:
                            ville[x][y] = [
                                Constantes.nom_sprite_route_croisement
                            ]
                    else:
                        ville[x][y] = [Constantes.nom_sprite_route_x]
        else:
            x = random.randint(2, Constantes.taille_ville[0] - 2)
            if (
                ville[x][0] is None
                and ville[x + 1][0] is None
                and ville[x - 1][0] is None
            ):
                for y in range(Constantes.taille_ville[1] + 1):
                    if ville[x][y] is not None:
                        if ville[x][y][0] == Constantes.nom_sprite_route_x:
                            ville[x][y] = [
                                Constantes.nom_sprite_route_croisement
                            ]
                    else:
                        ville[x][y] = [Constantes.nom_sprite_route_y]
    return ville


def gen_route_test(ville):
    tableau_route = []
    tableau_noeuds = gen_noeuds_dans_ville(
        int(Constantes.taille_ville[0] / 4 + Constantes.taille_ville[1] / 4)
    )
    """
    for noeud_1 in tableau_noeuds:
        for noeud_2 in tableau_noeuds:
            tableau_route.append(gen_tabl_relie_deux_points(noeud_1,noeud_2))
    """
    for noeud_1 in tableau_noeuds:
        noeud_2 = tableau_noeuds[random.randint(0, len(tableau_noeuds))]
        tableau_route.append(gen_tabl_relie_deux_points(noeud_1, noeud_2))
    for tableau_route_unitee in tableau_route:
        for coord_route in tableau_route_unitee:
            (x, y) = coord_route
            ville[x][y] = [Constantes.nom_sprite_route_x]
    return ville


def gen_tabl_relie_deux_points(pt_1, pt_2):
    if pt_1[0] > pt_2[0]:
        return gen_tabl_relie_deux_points(pt_2, pt_1)
    else:
        tabl_points = []
        epsilon = 0
        if (pt_1[1] - pt_2[1]) > (pt_1[0] - pt_2[0]):
            if pt_1[1] < pt_2[1]:
                alpha = 1
            else:
                alpha = -1
            y = pt_1[1]
            for x in range(pt_1[0], pt_2[0]):
                tabl_points.append((x, y))
                if epsilon + ((pt_1[1] - pt_2[1]) / (pt_1[0] - pt_2[0])) < 0.5:
                    epsilon = epsilon + (
                        (pt_1[1] - pt_2[1]) / (pt_1[0] - pt_2[0])
                    )
                else:
                    y += alpha
                    epsilon = (
                        epsilon
                        + ((pt_1[1] - pt_2[1]) / (pt_1[0] - pt_2[0]))
                        - 1
                    )
                    tabl_points.append((x, y))
        else:
            if pt_1[0] < pt_2[0]:
                alpha = 1
            else:
                alpha = -1
            x = pt_1[0]
            for y in range(pt_1[1], pt_2[1]):
                tabl_points.append((x, y))
                if epsilon + ((pt_1[0] - pt_2[0]) / (pt_1[1] - pt_2[1])) < 0.5:
                    epsilon = epsilon + (
                        (pt_1[0] - pt_2[0]) / (pt_1[1] - pt_2[1])
                    )
                else:
                    x += alpha
                    epsilon = (
                        epsilon
                        + ((pt_1[0] - pt_2[0]) / (pt_1[1] - pt_2[1]))
                        - 1
                    )
                    tabl_points.append((x, y))
        return tabl_points


def gen_noeuds_dans_ville(nb_max_noeuds):
    tableau_noeuds = []
    for num_noeud in range(random.randint(3, nb_max_noeuds + 3)):
        coord_neoud_temp = gen_coord_alea_dans_tabl_ville()
        while test_coord_pres_autre_coord(coord_neoud_temp, tableau_noeuds):
            coord_neoud_temp = gen_coord_alea_dans_tabl_ville()
        tableau_noeuds.append(coord_neoud_temp)
    return tableau_noeuds


def gen_coord_alea_dans_tabl_ville():
    return (
        random.randint(2, Constantes.taille_ville[1] - 2),
        random.randint(2, Constantes.taille_ville[0] - 2),
    )


def test_coord_pres_autre_coord(coord, tabl_autre_coord):
    test = False
    for coord_2 in tabl_autre_coord:
        test = test or (
            abs(coord[0] - coord_2[0]) == 1 and abs(coord[1] - coord_2[1]) == 1
        )
    return test


def gen_foret(ville):
    nb_max = int(
        Constantes.taille_ville[0] / 4 + Constantes.taille_ville[1] / 4
    )
    for num_foret in range(random.randint(3, nb_max + 3)):
        x = random.randint(0, Constantes.taille_ville[0])
        y = random.randint(0, Constantes.taille_ville[1])
        for i in range(0, 5):
            for j in range(0, 5):
                diviseur = int(((i + j) / 2) + 1)
                if (
                    0 <= (x - i) <= Constantes.taille_ville[0]
                    and 0 <= (y - j) <= Constantes.taille_ville[1]
                ):
                    if (
                        ville[x - i][y - j] is None
                        and random.randint(0, int(100 / diviseur)) <= 20
                    ):
                        ville[x - i][y - j] = [Constantes.nom_sprite_foret]
                if (
                    0 <= (x + i) <= Constantes.taille_ville[0]
                    and 0 <= (y + j) <= Constantes.taille_ville[1]
                ):
                    if (
                        ville[x + i][y + j] is None
                        and random.randint(0, int(100 / diviseur)) <= 20
                    ):
                        ville[x + i][y + j] = [Constantes.nom_sprite_foret]
    return ville


def gen_batiments(ville):
    tabl_pos_x = range(0, Constantes.taille_ville[0])
    tabl_pos_y = range(0, Constantes.taille_ville[1])
    for x in tabl_pos_x:
        for y in tabl_pos_y:
            if ville[x][y] is None and test_si_entoure_par_route(
                ville, (x, y)
            ):
                if (
                    (x in tabl_pos_x[0:5])
                    or (x in tabl_pos_x[-5:0])
                    and (y in tabl_pos_y[0:5])
                    or (y in tabl_pos_y[-5:0])
                ):
                    ville[x][y] = [
                        get_val_aleatoire_parmis(
                            get_liste_sprite("city/maisons")
                        ),
                        gen_stats(Constantes.type_maison),
                    ]
                elif (
                    (x in tabl_pos_x[5:10])
                    or (x in tabl_pos_x[-10:-5])
                    and (y in tabl_pos_y[5:10])
                    or (y in tabl_pos_y[-10:-5])
                ):
                    ville[x][y] = [
                        get_val_aleatoire_parmis(
                            get_liste_sprite("city/appartements/type2")
                        ),
                        gen_stats(Constantes.type_appartement_small),
                    ]
                elif (
                    (x in tabl_pos_x[10:15])
                    or (x in tabl_pos_x[-15:-10])
                    and (y in tabl_pos_y[10:15])
                    or (y in tabl_pos_y[-15:-10])
                ):
                    ville[x][y] = [
                        get_val_aleatoire_parmis(
                            get_liste_sprite("city/appartements/type3")
                        ),
                        gen_stats(Constantes.type_appartement_tall),
                    ]
                else:
                    ville[x][y] = [
                        get_val_aleatoire_parmis(
                            get_liste_sprite("city/grattes_ciels")
                        ),
                        gen_stats(Constantes.type_buildings),
                    ]
    return ville


def test_si_entoure_par_route(ville, pos):
    (x, y) = pos
    test = False
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if x + i in range(
                0, Constantes.taille_ville[0]
            ) and y + j in range(0, Constantes.taille_ville[1]):
                if ville[x + i][y + j] is not None:
                    test = test or (
                        ville[x + i][y + j][0] in Constantes.noms_sprites_route
                    )
                else:
                    test = test or (
                        ville[x + i][y + j] in Constantes.noms_sprites_route
                    )
    return test


def gen_ville():
    ville = gen_ville_vide()
    ville = gen_route(ville)
    ville = gen_batiments(ville)
    ville = gen_foret(ville)
    return ville


def enregistrer_ville(ville, nom_ville):
    fichier = open(nom_ville + ".txt", "wb")
    pickle.dump(ville, fichier)
    fichier.close()


def charger_ville(nom_ville):
    fichier = open(nom_ville + ".txt", "rb")
    ville = pickle.load(fichier)
    fichier.close()
    return ville
