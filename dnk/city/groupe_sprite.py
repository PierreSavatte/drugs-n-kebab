import pygame


class Groupe_sprite:
    def __init__(self):
        self.groupe = pygame.sprite.OrderedUpdates()
        self.tabl_batiment = []
        return

    def add(self, sprite, objet_batiment, coordonnees):
        self.groupe.add(sprite)
        self.tabl_batiment.append((objet_batiment, coordonnees))
        return

    def draw(self, fenetre):
        self.groupe.draw(fenetre)
        return

    def get_indice_bat(self, sprite):
        indice = 0
        indice_a_garder = 0
        for sprite_groupe in self.groupe:
            if sprite.rect.center != sprite_groupe.rect.center:
                indice += 1
            else:
                indice_a_garder = indice
        return indice_a_garder

    def get_pos_tabl(self, sprite):
        indice = self.get_indice_bat(sprite)
        position = self.tabl_batiment[indice][1]
        return position

    def get_stat_batiment(self, sprite):
        indice = self.get_indice_bat(sprite)
        objet_batiment = self.tabl_batiment[indice][0]
        return objet_batiment
