from .individu import Individu
from .. import main_fonctions
from ..constants import Constantes


class Client(Individu):
    def __init__(
        self,
        couleur,
        sexe,
        liste_recettes_debloquees,
        couleur_argument,
        sexe_arg,
    ):
        self.money = 0
        self.a_commande = False
        self.a_mange = False
        self.choix_commande(liste_recettes_debloquees)
        self.commande_donnee = False

        self.temps_depart_repas = None
        super().__init__(couleur_argument, sexe_arg)

    def Update(self, temps, restaurant):
        if self.test_si_mange():
            if self.coordonnees_objectif == self.position:
                if self.temps_depart_repas is None:
                    self.temps_depart_repas = temps.get_time()
                if self.test_si_fini_manger(temps):
                    self.objectif_suivant()
                    self.coordonnees_objectif = None
        elif self.commande_donnee and restaurant.cuisinee:
            self.objectif_suivant()
            self.coordonnees_objectif = None
        return

    def test_si_mange(self):
        return self.a_commande

    def test_si_fini_manger(self, temps):
        return (
            temps.get_time()
            >= self.temps_depart_repas + Constantes.delai_repas_client
        )

    def objectif_suivant(self):
        if not self.a_commande:
            self.a_commande = True
        else:
            if not self.a_mange:
                self.a_mange = True
        return

    def get_objectif(self):
        objectif_temp = self.objectif
        if not self.a_commande:
            objectif_temp = Constantes.sprite_caisse
        else:
            if not self.a_mange:
                objectif_temp = Constantes.sprite_chaise_left
            else:
                objectif_temp = Constantes.sprite_tapis_1
        test = objectif_temp != self.objectif
        if test:
            self.objectif = objectif_temp
        return test

    def choix_commande(self, liste_recettes_debloquees):
        self.commande_sauce = main_fonctions.get_val_aleatoire_parmis(
            Constantes.sauces
        )
        self.commande_1 = main_fonctions.get_val_aleatoire_parmis_bibliotheque(
            liste_recettes_debloquees
        )
        commande_2 = main_fonctions.get_val_aleatoire_parmis_bibliotheque(
            liste_recettes_debloquees
        )
        while commande_2 == self.commande_1:
            commande_2 = main_fonctions.get_val_aleatoire_parmis_bibliotheque(
                liste_recettes_debloquees
            )
        self.commande_2 = commande_2
        return

    def quitter_resto(self):
        self.a_commande = True
        self.a_mange = True
        self.objectif = Constantes.sprite_tapis_1
        return

    def get_commandes(self):
        return (self.commande_1, self.commande_2), self.commande_sauce
