'''
Model.py beschreibt die Modelle, die in diesem Framework benutzt werden.
'''
__author__ = 'Sebastian Gehrmann'
import einstellungen

class Kunde():
    '''
    Diese Klasse beschreibt verschiedene Kunden
    '''

    def __init__(self, name, ort):
        self.name = name
        self.ort = ort

    def __repr__(self):
        repr_string = self.name + " " + str(self.ort)
        return repr_string

    def __str__(self):
        repr_string = self.name + " " + str(self.ort)
        return repr_string


class Termin():
    '''
    Diese Klasse beschreibt die Dauer eines Termins
    '''

    def __init__(self, kunde, dauer, wirkliche_dauer):
        self.kunde = kunde
        self.dauer = dauer
        self.wirkliche_dauer = wirkliche_dauer

    def __repr__(self):
        repr_string = str(self.kunde) + ": " + str(self.dauer) + "h"
        return repr_string

    def __str__(self):
        repr_string = str(self.kunde) + ": " + str(self.dauer) + "h"
        return repr_string


class Techniker():
    '''
    Diese Klasse beschreibt die Servicetechniker
    '''

    def __init__(self, name, heimatort):
        self.name = name
        self.heimatort = heimatort
        self.ort = heimatort
        self.termine = Terminkalender()

    def gib_termin_fuer_tag(self, tag):
        return self.termine.gib_termine_fuer_tag(tag)

    def reset_tech(self):
        self.termine = Terminkalender()

    def __repr__(self):
        repr_string = self.name + " " + str(self.heimatort)
        return repr_string

    def __str__(self):
        repr_string = self.name + " " + str(self.heimatort)
        return repr_string

class Terminkalender():
    '''
    Diese Klasse soll den Terminkalender eines Technikers darstellen
    '''
    def __init__(self):
        self.kalender = {}
        self.initialisiere_kalender()

    def initialisiere_kalender(self):
        for a in xrange(einstellungen.planungshorizont+1):
            self.kalender[a] = {}

    def gib_termine_fuer_tag(self, tag):
        return self.kalender.get(tag)







