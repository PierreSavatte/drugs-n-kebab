import os


def get_character_sprites_paths(sprites_path, ethnicity, gender):
    return [
        os.path.join(
            sprites_path,
            "restaurant",
            "characters",
            ethnicity,
            gender,
            orientation,
        )
        for orientation in ["up", "down", "right", "left"]
    ]


class Constantes:
    root_path = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.join(root_path, "resources")
    sprites_path = os.path.join(resources_path, "sprites")

    taille_fen = (1000, 500)

    temp_refresh = 0.01

    larg_cadre_interface = 150

    icone = os.path.join(resources_path, "icone.ico")
    font = os.path.join(resources_path, "font.ttf")

    taille_logo = (10, 10)

    couleur_gris = (100, 100, 100)
    couleur_gris_light = (50, 50, 50)
    couleur_rouge = (255, 50, 50)
    couleur_vert = (50, 255, 50)
    couleur_bleu = (50, 50, 255)

    """
    ###
        Constantes Main Fonctions : 
    ###
    """

    decalage_bouton_main_deroulement_x = 3
    decalage_bouton_main_deroulement_y = 2
    decalage_entre_boutons_y = 2

    sprite_fleche_menu_deroulant = os.path.join(
        sprites_path, "world", "fleche_menu_deroulant.png"
    )

    """
    ###
        Constantes Logo : 
    ###
    """
    taille_police_ecriture = 10

    delai_clique_logo = 1

    larg_entre_slide = 3 * taille_police_ecriture

    x_start = 50
    y_start = 50
    taille_case = 25
    decalage_entre_cases = 1

    taille_boutons = 20

    x_tabl_max = x_start + taille_case * (
        taille_logo[0] + decalage_entre_cases
    )
    y_tabl_max = y_start + taille_case * (
        taille_logo[1] + decalage_entre_cases
    )

    taille_slide_x = 10
    taille_slide_y = (taille_case + decalage_entre_cases) * 5

    taille_curseur_x = 2 * taille_slide_x
    taille_curseur_y = 6
    decalage_couleur_curseur = taille_curseur_y / 2 + 1

    taille_couleur_x = (
        2 * (taille_case + decalage_entre_cases) + taille_slide_x
    )
    taille_couleur_y = taille_case

    y_start_saisie_couleur = (
        taille_slide_y + y_start + decalage_couleur_curseur
    )
    taille_saisie_couleur_y = taille_case

    x_start_bouton_fleche = taille_couleur_x / 2 + x_tabl_max
    y_start_carre_couleur_1 = (
        y_start_saisie_couleur
        + taille_saisie_couleur_y
        + decalage_couleur_curseur
    )
    y_start_bouton_fleche = (
        y_start_carre_couleur_1 + taille_couleur_y + decalage_couleur_curseur
    )
    y_start_carre_couleur_2 = (
        y_start_bouton_fleche + taille_boutons + decalage_couleur_curseur
    )

    sprite_pipette = os.path.join(sprites_path, "world", "pipette.bmp")
    sprite_fleche = os.path.join(sprites_path, "world", "fleche.bmp")
    sprite_quit = os.path.join(sprites_path, "world", "quit.bmp")

    """
    ###
        Constantes Map Monde : 
    ###
    """

    sprite_map_monde = os.path.join(sprites_path, "world", "world_map_2.png")
    sprite_point = os.path.join(sprites_path, "world", "point.png")
    taille_sprite_point = (10, 10)

    vitesse_vehicule = 15
    sprite_avion = os.path.join(sprites_path, "world", "avion.png")
    couleur_avion_main_depart = (239, 228, 176)
    couleur_avion_secondaire_depart = (127, 127, 127)

    villes = {
        "Kiev": (534, 101),
        "Paris": (455, 110),
        "Oslo": (481, 67),
        "Rio de Janeiro": (306, 373),
        "Perth": (812, 402),
        "San Francisco": (77, 145),
        "Sao Paulo": (295, 373),
        "Bangkok": (775, 235),
        "Santiago": (232, 413),
        "Oulan-Bator": (781, 110),
        "Guatemala": (155, 233),
        "Oran": (447, 157),
        "Tanger": (431, 159),
        "Atlanta": (184, 162),
        "Kaboul": (670, 162),
        "Miami": (191, 191),
        "Dublin": (432, 90),
        "Phnom Penh": (790, 241),
        "Rome": (490, 133),
        "Bamako": (419, 244),
        "Singapour": (788, 285),
        "Athenes": (520, 147),
        "Washington": (213, 142),
        "Seville": (432, 145),
        "Venise": (484, 119),
        "Los-Angeles": (81, 161),
        "Ushuaia": (261, 488),
        "Bombay": (686, 222),
        "Pyoungyang": (832, 144),
        "Auckland": (985, 426),
        "Tripoli": (490, 169),
        "Sydney": (914, 418),
        "Dakar": (393, 234),
        "Quito": (193, 289),
        "Moscou": (558, 83),
        "Albuquerque": (112, 152),
        "Kuala Lumpur": (781, 275),
        "Berlin": (489, 100),
        "Anchorage": (60, 64),
        "Edimbourg": (444, 82),
        "New-York": (225, 135),
        "Yaounde": (490, 273),
        "Pretoria": (537, 388),
        "La Havane": (184, 203),
        "New Delhi": (698, 186),
        "Seattle": (96, 111),
        "Le Caire": (545, 179),
        "Le Cap": (508, 413),
        "El-Paso": (119, 171),
        "La Mecque": (578, 206),
        "Manille": (842, 235),
        "Istanbul": (532, 136),
        "Dallas": (134, 158),
        "Port Louis": (627, 361),
        "Panama": (185, 254),
        "Hanoi": (782, 211),
        "Koweit": (598, 181),
        "Caracas": (230, 250),
        "Bagdad": (586, 163),
        "Medine": (575, 191),
        "Marrakech": (426, 174),
        "Saint-Denis": (617, 368),
        "Toronto": (215, 125),
        "Anadyr": (901, 51),
        "Helsinki": (518, 63),
        "Wellington": (977, 441),
        "Detroit": (198, 132),
        "Tunis": (476, 151),
        "Stockholm": (495, 70),
        "Tananarive": (599, 355),
        "Calcutta": (731, 199),
        "Nairobi": (572, 283),
        "Montreal": (244, 114),
        "Port-au-Prince": (213, 218),
        "Reykjavik": (404, 53),
        "Lima": (197, 328),
        "Fort-de-France": (246, 232),
        "Damas": (566, 161),
        "Chicago": (177, 132),
        "Shanghai": (828, 173),
        "Winnipeg": (190, 97),
        "Copenhague": (484, 84),
        "Mascate": (633, 202),
        "Buenos Aires": (266, 416),
        "Kingston": (194, 221),
        "Ankara": (548, 141),
        "Quebec": (256, 106),
        "Jakarta": (800, 313),
        "La Paz": (93, 197),
        "Tijuana": (84, 172),
        "Mexico": (127, 215),
        "Sofia": (521, 128),
        "Londres": (449, 97),
        "Jerusalem": (560, 170),
    }
    # {'Kiev': (534, 101), 'Paris': (455, 110), 'Oslo': (481, 67), 'Rio de Janeiro': (306, 373), 'Perth': (812, 402), 'San Francisco': (77, 145), 'Sao Paulo': (295, 373), 'Santiago': (232, 413), 'Oulan-Bator': (781, 110), 'Oran': (447, 157), 'Tanger': (431, 159), 'Atlanta': (184, 162), 'Miami': (191, 191), 'Dublin': (432, 90), 'Rome': (490, 133), 'Bamako': (419, 244), 'Athenes': (520, 147), 'Washington': (213, 142), 'Seville': (432, 145), 'Venise': (484, 119), 'Los-Angeles': (81, 161), 'Seattle': (96, 111), 'Bombay': (686, 222), 'Caracas': (230, 250), 'Auckland': (985, 426), 'Tripoli': (490, 169), 'Sydney': (914, 418), 'Dakar': (393, 234), 'Quito': (193, 289), 'Moscou': (558, 83), 'Albuquerque': (112, 152), 'Kuala Lumpur': (781, 275), 'Berlin': (489, 100), 'Anchorage': (60, 64), 'Edimbourg': (444, 82), 'New-York': (225, 135), 'Yaounde': (490, 273), 'Pretoria': (537, 388), 'New Delhi': (698, 186), 'Ushuaia': (261, 488), 'Le Caire': (545, 179), 'Le Cap': (508, 413), 'El-Paso': (119, 171), 'La Mecque': (578, 206), 'Quebec': (256, 106), 'Istanbul': (532, 136), 'Dallas': (134, 158), 'Hanoi': (782, 211), 'Koweit': (598, 181), 'Pyoungyang': (832, 144), 'Bagdad': (586, 163), 'Medine': (575, 191), 'Marrakech': (426, 174), 'Toronto': (215, 125), 'Anadyr': (901, 51), 'Helsinki': (518, 63), 'Wellington': (977, 441), 'Detroit': (198, 132), 'Tunis': (476, 151), 'Stockholm': (495, 70), 'Calcutta': (731, 199), 'Nairobi': (572, 283), 'Montreal': (244, 114), 'Kaboul': (670, 162), 'Reykjavik': (404, 53), 'Lima': (197, 328), 'Sofia': (521, 128), 'Chicago': (177, 132), 'Shanghai': (828, 173), 'Winnipeg': (190, 97), 'Londres': (449, 97), 'Copenhague': (484, 84), 'Mascate': (633, 202), 'Buenos Aires': (266, 416), 'Ankara': (548, 141), 'Manille': (842, 235), 'Jakarta': (800, 313)}
    # {'Damas': (567, 162), 'Kiev': (534, 101), 'Istanbul': (532, 136), 'Paris': (455, 110), 'Oslo': (481, 67), 'Copenhague': (484, 84), 'Mascate': (633, 202), 'Moscou': (558, 83), 'Berlin': (489, 100), 'Athenes': (520, 147), 'Tanger': (431, 159), 'Bagdad': (586, 163), 'Helsinki': (518, 63), 'Barcelone': (455, 132), 'Rome': (490, 133), 'Tunis': (476, 151), 'Stockholm': (495, 70), 'Oran': (447, 157), 'Kaboul': (670, 162), 'Reykjavik': (404, 53), 'Le Caire': (545, 179), 'Sofia': (521, 128), 'Seville': (432, 145), 'La Mecque': (578, 206), 'Jerusalem': (560, 170)}

    """
    ###
        Constantes Ville :
    ###
    """

    taille_ville = (15, 10)
    taille_sprite_ville_x = 64
    taille_sprite_ville_y = 31
    pos_pixel_bord_bas_gauche_case = 32
    angle_rotation = 45
    vitesse_mouvement_ville_0 = 2
    aceleration_mouvement_ville = 0.1
    taille_font_rect_mini_fen_ville = 13

    stat_cout = "cout"
    nom_type = "type"
    stat_achete = "acheté"
    stat_occupe = "occupe"
    tabl_stats = [stat_cout]

    type_maison = "Maison"
    val_min_cout_type_maison = 100000
    val_max_cout_type_maison = 500000

    type_appartement_small = "Petit appartement"
    val_min_cout_type_appartement_small = 50000
    val_max_cout_type_appartement_small = 250000

    type_appartement_tall = "Grand appartement"
    val_min_cout_type_appartement_tall = 200000
    val_max_cout_type_appartement_tall = 1000000

    type_buildings = "Appartement luxieux"
    val_min_cout_type_buildings = 500000
    val_max_cout_type_buildings = 1000000

    nom_sprite_terrain = os.path.join(sprites_path, "city", "sol", "sol.png")
    nom_sprite_terrain_montagne = os.path.join(
        sprites_path, "city", "sol", "sol_mountain.png"
    )
    nom_sprite_terrain_champ_1 = os.path.join(
        sprites_path, "city", "sol", "sol_champ1.png"
    )
    nom_sprite_terrain_champ_2 = os.path.join(
        sprites_path, "city", "sol", "sol_champ2.png"
    )
    nom_sprite_terrain_champ_3 = os.path.join(
        sprites_path, "city", "sol", "sol_champ3.png"
    )
    nom_sprite_foret = os.path.join(sprites_path, "city", "sol", "Wood.png")

    nom_sprite_route_x = os.path.join(
        sprites_path, "city", "sol", "Road1.1.png"
    )
    nom_sprite_route_y = os.path.join(
        sprites_path, "city", "sol", "Road0.1.png"
    )
    nom_sprite_route_croisement = os.path.join(
        sprites_path, "city", "sol", "croisement.1.png"
    )
    noms_sprites_route = [
        nom_sprite_route_x,
        nom_sprite_route_y,
        nom_sprite_route_croisement,
    ]
    noms_sprites_deco = [
        nom_sprite_route_x,
        nom_sprite_route_y,
        nom_sprite_route_croisement,
        nom_sprite_foret,
    ]

    """
    ###
        Constantes Resto :
    ###
    """
    spawn_restaurant = (3, 7)

    profondeur_pathfinding = 20

    delai_deplacement_client = 0.5
    delai_spawn_client = 3
    delai_gestion_client_en_caisse = 2
    delai_repas_client = 10

    long_barre_chargement = 11
    hauteur_barre_chargement = 5

    nom_biblio_position = "position"
    nom_biblio_client_geree_en_caisse = "client_geree_en_caisse"
    nom_biblio_temps_depart_client_geree_en_caisse = (
        "temps_depart_client_geree_en_caisse"
    )

    nb_client_attente_caisse = 3

    couleur_rect_boutons = (0, 0, 0)
    largeur_bouton_resto = 16
    taille_bouton = (largeur_bouton_resto, largeur_bouton_resto)

    taille_case_resto = 16
    taille_sprite_resto = 16
    taille_restaurant = (8, 8)

    nom_biblio_sprite = "sprite"
    nom_biblio_walkable = "walkable"
    nom_biblio_est_objectif = "est_objectif"

    sprite_mur = os.path.join(sprites_path, "restaurant", "wall.png")
    sprite_sol = os.path.join(sprites_path, "restaurant", "floor_1.png")

    sprite_evier = os.path.join(sprites_path, "restaurant", "Evier.png")
    sprite_table_de_travail = os.path.join(
        sprites_path, "restaurant", "Table_de_travail.png"
    )
    sprite_comptoir = os.path.join(sprites_path, "restaurant", "Comptoir.png")
    sprite_machine_kebab_1 = os.path.join(
        sprites_path, "restaurant", "Machine_kebab_1.png"
    )
    sprite_machine_kebab_2 = os.path.join(
        sprites_path, "restaurant", "Machine_kebab_2.png"
    )
    sprite_caisse = os.path.join(sprites_path, "restaurant", "caisse_up.png")
    sprite_table_simple = os.path.join(
        sprites_path, "restaurant", "Table_simple.png"
    )
    sprite_tapis_1 = os.path.join(sprites_path, "restaurant", "carpet.png")

    liste_cuisines = [sprite_machine_kebab_1]

    sprite_meuble_1 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_1.png"
    )
    sprite_meuble_2 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_2.png"
    )
    sprite_meuble_3 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_3.png"
    )
    sprite_meuble_4 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_4.png"
    )
    sprite_meuble_5 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_5.png"
    )
    sprite_meuble_6 = os.path.join(
        sprites_path, "restaurant", "furniture", "Meuble_6.png"
    )

    sprite_chaise_left = os.path.join(
        sprites_path, "restaurant", "chaise_1_left.png"
    )
    sprite_chaise_right = os.path.join(
        sprites_path, "restaurant", "chaise_1_right.png"
    )
    sprite_chaise_up = os.path.join(
        sprites_path, "restaurant", "chaise_1_up.png"
    )
    sprite_chaise_down = os.path.join(
        sprites_path, "restaurant", "chaise_1_down.png"
    )
    sprites_chaise = [
        sprite_chaise_up,
        sprite_chaise_down,
        sprite_chaise_left,
        sprite_chaise_right,
    ]
    sprites_african_m_2 = get_character_sprites_paths(
        sprites_path, "african", "m"
    )
    sprites_african_f_2 = get_character_sprites_paths(
        sprites_path, "african", "f"
    )

    sprites_asian_m_1 = get_character_sprites_paths(sprites_path, "asian", "m")
    sprites_asian_f_1 = get_character_sprites_paths(sprites_path, "asian", "f")

    sprites_european_m_1 = get_character_sprites_paths(
        sprites_path, "european", "m"
    )
    sprites_european_f_1 = get_character_sprites_paths(
        sprites_path, "european", "f"
    )

    sprites_joueur = sprites_african_f_2

    """
        PLATS

    """
    # RESSOURCES

    # Bases
    nom_pain = "pain"
    nom_galette = "galette"
    nom_pate_pizza = "pate_pizza"

    # Viandes
    nom_viande_kebab = "viande_kebab"
    nom_jambon = "jambon"
    nom_poulet = "poulet"
    nom_merguez = "merguez"
    nom_saucisse = "saucisse"
    nom_dinde = "dinde"
    nom_steak = "steak"
    nom_nugget = "nugget"
    nom_thon = "thon"
    nom_saumon = "saumon"
    nom_oeuf = "oeuf"

    # Légumes
    nom_oignon = "oignon"
    nom_tomate = "tomate"
    nom_salade = "salade"
    nom_concombre = "concombre"
    nom_poivron = "poivron"
    nom_patate = "patate"
    nom_olive = "olive"
    nom_champignon = "champignon"

    # Divers
    nom_sauce = "sauce"  # Nom de l'indice de la bibliothque

    nom_creme = "creme"
    nom_herbes = "herbes"
    nom_beurre = "beurre"
    nom_soda = "soda"
    nom_fromage = "fromage"

    # RECETTES

    # SAUCES

    nom_algerienne = "algerienne"
    nom_samourai = "samourai"
    nom_sauce_europeanhe = "sauce europeanhe"
    nom_mayonnaise = "mayonnaise"
    nom_ketchup = "ketchup"
    sauces = [
        nom_algerienne,
        nom_samourai,
        nom_sauce_europeanhe,
        nom_mayonnaise,
        nom_ketchup,
    ]

    # KEBABS

    # Simple :
    nom_kebab_simple = "kebab_simple"
    prix_kebab_simple = 6
    ressources_kebab_simple = {
        nom_pain: 1,
        nom_viande_kebab: 1,
        nom_oignon: 1,
        nom_tomate: 1,
        nom_salade: 1,
        nom_sauce: 1,
    }

    # Pita :
    nom_kebab_pita = "pita"
    prix__kebab_pita = 6
    ressources__kebab_pita = {
        nom_galette: 1,
        nom_viande_kebab: 1,
        nom_oignon: 1,
        nom_tomate: 1,
        nom_salade: 1,
        nom_sauce: 1,
    }

    # Kebab_Sans_Crudites :
    nom_kebab_sans_crudites = "kebab_sans_crudites"
    prix_kebab_sans_crudites = 4.5
    ressources_kebab_sans_crudites = {
        nom_pain: 1,
        nom_viande_kebab: 1,
        nom_salade: 1,
        nom_sauce: 1,
    }

    # SANDWICHS

    # Jambon :
    nom_sandwich_jambon = "sandwich_jambon"
    prix_sandwich_jambon = 3
    ressources_sandwich_jambon = {nom_pain: 1, nom_jambon: 1, nom_beurre: 1}

    # Crudites :
    nom_sandwich_crudites = "sandwich_crudites"
    prix_sandwich_crudites = 4.5
    ressources_sandwich_crudites = {
        nom_pain: 1,
        nom_thon: 1,
        nom_oeuf: 1,
        nom_tomate: 1,
        nom_salade: 1,
        nom_sauce: 1,
    }

    # Vegetarien :
    nom_sandwich_vegetarien = "sandwich_vegetarien"
    prix_sandwich_vegetarien = 5
    ressources_sandwich_vegetarien = {
        nom_pain: 1,
        nom_salade: 1,
        nom_sauce: 1,
        nom_tomate: 1,
        nom_concombre: 1,
        nom_fromage: 1,
    }

    # Poulet :
    nom_sandwich_poulet = "sandwich_poulet"
    prix_sandwich_poulet = 5
    ressources_sandwich_poulet = {
        nom_pain: 1,
        nom_poulet: 1,
        nom_beurre: 1,
        nom_tomate: 1,
        nom_fromage: 1,
    }

    # Merguez :
    nom_sandwich_merguez = "sandwich_merguez"
    prix_sandwich_merguez = 4.5
    ressources_sandwich_merguez = {nom_pain: 1, nom_merguez: 1, nom_sauce: 1}

    # Saumon :
    nom_sandwich_saumon = "sandwich_saumon"
    prix_sandwich_saumon = 4.5
    ressources_sandwich_saumon = {
        nom_pain: 1,
        nom_saumon: 1,
        nom_salade: 1,
        nom_tomate: 1,
    }

    # BURGERS

    # Simple :
    nom_burger_simple = "burger_simple"
    prix_burger_simple = 5
    ressources_burger_simple = {
        nom_pain: 1,
        nom_steak: 1,
        nom_fromage: 1,
        nom_sauce: 1,
        nom_salade: 1,
    }

    # Double :
    nom_burger_double = "burger_double"
    prix_burger_double = 7
    ressources_burger_double = {
        nom_pain: 1,
        nom_steak: 2,
        nom_fromage: 2,
        nom_salade: 1,
        nom_sauce: 1,
    }

    # Vegetarien :
    nom_burger_vegetarien = "burger_vegetarien"
    prix_burger_vegetarien = 6
    ressources_burger_vegetarien = {
        nom_pain: 1,
        nom_tomate: 1,
        nom_fromage: 1,
        nom_poivron: 1,
        nom_patate: 1,
        nom_sauce: 1,
    }

    # PANINIS

    # Fromage :
    nom_panini_fromage = "panini_fromage"
    prix_panini_fromage = 4
    ressources_panini_fromage = {nom_pain: 1, nom_fromage: 2}

    # Saumon :
    nom_panini_saumon = "panini_saumon"
    prix_panini_saumon = 6
    ressources_panini_saumon = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_saumon: 1,
        nom_herbes: 1,
        nom_tomate: 1,
        nom_sauce: 1,
    }

    # Jambon :
    nom_panini_jambon = "panini_jambon"
    prix_panini_jambon = 3.5
    ressources_panini_jambon = {nom_pain: 1, nom_fromage: 1, nom_jambon: 1}

    # Poulet :
    nom_panini_poulet = "panini_poulet"
    prix_panini_poulet = 4
    ressources_panini_poulet = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_poulet: 1,
        nom_tomate: 1,
    }

    # Italien :
    nom_panini_italien = "panini_italien"
    prix_panini_italien = 5.5
    ressources_panini_italien = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_jambon: 1,
        nom_herbes: 1,
        nom_sauce: 1,
        nom_tomate: 1,
    }

    # TACOS

    # Poulet :
    nom_taco_poulet = "taco_poulet"
    prix_taco_poulet = 4.5
    ressources_taco_poulet = {
        nom_galette: 1,
        nom_poulet: 1,
        nom_sauce: 1,
        nom_fromage: 1,
        nom_oeuf: 1,
    }

    # Steak :
    nom_taco_steak = "taco_steak"
    prix_taco_steak = 4.5
    ressources_taco_steak = {
        nom_galette: 1,
        nom_steak: 1,
        nom_sauce: 1,
        nom_fromage: 1,
        nom_tomate: 1,
    }

    # Merguez :
    nom_taco_merguez = "taco_merguez"
    prix_taco_merguez = 4
    ressources_taco_merguez = {
        nom_galette: 1,
        nom_merguez: 1,
        nom_sauce: 1,
        nom_fromage: 1,
        nom_poivron: 1,
    }

    # Nugget :
    nom_taco_nugget = "taco_nugget"
    prix_taco_nugget = 4
    ressources_taco_nugget = {
        nom_galette: 1,
        nom_nugget: 1,
        nom_sauce: 1,
        nom_fromage: 1,
    }

    # BAGELS

    # Dinde :
    nom_bagel_dinde = "bagel_dinde"
    prix_bagel_dinde = 5.5
    ressources_bagel_dinde = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_dinde: 1,
        nom_salade: 1,
        nom_concombre: 1,
    }

    # Thon :
    nom_bagel_thon = "bagel_thon"
    prix_bagel_thon = 6
    ressources_bagel_thon = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_thon: 1,
        nom_salade: 1,
        nom_concombre: 1,
    }

    # Saumon :
    nom_bagel_saumon = "bagel_saumon"
    prix_bagel_saumon = 6.5
    ressources_bagel_saumon = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_saumon: 1,
        nom_herbes: 1,
    }

    # Jambon :
    nom_bagel_jambon = "bagel_jambon"
    prix_bagel_jambon = 5
    ressources_bagel_jambon = {
        nom_pain: 1,
        nom_fromage: 1,
        nom_jambon: 1,
        nom_herbes: 1,
    }

    # Steak :
    nom_bagel_steak = "bagel_steak"
    prix_bagel_steak = 6
    ressources_bagel_steak = {
        nom_pain: 1,
        nom_steak: 1,
        nom_creme: 1,
        nom_tomate: 1,
    }

    # HOTDOGS

    # Simple :
    nom_hotdog_simple = "hotdog_simple"
    prix_hotdog_simple = 4
    ressources_hotdog_simple = {nom_pain: 1, nom_saucisse: 1}

    # Double :
    nom_hotdog_double = "hotdog_double"
    prix_hotdog_double = 5
    ressources_hotdog_double = {nom_pain: 1, nom_saucisse: 2, nom_sauce: 1}

    # Merguez :
    nom_hotdog_merguez = "hotdog_merguez"
    prix_hotdog_merguez = 4
    ressources_hotdog_merguez = {nom_pain: 1, nom_merguez: 1, nom_sauce: 1}

    # PIZZAS

    # 4 Fromages :
    nom_pizza_4_fromages = "pizza_4_fromages"
    prix_pizza_4_fromages = 5
    ressources_pizza_4_fromages = {
        nom_pate_pizza: 1,
        nom_fromage: 4,
        nom_tomate: 1,
    }

    # Margherita :
    nom_pizza_margherita = "pizza_margherita"
    prix_pizza_margherita = 5
    ressources_pizza_margherita = {
        nom_pate_pizza: 1,
        nom_fromage: 2,
        nom_tomate: 1,
        nom_olive: 1,
        nom_creme: 1,
    }

    # Reine :
    nom_pizza_reine = "pizza_reine"
    prix_pizza_reine = 4.5
    ressources_pizza_reine = {
        nom_pate_pizza: 1,
        nom_fromage: 1,
        nom_tomate: 1,
        nom_jambon: 1,
    }

    # Vegetarienne :
    nom_pizza_vegetarienne = "pizza_vegetarienne"
    prix_pizza_vegetarienne = 6
    ressources_pizza_vegetarienne = {
        nom_pate_pizza: 1,
        nom_fromage: 1,
        nom_tomate: 1,
        nom_poivron: 1,
        nom_oignon: 1,
        nom_olive: 1,
        nom_creme: 1,
        nom_champignon: 1,
    }

    # Baltique :
    nom_pizza_baltique = "pizza_baltique"
    prix_pizza_baltique = 5.5
    ressources_pizza_baltique = {
        nom_pate_pizza: 1,
        nom_fromage: 1,
        nom_tomate: 1,
        nom_creme: 1,
        nom_thon: 1,
        nom_saumon: 1,
    }

    # Pecheur :
    nom_pizza_pecheur = "pizza_pecheur"
    prix_pizza_pecheur = 5.5
    ressources_pizza_pecheur = {
        nom_pate_pizza: 1,
        nom_fromage: 1,
        nom_tomate: 1,
        nom_poivron: 1,
        nom_thon: 1,
        nom_olive: 1,
    }

    # Norvegienne :
    nom_pizza_norvegienne = "pizza_norvegienne"
    prix_pizza_norvegienne = 5.5
    ressources_pizza_norvegienne = {
        nom_pate_pizza: 1,
        nom_fromage: 2,
        nom_saumon: 1,
        nom_creme: 1,
        nom_patate: 1,
    }

    # FRITES

    # Petite :
    nom_frite_petite = "petite frite"
    prix_frite_petite = 1
    ressources_frite_petite = {nom_patate: 1, nom_sauce: 1}

    # Moyenne :
    nom_frite_moyenne = "moyenne frite"
    prix_frite_moyenne = 1.5
    ressources_frite_moyenne = {nom_patate: 2, nom_sauce: 1}

    # PGrande :
    nom_frite_grande = "grande frite"
    prix_frite_grande = 2
    ressources_frite_grande = {nom_patate: 3, nom_sauce: 1}

    biblio_recettes = {
        nom_kebab_simple: (ressources_kebab_simple, prix_kebab_simple),
        nom_frite_grande: (ressources_frite_grande, prix_frite_grande),
        nom_pizza_baltique: (ressources_pizza_baltique, prix_pizza_baltique),
    }

    """
        Personnel:
    """

    african = "african"
    american = "american"
    asian = "asian"
    creole = "creole"
    european = "european"
    indian = "indian"
    latin_american = "latin_american"
    scandinavian = "scandinavian"

    ethnic_table = [
        african,
        american,
        asian,
        creole,
        european,
        indian,
        latin_american,
        scandinavian,
    ]

    man = "m"
    woman = "w"

    tableau_sexe = [man, woman]

    african_woman_names = ["Vumi", "Ima"]
    african_man_names = ["Elikia", "Nsi"]

    arabic_woman_names = ["Saïda", "Yasmina"]
    arabic_man_names = ["Djibril", "Younes"]

    asian_woman_names = ["Hisae", "Yumiko"]
    asian_man_names = ["Genjiro", "Ryoichi"]

    european_woman_names = ["Marie", "Lucie"]
    european_man_names = ["Claude", "Quentin"]

    nom_stat_cuisine = "stat. cuisine"
    nom_stat_nettoyage = "stat. nettoyage"
    nom_stat_vente = "stat. vente"
    tabeau_noms_stats = [nom_stat_cuisine, nom_stat_nettoyage, nom_stat_vente]

    nom_job_cuisinier = "job_cuisinier"
    nom_job_service = "job_service"
    nom_job_nettoyage = "job_nettoyage"

    sprite_tache = os.path.join(sprites_path, "restaurant", "stain.png")

    # chef_cuisinier:
    nom_categorie_chef_cuisinier = "chef-cuisinier"
    fourchette_valeurs_cuisine_chef_cuisinier = (70, 90)
    fourchette_valeurs_nettoyage_chef_cuisinier = (50, 70)
    fourchette_valeurs_vente_chef_cuisinier = (30, 60)
    tabeau_valeurs_stats_chef_cuisinier = [
        fourchette_valeurs_cuisine_chef_cuisinier,
        fourchette_valeurs_nettoyage_chef_cuisinier,
        fourchette_valeurs_vente_chef_cuisinier,
    ]

    # cuisinier:
    nom_categorie_cuisinier = "cuisinier"
    fourchette_valeurs_cuisine_cuisinier = (50, 70)
    fourchette_valeurs_nettoyage_cuisinier = (20, 50)
    fourchette_valeurs_vente_cuisinier = (20, 40)
    tabeau_valeurs_stats_cuisinier = [
        fourchette_valeurs_cuisine_cuisinier,
        fourchette_valeurs_nettoyage_cuisinier,
        fourchette_valeurs_vente_cuisinier,
    ]

    # caissier:
    nom_categorie_caissier = "caissier"
    fourchette_valeurs_cuisine_caissier = (10, 30)
    fourchette_valeurs_nettoyage_caissier = (30, 50)
    fourchette_valeurs_vente_caissier = (50, 80)
    tabeau_valeurs_stats_caissier = [
        fourchette_valeurs_cuisine_caissier,
        fourchette_valeurs_nettoyage_caissier,
        fourchette_valeurs_vente_caissier,
    ]

    # ballayeur:
    nom_categorie_ballayeur = "ballayeur"
    fourchette_valeurs_cuisine_ballayeur = (10, 20)
    fourchette_valeurs_nettoyage_ballayeur = (40, 70)
    fourchette_valeurs_vente_ballayeur = (5, 20)
    tabeau_valeurs_stats_ballayeur = [
        fourchette_valeurs_cuisine_ballayeur,
        fourchette_valeurs_nettoyage_ballayeur,
        fourchette_valeurs_vente_ballayeur,
    ]

    # none:
    nom_categorie_autres = None
    noms_categorie_autres = ["dealer", "sans-emploi", "camionneur"]
    fourchette_valeurs_cuisine_None = (10, 30)
    fourchette_valeurs_nettoyage_None = (20, 40)
    fourchette_valeurs_vente_None = (0, 40)
    tabeau_valeurs_stats_None = [
        fourchette_valeurs_cuisine_None,
        fourchette_valeurs_nettoyage_None,
        fourchette_valeurs_vente_None,
    ]

    nom_caracteristiques = [
        nom_categorie_chef_cuisinier,
        nom_categorie_cuisinier,
        nom_categorie_caissier,
        nom_categorie_ballayeur,
        nom_categorie_autres,
    ]
    noms_categories_femmes = {
        nom_categorie_chef_cuisinier: "chef-cuisinière",
        nom_categorie_caissier: "caissiere",
        nom_categorie_cuisinier: "cuisinière",
        nom_categorie_ballayeur: "ballayeuse",
        nom_categorie_autres: "femme au foyer",
    }
