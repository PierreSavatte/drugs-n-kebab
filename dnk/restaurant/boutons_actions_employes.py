import time

from .. import main_fonctions
from ..constants import Constantes


class Boutons_actions_employes:
    def __init__(self, font, employe, position_depart, restaurant, temps):
        self.employe_lie = employe
        self.restaurant = restaurant
        self.boutons = self.get_boutons(font, position_depart)
        self.fin = False
        self.temps_appartition = time.time()
        return

    def return_cuisine(self):
        if self.test_temps():
            self.employe_lie.get_ordre(
                Constantes.nom_stat_cuisine, self.restaurant
            )
            self.fin = True

    def return_nettoyage(self):
        if self.test_temps():
            self.employe_lie.get_ordre(
                Constantes.nom_stat_nettoyage, self.restaurant
            )
            self.fin = True

    def return_vente(self):
        if self.test_temps():
            self.employe_lie.get_ordre(
                Constantes.nom_stat_vente, self.restaurant
            )
            self.fin = True

    def test_temps(self):
        return time.time() >= self.temps_appartition + 0.2

    def Update(self, fenetre, pos_mouse_clic):
        for bouton in self.boutons:
            bouton.Update(fenetre, pos_mouse_clic)
        if pos_mouse_clic is not None and self.test_temps():
            self.fin = True
        return

    def get_boutons(self, font, position_depart):
        tabl = []
        position_y = position_depart[0]
        for (texte, fonction) in [
            ("Cuisine", self.return_cuisine),
            ("Nettoyage", self.return_nettoyage),
            ("Accueil en caisse", self.return_vente),
        ]:
            tabl.append(
                main_fonctions.Bouton(
                    font,
                    (position_depart[0], position_y),
                    texte,
                    fonction,
                    resize=0.75,
                )
            )
            position_y += tabl[len(tabl) - 1].get_hauteur() + 5
        return tabl
