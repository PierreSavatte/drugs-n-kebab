import random

from ..constants import Constantes


def gen_ville_vide():
    tabl_ville = []
    for x in range(Constantes.taille_ville[0] + 1):
        tabl_ville.append([])
        for y in range(Constantes.taille_ville[1] + 1):
            tabl_ville[x].append(None)
    return tabl_ville


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


def gen_stats(type_bat):
    if type_bat == Constantes.stat_occupe:
        biblio_stat = {}
        biblio_stat[Constantes.nom_type] = None
        biblio_stat[Constantes.stat_cout] = None
        biblio_stat[Constantes.stat_achete] = False
        biblio_stat[Constantes.stat_occupe] = True
    else:
        biblio_stat = {}
        biblio_stat[Constantes.nom_type] = type_bat
        biblio_stat[Constantes.stat_cout] = get_val_cout_batiment(type_bat)
        biblio_stat[Constantes.stat_achete] = False
        biblio_stat[Constantes.stat_occupe] = True
    return biblio_stat


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


def get_sprite_route_unit(tabl_orient):
    if tabl_orient == ["O", "E", "N", "S"]:
        return Constantes.nom_sprite_route_croisement
    if "O" in tabl_orient:
        return Constantes.nom_sprite_route_x
    if "N" in tabl_orient:
        return Constantes.nom_sprite_route_y
    else:
        return Constantes.nom_sprite_foret


def get_tabl_route(tabl_coord_route):
    tabl_orientation = ["O", "E", "N", "S"]
    tabl_route = []
    for (x, y) in tabl_coord_route:
        tabl_orient_temp = []
        i = 0
        for (x_2, y_2) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (x_2, y_2) in tabl_coord_route:
                tabl_orient_temp.append(tabl_orientation[i])
            i += 1
        tabl_route.append(((x, y), get_sprite_route_unit(tabl_orient_temp)))
    return tabl_route


def gen_tabl_entree_ville(ville):
    long_ville_x = len(ville) - 1
    long_ville_y = len(ville[0]) - 1

    milieu_ville_x = int(long_ville_x / 2)
    milieu_ville_y = int(long_ville_y / 2)

    long_entree = int(long_ville_x / 5)

    tabl = []
    for i in range(long_entree):
        tabl.append((i, milieu_ville_y))
        tabl.append((long_ville_x - i, milieu_ville_y))

        tabl.append((milieu_ville_x, i))
        tabl.append((milieu_ville_x, long_ville_y - i))

    for j in range(long_ville_x - long_entree):
        tabl.append((long_entree + j, long_entree))
        tabl.append((long_entree, long_entree + j))
        tabl.append(
            (long_ville_x - long_entree - j, long_ville_y - long_entree)
        )
        tabl.append(
            (long_ville_x - long_entree, long_ville_y - long_entree - j)
        )
    return tabl


def gen_route(ville):
    tabl_pos = gen_tabl_entree_ville(ville)
    """
    tabl.append()
    """
    tabl_route = get_tabl_route(tabl_pos)
    for route in tabl_route:
        (x, y) = route[0]
        ville[x][y] = [route[1]]
    return ville


def gen_ville():
    ville = gen_ville_vide()
    ville = gen_route(ville)
    # ville = gen_batiments(ville)
    # ville = gen_foret(ville)
    return ville
