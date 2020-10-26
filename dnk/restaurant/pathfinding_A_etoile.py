import math

from ..constantes import Constantes


def distance_entre_deux_points(A, B):
    (x_A, y_A) = A
    (x_B, y_B) = B
    return math.sqrt((x_A - x_B) ** 2 + (y_A - y_B) ** 2)


def get_cout(coord_depart, coord_etudiee, coord_fin):
    cout_g = distance_entre_deux_points(coord_depart, coord_etudiee)
    cout_h = distance_entre_deux_points(coord_fin, coord_etudiee)
    return cout_g + cout_h


def get_noeud_plus_bas_cout_grille_ouverte(
    coord_depart, grille_ouverte, coord_fin
):
    cout_min = grille_ouverte[0][2]
    case_cout_min = grille_ouverte[0]
    for case in grille_ouverte:
        cout_temp = get_cout(coord_depart, case[0], coord_fin)
        if cout_temp < cout_min:
            cout_min = cout_temp
            case_cout_min = case
    return case_cout_min


def pop_valeur_in_liste(valeur, liste):
    for x in range(len(liste) - 1):
        if liste[x][0] == valeur:
            liste.pop(x)
    return


def get_indice_item(liste, item):
    for i in range(len(liste)):
        if liste[i][0] == item:
            return i


def get_path(grille_fermee, coord_fin, coord_depart):
    path = []
    coord_etudiee = coord_fin
    while coord_etudiee != coord_depart:
        path.append(coord_etudiee)
        coord_etudiee = grille_fermee[
            get_indice_item(grille_fermee, coord_etudiee)
        ][1]
    return inverser_liste(path)


def inverser_liste(liste):
    liste_inversee = []
    for x in range(len(liste)):
        liste_inversee.append(liste[-(x + 1)])
    return liste_inversee


def test_in_list(liste, objet):
    test = False
    for objet_liste in liste:
        test = test or (objet == objet_liste[0])
    return test


def pathfinding(
    grille_restaurant, coord_depart, coord_fin, liste_position_personnages
):

    if coord_depart is None or coord_fin is None:
        print("ERROR : " + str(coord_depart) + " ; " + str(coord_fin))

    grille_ouverte = []
    grille_fermee = []

    grille_ouverte.append(
        (coord_depart, None, get_cout(coord_depart, coord_depart, coord_fin))
    )

    coord_actuelle = coord_depart

    profondeur = 0

    while (coord_actuelle != coord_fin) and (
        profondeur <= Constantes.profondeur_pathfinding
    ):
        noeud_plus_bas = get_noeud_plus_bas_cout_grille_ouverte(
            coord_depart, grille_ouverte, coord_fin
        )
        coord_actuelle = noeud_plus_bas[0]
        pop_valeur_in_liste(coord_actuelle, grille_ouverte)
        grille_fermee.append(noeud_plus_bas)

        for (x, y) in [
            (coord_actuelle[0] - 1, coord_actuelle[1]),
            (coord_actuelle[0], coord_actuelle[1] - 1),
            (coord_actuelle[0], coord_actuelle[1] + 1),
            (coord_actuelle[0] + 1, coord_actuelle[1]),
        ]:
            if (
                0 <= x < len(grille_restaurant)
                and 0 <= y < len(grille_restaurant[0])
                and (x, y) != coord_actuelle
            ):
                voisin = (x, y)
                if (
                    grille_restaurant[x][y][Constantes.nom_biblio_walkable]
                    and not (test_in_list(grille_fermee, voisin))
                    and not ((x, y) in liste_position_personnages)
                ):
                    cout_temp = get_cout(coord_depart, voisin, coord_fin)
                    i = get_indice_item(grille_ouverte, voisin)

                    # if not(test_in_list(grille_ouverte,voisin)):
                    if i is None:
                        grille_ouverte.append(
                            (voisin, coord_actuelle, cout_temp)
                        )
                    elif cout_temp < grille_ouverte[i][2]:
                        grille_ouverte[i] = (voisin, coord_actuelle, cout_temp)

        profondeur += 1
    path = None
    if coord_actuelle == coord_fin:
        path = get_path(grille_fermee, coord_fin, coord_depart)
    else:
        path = get_path(grille_fermee, coord_actuelle, coord_depart)
    return path
