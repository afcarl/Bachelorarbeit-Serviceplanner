# coding=utf-8
'''
In Problem.py werden die verschiedenen Probleme erzeugt, welche geloest werden muessen.
'''

__author__ = 'Sebastian Gehrmann'
import einstellungen
import model
import karten
import names
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import math
import numpy as np
import random
from scipy import stats

from einstellungen import remove_border, set_plt_options


class Problem():
    '''
    Diese Klasse definiert die Eigenschaften eines Problemes
    '''

    def __init__(self, terminarten, karte, techniker, kunden, anzahlTermine):
        # dict mit {Termindauer: (p, std)}
        if terminarten == 1:
            self.terminarten = {1: (0.2, 0.2),
                                2: (0.3, 0.3),
                                3: (0.3, 0.4),
                                4: (0.2, 0.5)}
        else:
            self.terminarten = terminarten
        # Die Karte, auf der modelliert wird
        self.karte = karte
        # array mit Technikern
        if isinstance(techniker, ( int, long )):
            self.techniker = self.generiere_entitaeten(karte, model.Techniker, techniker)
        else:
            self.techniker = techniker
        # array mit Kunden
        if isinstance(kunden, ( int, long )):
            self.kunden = self.generiere_entitaeten(karte, model.Kunde, kunden)
        else:
            self.kunden = kunden
        # Nummer der zu erzeugenden Termine
        self.anzahlTermine = anzahlTermine

        self.termine = []
        self.grundtermine = []
        self.generiere_termine()

        self.validiere_daten()

        set_plt_options()

    def validiere_daten(self):
        # Terminarten sollten immer 1 ergeben und positiv sein
        try:
            gesamtchance = 0
            for k, v in self.terminarten.iteritems():
                if k < 0:
                    raise ValueError("Die Terminart %d ist negativ. Das sollte nicht passieren." % k)
                gesamtchance += v[0]
            if gesamtchance != 1:
                raise ValueError("Die Chancen der Terminarten sollten in Summe 1 ergeben.")
        except:
            raise ValueError(
                "Die Terminarten sollten als Dictionary mit der Form {Termindauer: (p, std)} angegeben werden.")
        # alle Techniker und Kunden muessen auf der Karte sein
        try:
            for t in self.techniker:
                if not self.karte.enthaelt(t.ort) or not self.karte.enthaelt(t.heimatort):
                    raise ValueError("Der Techniker %s ist nicht auf der Karte enthalten" % t.name)
            for k in self.kunden:
                if not self.karte.enthaelt(k.ort):
                    raise ValueError("Der Kunde %s ist nicht auf der Karte enthalten" % k.name)
        except:
            raise ValueError(
                "Die Techniker und Kunden sollten Instanzen von Kunde und Techniker sein und in einem Array gespeichert werden.")

    '''
    GENERIERUNG
    '''

    def generiere_zufallsdaten(self):

        name = names.get_full_name()
        return (name, self.karte.gib_Zufallspunkt())

    def generiere_entitaeten(self, karte, typ, anzahl):
        eintitaeten_array = []
        for i in xrange(anzahl):
            eintitaeten_array.append(typ(*self.generiere_zufallsdaten()))

        return eintitaeten_array

    def generiere_termine(self):
        arten = []
        wahrscheinlichkeiten = []
        for k, v in self.terminarten.iteritems():
            arten.append(k)
            wahrscheinlichkeiten.append(v[0])
        verteilung = stats.rv_discrete(name='verteilung', values=(arten, wahrscheinlichkeiten))
        self.grundtermine = verteilung.rvs(size=self.anzahlTermine)

        for t in self.grundtermine:
            reale_dauer = random.gauss(t, self.terminarten[t][1])
            self.termine.append(model.Termin(random.choice(self.kunden), t, reale_dauer))


    def reset_problem(self):
        for tech in self.techniker:
            tech.reset_tech()

    '''
    VISUALISIERUNG
    '''

    def visualisiere_problem(self):

        set_plt_options()
        # self.karte.vis_karte()
        techniker_x = [x.ort[0] for x in self.techniker]
        techniker_y = [x.ort[1] for x in self.techniker]
        plt.plot(techniker_x, techniker_y, 'D', label='Techniker')

        kunden_x = [x.ort[0] for x in self.kunden]
        kunden_y = [x.ort[1] for x in self.kunden]
        plt.plot(kunden_x, kunden_y, 'o', label='Kunden')

        plt.xlim(-1, self.karte.max_x + 1)
        plt.ylim(-1, self.karte.max_y + 1)

        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(prop=fontP, loc='right', bbox_to_anchor=(1.1, .93),
                   ncol=1, fancybox=True, )

        plt.grid(True)
        remove_border()
        plt.title("Karte der Techniker und Kunden")

        plt.show()

    def visualisiere_grundtermine(self):

        set_plt_options()
        bin_berechnung = np.unique(self.grundtermine) - .5
        bin_berechnung = bin_berechnung.tolist()
        bin_berechnung.append(max(self.grundtermine) + .5)
        plt.hist(self.grundtermine, bins=bin_berechnung)
        plt.xticks([1, 2, 3, 4])
        remove_border()
        plt.grid(axis='y', color='white', linestyle='-')
        plt.title(u"Verteilung der geplanten Terminlängen")
        plt.xlabel("Dauer in Stunden")
        plt.ylabel("Anzahl Termine")
        plt.show()

    def visualisiere_wirkliche_zeit(self):
        wirkliche_dauern = []
        for t in self.termine:
            wirkliche_dauern.append(t.wirkliche_dauer)
        plt.hist(wirkliche_dauern, bins=15)
        remove_border()
        plt.grid(axis='y', color='white', linestyle='-')
        plt.xticks(xrange(int(math.ceil(max(wirkliche_dauern)) + 1)))
        plt.title("Verteilung der wirklichen Dauer")
        plt.xlabel("Dauer in Stunden")
        plt.ylabel("Anzahl Termine")
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    karte = karten.BasisKarte()
    technikerarray = []
    technikerarray.append(model.Techniker('Bryan Moore', (2, 1)))
    technikerarray.append(model.Techniker('Matthew Crawford', (2, 6)))
    technikerarray.append(model.Techniker('David Lowe', (1, 10)))
    technikerarray.append(model.Techniker('Molly Bullock', (4, 7)))
    technikerarray.append(model.Techniker('Edwin Higgins', (8, 0)))
    testproblem = Problem(1, karte, technikerarray, 20, 100)
    testproblem.visualisiere_problem()










