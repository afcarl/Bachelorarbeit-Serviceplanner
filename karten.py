# coding=utf-8
'''
Karten.py beschreibt die Layouts, die Probleme haben koennen.
'''
__author__ = 'Sebastian Gehrmann'
import einstellungen
from einstellungen import remove_border, set_plt_options
from random import randint
import matplotlib.pyplot as plt
from matplotlib import rcParams


class Karte():
    '''
    abstrakte Klasse, die die Methoden einer Klasse definiert
    '''

    def gib_Zufallspunkt(self):
        pass

    def vis_karte(self):
        pass

    def enthaelt(self, koordinaten):
        pass


class BasisKarte(Karte):
    '''
    BasisKarte ist eine 10x10 quadratische Karte
    '''

    def __init__(self):
        self.max_x = 10
        self.max_y = 10

    def gib_Zufallspunkt(self):
        zufalls_x = randint(0, self.max_x)
        zufalls_y = randint(0, self.max_y)
        return (zufalls_x, zufalls_y)

    #plotte eine Karte
    def vis_karte(self):
        set_plt_options()
        x_values = []
        y_values = []
        for x in xrange(self.max_x+1):
            for y in xrange(self.max_y+1):
                x_values.append(x)
                y_values.append(y)
        plt.plot(x_values, y_values, 'rx')
        remove_border()
        plt.xlim(-1,11)
        plt.ylim(-1,11)
        plt.title(u"Karte für das Testproblem")
        plt.xlabel("X-Koordinate")
        plt.ylabel("Y-Koordinate")

        plt.show()

    def enthaelt(self, koordinaten):
        if not 0 <= koordinaten[0] <= self.max_x:
            return False
        if not 0 <= koordinaten[1] <= self.max_y:
            return False
        return True



if __name__ == '__main__':
    karte = BasisKarte()
    karte.vis_karte()


