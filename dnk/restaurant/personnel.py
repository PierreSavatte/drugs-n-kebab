import random

from .individu import Individu
from .. import main_fonctions
from ..constantes import Constantes


class Personnel(Individu):

    # Constructeur:
    def __init__(
        self,
        couleur,
        sexe,
        categorie_arg,
        biblios_caisses,
        couleur_argument,
        sexe_arg,
    ):
        """
        @param categorie_arg: catégorie de l'employé, chaine de caractère
        @param est_homme_arg: booleen qui decrit si l'employé est un homme
        """
        self.categorie = categorie_arg
        self.categorie_a_afficher = self.def_categorie_a_afficher(
            categorie_arg, sexe
        )
        self.statistiques = self.def_stats(categorie_arg)
        self.experience = [0, 0, 0]

        self.objectif = None

        self.action = False
        self.action_termine = False
        self.stat_liee = None
        self.stat_en_jeu = None
        self.temps_debut_action = None

        self.biblio_caisses = biblios_caisses
        self.biblio_caisse_liee = None

        self.en_boucle = True

        super().__init__(couleur_argument, sexe_arg)

    def get_biblio_caisse_liee(self, position_arg):
        if self.stat_liee == Constantes.nom_stat_vente:
            for biblio in self.biblio_caisses:
                position = biblio[Constantes.nom_biblio_position]
                if position_arg == (position[0], position[1] - 1):
                    return biblio
        return

    def get_ordre(self, stat, restaurant):
        if not (self.action):
            if stat == Constantes.nom_stat_cuisine:
                objectif_temp = Constantes.sprite_machine_kebab_1
            elif stat == Constantes.nom_stat_nettoyage:
                objectif_temp = Constantes.sprite_tache
            elif stat == Constantes.nom_stat_vente:
                objectif_temp = Constantes.sprite_caisse
            self.objectif = objectif_temp
            self.stat_liee = stat
            retourne = self.modifier_chemin(
                restaurant,
                objectif_temp,
                Individu.tabl_positions,
                est_personnel=True,
            )

            if len(self.chemin) != 0:
                pos_employe_en_caisse = self.chemin[-1]
                self.biblio_caisse_liee = self.get_biblio_caisse_liee(
                    pos_employe_en_caisse
                )

            if stat == Constantes.nom_stat_nettoyage and not (retourne):
                print("Rien a nettoyer")
                self.objectif = None
        else:
            print("DEJA OCCUPE")

    """def get_position_taches(self,grille_meubles):
        for x in range(len(grille_meubles)):
            for y in range(len(grille_meubles[0])):
                if grille_meubles[x][y] == Constantes.sprite_tache:
                    return (x,y)"""

    def Update(self, temps, restaurant, fenetre, font):
        if not self.action:
            if self.position == self.coordonnees_objectif:
                if not self.action_termine:
                    if self.stat_liee == Constantes.nom_stat_cuisine:
                        if restaurant.commande_geree is not None:
                            self.debut_action(temps)
                        else:
                            print("En attente d'une commande")
                    if self.stat_liee == Constantes.nom_stat_vente:
                        restaurant.gestion_client_en_caisse(
                            self.biblio_caisse_liee, fenetre, font, temps
                        )
                        if self.biblio_caisse_liee[
                            Constantes.nom_biblio_client_geree_en_caisse
                        ]:
                            self.debut_action()
                        else:
                            print("En attente de clients")
        else:
            self.continue_action(temps)

        if not self.action and self.action_termine:
            self.action_termine = False
            if self.stat_liee == Constantes.nom_stat_cuisine:
                restaurant.cuisine()
            elif self.stat_liee == Constantes.nom_stat_nettoyage:
                print("Fin nettoyage")
            elif self.stat_liee == Constantes.nom_stat_vente:
                print("Fin vente")
            if self.en_boucle:
                self.debut_action(temps)
            else:
                self.clean_objectifs()
        return

    def get_objectif(self):
        objectif_temp = self.objectif
        test = objectif_temp != self.objectif
        if test:
            self.objectif = objectif_temp
        return test

    def continue_action(self, temps):
        if self.action:
            temps_action = self.get_temps_stat(self.stat_liee)
            if temps.get_time() >= self.temps_debut_action + temps_action:
                self.experience_up(self.stat_liee)
            else:
                self.experience_up(self.stat_liee, valeur=10)
                self.action = False
                self.temps_debut_action = None
                self.action_termine = True
        return

    def debut_action(self, temps):
        self.stat_en_jeu = self.stat_liee
        self.temps_debut_action = temps.get_time()
        self.action = True
        return

    def experience_up(self, stat, valeur=1):
        i = Constantes.tabeau_noms_stats.index(stat)
        self.experience[i] += valeur
        if self.experience[i] >= 1500:
            self.experience[i] = 0
            self.level_up(stat)
        return

    def level_up(self, nom_stat):
        if nom_stat in Constantes.tabeau_noms_stats:
            self.statistiques[nom_stat] += int(
                5000 / self.statistiques[Constantes.nom_stat_cuisine]
            )
        return

    def get_temps_action(self):
        return self.get_temps_stat(self.stat_liee)

    def get_level_stat(self, stat):
        if stat in Constantes.tabeau_noms_stats:
            return int(self.statistiques[stat] / 5)

    def get_temps_stat(self, stat):
        if stat in Constantes.tabeau_noms_stats:
            return 1000 / self.statistiques[stat]

    def def_categorie_a_afficher(self, categorie_arg, sexe):
        """
        Fonction qui attribue la catégorie a afficher pour l'employé. Elle permet surtout de donner un nom de catégorie feminin à une femme
        @param categorie_arg: catégorie de l'employé, chaine de caractère
        @param est_homme_arg: booleen qui decrit si l'employé est un homme
        @return: une chaine de caractère contenant le nom de la catégorie à afficher
        """
        if sexe == Constantes.nom_homme:
            if categorie_arg is None:
                return self.main_fonctions.get_val_aleatoire_parmis(
                    Constantes.noms_categorie_autres
                )
            else:
                return categorie_arg
        else:
            return Constantes.noms_categories_femmes[categorie_arg]

    def def_stats(self, categorie_arg):
        """
        Fonction qui attribue des stats en fonction de la catégorie d'un employé
        @param categorie_arg: catégorie de l'employé, chaine de caractère
        @return: une bibliotheque de statistiques de l'employé
        """
        caracteristiques = {}
        if categorie_arg == Constantes.nom_categorie_cuisinier:
            for i in range(len(Constantes.tabeau_noms_stats)):
                caracteristiques[
                    Constantes.tabeau_noms_stats[i]
                ] = main_fonctions.get_valeur_multiple_de_5(
                    random.randint(
                        Constantes.tabeau_valeurs_stats_cuisinier[i][0],
                        Constantes.tabeau_valeurs_stats_cuisinier[i][1],
                    )
                )
        elif categorie_arg == Constantes.nom_categorie_chef_cuisinier:
            for i in range(len(Constantes.tabeau_noms_stats)):
                caracteristiques[
                    Constantes.tabeau_noms_stats[i]
                ] = main_fonctions.get_valeur_multiple_de_5(
                    random.randint(
                        Constantes.tabeau_valeurs_stats_chef_cuisinier[i][0],
                        Constantes.tabeau_valeurs_stats_chef_cuisinier[i][1],
                    )
                )
        elif categorie_arg == Constantes.nom_categorie_caissier:
            for i in range(len(Constantes.tabeau_noms_stats)):
                caracteristiques[
                    Constantes.tabeau_noms_stats[i]
                ] = main_fonctions.get_valeur_multiple_de_5(
                    random.randint(
                        Constantes.tabeau_valeurs_stats_caissier[i][0],
                        Constantes.tabeau_valeurs_stats_caissier[i][1],
                    )
                )
        else:
            for i in range(len(Constantes.tabeau_noms_stats)):
                caracteristiques[
                    Constantes.tabeau_noms_stats[i]
                ] = main_fonctions.get_valeur_multiple_de_5(
                    random.randint(
                        Constantes.tabeau_valeurs_stats_None[i][0],
                        Constantes.tabeau_valeurs_stats_None[i][1],
                    )
                )
        return caracteristiques
