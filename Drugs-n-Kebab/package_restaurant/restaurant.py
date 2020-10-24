# coding: utf8
from constantes import Constantes
import affichage
import time

class Restaurant:
    
    #Constructeur:
    def __init__(self,grille):
        self.gains = 0
        self.pertes = 0
        self.clients = []
        self.employes = []
        self.grille_meubles = grille
        
        self.pos_caisses = self.get_positions_caisses()
        """
        self.client_geree_en_caisse = False
        self.temps_depart_client_geree_en_caisse = None
        """
        self.proprete = 100
        
        self.commande_geree = None
        self.cuisinee = True
        
        #"Ressources du restaurant"
        self.ressources = {Constantes.nom_pain : 10,Constantes.nom_viande_kebab : 10,Constantes.nom_oignon:10, Constantes.nom_tomate:10, Constantes.nom_salade:10,Constantes.nom_galette:10, Constantes.nom_patate: 0, Constantes.nom_algerienne : 10, Constantes.nom_samourai : 10, Constantes.nom_sauce_blanche : 10, Constantes.nom_mayonnaise : 10, Constantes.nom_ketchup : 10,Constantes.nom_pate_pizza: 1,Constantes.nom_fromage: 10,Constantes.nom_tomate: 10,Constantes.nom_creme: 10,Constantes.nom_thon: 10,Constantes.nom_saumon: 10}
        return
    
    def cuisine(self):
        if self.commande_geree != None:
            (commande,sauce) = self.commande_geree
            #nom_commande = commande[0]
            ingredients = commande[1][0]
            prix = commande[1][1]
            presence_sauce = False
            for ingredient in ingredients:
                if ingredient == Constantes.nom_sauce :
                    presence_sauce
                else:
                    nombre_ingredient = ingredients[ingredient]
                    self.ressources[ingredient] -= nombre_ingredient
            if presence_sauce :
                self.ressources[sauce] -= ingredients[Constantes.nom_sauce]
            self.gains += prix
            self.commande_geree = None
            self.cuisinee = True
        return
    
    def test_ressources_suffisantes(self,commande_client,sauce_client):
        # commande_client = (nom_commande,ressources_necessaires,prix)
        ressources_commande = commande_client[1][0]
        test = True
        for nom_ressource in ressources_commande:
            if nom_ressource != Constantes.nom_sauce:
                test = test and ressources_commande[nom_ressource] <= self.ressources[nom_ressource]
            else:
                test = test and ressources_commande[nom_ressource] <= self.ressources[sauce_client]
        return test
    
    def recevoir_commande(self,commande,sauce):
        if self.test_ressources_suffisantes(commande,sauce):
            self.commande_geree = (commande,sauce)
            self.cuisinee = False
        return
    
    def generation_bibliotheque(self,pos):
        bibliotheque = {}
        bibliotheque[Constantes.nom_biblio_position] = pos
        bibliotheque[Constantes.nom_biblio_client_geree_en_caisse] = False
        bibliotheque[Constantes.nom_biblio_temps_depart_client_geree_en_caisse] = None
        return bibliotheque

    def get_positions_caisses(self):
        liste_biblio = []
        for x in range(0,len(self.grille_meubles)):
            for y in range(0,len(self.grille_meubles[0])):
                if self.grille_meubles[x][y][Constantes.nom_biblio_sprite] == Constantes.sprite_caisse:
                    liste_biblio.append(self.generation_bibliotheque((x,y)))
        return liste_biblio
    
    def get_positions_cuisines(self):
        tabl = []
        for x in range(0,len(self.grille_meubles)):
            for y in range(0,len(self.grille_meubles[0])):
                if self.grille_meubles[x][y][Constantes.nom_biblio_sprite] in Constantes.liste_cuisines:
                    tabl.append((x,y))
        return tabl
    
    def gestion_client_en_caisse(self,biblio_caisse,fenetre,font,temps,joueur = None,action_du_joueur = False):
        
        if biblio_caisse != None :
            (x,y) = biblio_caisse[Constantes.nom_biblio_position]
            if biblio_caisse[Constantes.nom_biblio_temps_depart_client_geree_en_caisse] != None and temps.get_time() >= biblio_caisse[Constantes.nom_biblio_temps_depart_client_geree_en_caisse]+Constantes.delai_gestion_client_en_caisse:
                client = self.get_client_en_caisse((x,y+1))
                biblio_caisse[Constantes.nom_biblio_client_geree_en_caisse] = False
                biblio_caisse[Constantes.nom_biblio_temps_depart_client_geree_en_caisse] = None
                commandes_client = client.get_commandes()
                commande_sauce = commandes_client[1]
                commandes = commandes_client[1]
                quitter_resto = False
                if action_du_joueur:
                    if joueur.action_termine:
                        commande_effective = affichage.mini_fenetre_commande(self,temps,commandes_client,fenetre,font)
                        if commande_effective != None :
                            self.recevoir_commande(commande_effective,commande_sauce)
                            client.commande_donnee = True
                        else:
                            quitter_resto = True
                else:
                    commande_trouvee = False
                    i = 0
                    commande_effective = commandes[i]
                    while i < len(commandes_client):
                        if self.test_ressources_suffisantes(commande_effective,commande_sauce):
                            commande_effective = commandes[i]
                            commande_trouvee = True
                        i +=1
                    if commande_trouvee:
                        self.recevoir_commande(commande_effective,commande_sauce)
                    
                if client != None :
                    if quitter_resto:
                        client.coordonnees_objectif = None
                        client.quitter_resto()
            elif action_du_joueur and not(joueur.action):
                biblio_caisse[Constantes.nom_biblio_client_geree_en_caisse] = False
                biblio_caisse[Constantes.nom_biblio_temps_depart_client_geree_en_caisse] = None
        else:
            for biblio in self.pos_caisses:
                biblio[Constantes.nom_biblio_client_geree_en_caisse] = False
                biblio[Constantes.nom_biblio_temps_depart_client_geree_en_caisse] = None
        return False
    
    def get_client_en_caisse(self,position_devant_caisse):
        for client in self.clients:
            if client.position == position_devant_caisse:
                return client