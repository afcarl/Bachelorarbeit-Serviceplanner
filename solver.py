"""
In diesem Skript werden die verschiedenen Loesungsalgorithmen gesammelt
"""
import karten

__author__ = 'Sebastian Gehrmann'

import copy
import einstellungen
import heapq
import math
import random

import problem


def berechne_entfernung(von, zu):
    """
    Funktion zur Berechnung der Entfernung zwischen zwei Punkten
    """
    a_q = abs(von[0] - zu[0])
    b_q = abs(von[1] - zu[1])
    return math.ceil(math.sqrt(a_q + b_q)) / float(2)


def termine_in_techniker(tech):
    """
    zaehlt die Anzahl Termine fuer einen Techniker
    """
    anzahl = 0
    for k, v in tech.termine.kalender.iteritems():
        anzahl += len(v)
    return anzahl


def sortiere_techniker(tech_array):
    """
    sortiert Techniker nach der Anzahl ihrer Termine auf einem Heap
    """
    sortierte_techniker = []
    for t in tech_array:
        heapq.heappush(sortierte_techniker, (termine_in_techniker(t), t))
    return sortierte_techniker


def sortiere_techniker_entfernung(tech_array, ort):
    """
    sortiert Techniker nach der Entfernung zu einem Punkt auf ein Heap
    """
    sortierte_techniker = []
    for t in tech_array:
        heapq.heappush(sortierte_techniker, (berechne_entfernung(t.heimatort, ort), t))
    return sortierte_techniker


def greedy_solver(testproblem):
    """
    Erste Version des Greedy-Algorithmus. Liefert einen Terminplan fuer ein SSP
    """

    termine_zu_vergeben = copy.copy(testproblem.termine)
    termine_backlog = []
    # um zu messen wann fertig ist
    anzahl_termine_zu_vergeben = len(termine_zu_vergeben)
    # iteriere alle Termine
    while anzahl_termine_zu_vergeben > 0:
        current_termin = random.choice(termine_zu_vergeben)
        found_something = False
        # Techniker reduzieren auf die in Fahrweite und dann auf Heap sortieren nach Anzahl Termine
        techniker_fuer_termin = [t for t in testproblem.techniker
                                 if 2 * berechne_entfernung(t.heimatort,
                                                            current_termin.kunde.ort)
                                 + current_termin.dauer
                                 <= einstellungen.max_arbeitsdauer]
        techniker_heap = sortiere_techniker(techniker_fuer_termin)

        #solange noch Techniker vorhanden sind und noch nichts gefunden wurde
        while len(techniker_heap) > 0 and not found_something:
            current_techniker = heapq.heappop(techniker_heap)[1]
            wegzeit_nach_hause = berechne_entfernung(current_techniker.heimatort,
                                                     current_termin.kunde.ort)
            #probiere jeden Tag
            for tag_nummer in xrange(einstellungen.min_planungshorizont, einstellungen.planungshorizont + 1, 1):
                current_terminplan = current_techniker.gib_termin_fuer_tag(tag_nummer)
                if not current_terminplan:
                    anfangszeit = einstellungen.zeiten_ab + wegzeit_nach_hause
                    current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                    found_something = True
                    break
                else:
                    # der spaeteste Termin an dem Tag
                    letzter_terminzeitpunkt = max(current_terminplan.keys())
                    letzter_termin = current_terminplan[letzter_terminzeitpunkt]
                    # Wann ist er fertig?
                    letzter_termin_fertig_zeit = letzter_terminzeitpunkt + letzter_termin.dauer
                    # Wie lange wuerde man zum naechsten fahren?
                    wegzeit_zu_kunde = berechne_entfernung(letzter_termin.kunde.ort,
                                                           current_termin.kunde.ort)
                    # Wie lange wuerde es also insgesamt dauern?
                    neuer_termin_gesamt_zeit = wegzeit_zu_kunde + current_termin.dauer + wegzeit_nach_hause
                    # Wie lange darf es max. dauern?
                    spaeteste_zeit = einstellungen.max_arbeitsdauer + einstellungen.zeiten_ab
                    # Passt der Termin noch?
                    if letzter_termin_fertig_zeit + neuer_termin_gesamt_zeit <= spaeteste_zeit:
                        anfangszeit = letzter_termin_fertig_zeit + wegzeit_zu_kunde
                        current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                        found_something = True
                        break

        if not found_something:
            termine_backlog.append(current_termin)
        termine_zu_vergeben.remove(current_termin)
        anzahl_termine_zu_vergeben -= 1
    return testproblem, termine_backlog


def greedy_solver_erweitert(testproblem):
    spaeteste_zeit = einstellungen.max_arbeitsdauer + einstellungen.zeiten_ab
    termine_backlog = []

    termine_zuweis_dict = {t.name: [] for t in testproblem.techniker}
    for term in testproblem.termine:
        curr_min = float('inf')
        curr_min_techniker = None
        for tech in testproblem.techniker:
            curr_dist = berechne_entfernung(term.kunde.ort, tech.ort)
            if curr_dist < curr_min:
                curr_min = curr_dist
                curr_min_techniker = tech
        termine_zuweis_dict[curr_min_techniker.name].append(term)

    # nacheinander die Techniker durchgehen
    for key, value in termine_zuweis_dict.iteritems():
        termine_zu_vergeben = copy.copy(value)

        current_techniker = [t for t in testproblem.techniker if t.name == key][0]
        current_techniker.reset_tech()
        anzahl_termine_zu_vergeben = len(termine_zu_vergeben)

        while anzahl_termine_zu_vergeben > 0:
            found_something = False

            current_termin = random.choice(termine_zu_vergeben)
            wegzeit_nach_hause = berechne_entfernung(current_techniker.heimatort,
                                                     current_termin.kunde.ort)

            for tag_nummer in xrange(einstellungen.min_planungshorizont, einstellungen.planungshorizont + 1, 1):
                current_terminplan = current_techniker.gib_termin_fuer_tag(tag_nummer)
                if not current_terminplan:
                    anfangszeit = einstellungen.zeiten_ab + wegzeit_nach_hause
                    current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                    found_something = True
                    break
                else:
                    letzter_terminzeitpunkt = max(current_terminplan.keys())
                    letzter_termin = current_terminplan[letzter_terminzeitpunkt]
                    letzter_termin_fertig_zeit = letzter_terminzeitpunkt + letzter_termin.dauer

                    gleicher_kunde_termine = [term for term in termine_zu_vergeben if
                                              term.kunde.ort == letzter_termin.kunde.ort]
                    if gleicher_kunde_termine:
                        gleicher_kunde_termine.sort(key=lambda x: x.dauer, reverse=True)
                        for term in gleicher_kunde_termine:
                            nach_hause_von_term = berechne_entfernung(current_techniker.heimatort, term.kunde.ort)
                            if letzter_termin_fertig_zeit + term.dauer + nach_hause_von_term <= spaeteste_zeit:
                                current_termin = term
                                found_something = True
                                anfangszeit = letzter_termin_fertig_zeit
                                current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                                break
                        if found_something:
                            break
                    else:

                        wegzeit_zu_kunde = berechne_entfernung(letzter_termin.kunde.ort,
                                                               current_termin.kunde.ort)
                        # Wie lange wuerde es also insgesamt dauern?
                        neuer_termin_gesamt_zeit = wegzeit_zu_kunde + current_termin.dauer + wegzeit_nach_hause
                        # Wie lange darf es max. dauern?
                        # Passt der Termin noch?
                        if letzter_termin_fertig_zeit + neuer_termin_gesamt_zeit <= spaeteste_zeit:
                            anfangszeit = letzter_termin_fertig_zeit + wegzeit_zu_kunde
                            current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                            found_something = True
                            break

            if not found_something:
                termine_backlog.append(current_termin)
            termine_zu_vergeben.remove(current_termin)
            anzahl_termine_zu_vergeben -= 1

    return testproblem, termine_backlog


def greedy_solver_final(testproblem):
    termine_zu_vergeben = copy.copy(testproblem.termine)
    spaeteste_zeit = einstellungen.max_arbeitsdauer + einstellungen.zeiten_ab

    termine_backlog = []
    anzahl_termine_zu_vergeben = len(termine_zu_vergeben)
    while anzahl_termine_zu_vergeben > 0:
        current_termin = random.choice(termine_zu_vergeben)
        found_something = False
        # Techniker reduzieren auf welche in Fahrweite und dann auf Heap sortieren nach Anzahl Termine
        techniker_fuer_termin = [t for t in testproblem.techniker
                                 if 2 * berechne_entfernung(t.heimatort,
                                                            current_termin.kunde.ort)
                                 + current_termin.dauer
                                 <= einstellungen.max_arbeitsdauer]
        # sortiere nach der entfernung vom heimatort
        techniker_heap = sortiere_techniker_entfernung(techniker_fuer_termin, current_termin.kunde.ort)

        while len(techniker_heap) > 0 and not found_something:
            current_techniker = heapq.heappop(techniker_heap)[1]
            wegzeit_nach_hause = berechne_entfernung(current_techniker.heimatort,
                                                     current_termin.kunde.ort)
            for tag_nummer in xrange(einstellungen.min_planungshorizont, einstellungen.planungshorizont + 1, 1):
                current_terminplan = current_techniker.gib_termin_fuer_tag(tag_nummer)
                if not current_terminplan:
                    anfangszeit = einstellungen.zeiten_ab + wegzeit_nach_hause
                    current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                    found_something = True
                    break
                else:
                    letzter_terminzeitpunkt = max(current_terminplan.keys())
                    letzter_termin = current_terminplan[letzter_terminzeitpunkt]
                    letzter_termin_fertig_zeit = letzter_terminzeitpunkt + letzter_termin.dauer

                    gleicher_kunde_termine = [term for term in termine_zu_vergeben if
                                              term.kunde.ort == letzter_termin.kunde.ort]
                    if gleicher_kunde_termine:
                        gleicher_kunde_termine.sort(key=lambda x: x.dauer, reverse=True)
                        for term in gleicher_kunde_termine:
                            nach_hause_von_term = berechne_entfernung(current_techniker.heimatort, term.kunde.ort)
                            if letzter_termin_fertig_zeit + term.dauer + nach_hause_von_term <= spaeteste_zeit:
                                current_termin = term
                                found_something = True
                                anfangszeit = letzter_termin_fertig_zeit
                                current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                                break
                        if found_something:
                            break
                    else:

                        wegzeit_zu_kunde = berechne_entfernung(letzter_termin.kunde.ort,
                                                               current_termin.kunde.ort)
                        neuer_termin_gesamt_zeit = wegzeit_zu_kunde + current_termin.dauer + wegzeit_nach_hause
                        if letzter_termin_fertig_zeit + neuer_termin_gesamt_zeit <= spaeteste_zeit:
                            anfangszeit = letzter_termin_fertig_zeit + wegzeit_zu_kunde
                            current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                            found_something = True
                            break

        if not found_something:
            termine_backlog.append(current_termin)
        termine_zu_vergeben.remove(current_termin)
        anzahl_termine_zu_vergeben -= 1
    return testproblem, termine_backlog


def greedy_heuristik(testproblem):
    termine_zu_vergeben = copy.copy(testproblem.termine)
    spaeteste_zeit = einstellungen.soll_arbeitsdauer + einstellungen.zeiten_ab

    termine_backlog = []
    anzahl_termine_zu_vergeben = len(termine_zu_vergeben)
    while anzahl_termine_zu_vergeben > 0:
        current_termin = random.choice(termine_zu_vergeben)
        found_something = False
        # Techniker reduzieren auf welche in Fahrweite und dann auf Heap sortieren nach Anzahl Termine
        techniker_fuer_termin = [t for t in testproblem.techniker
                                 if 2 * berechne_entfernung(t.heimatort,
                                                            current_termin.kunde.ort)
                                 + current_termin.dauer
                                 <= einstellungen.max_arbeitsdauer]
        # sortiere nach der entfernung vom heimatort
        techniker_heap = sortiere_techniker_entfernung(techniker_fuer_termin, current_termin.kunde.ort)

        while len(techniker_heap) > 0 and not found_something:
            current_techniker = heapq.heappop(techniker_heap)[1]
            wegzeit_nach_hause = berechne_entfernung(current_techniker.heimatort,
                                                     current_termin.kunde.ort)
            for tag_nummer in xrange(einstellungen.min_planungshorizont, einstellungen.planungshorizont + 1, 1):
                current_terminplan = current_techniker.gib_termin_fuer_tag(tag_nummer)
                if not current_terminplan:
                    anfangszeit = einstellungen.zeiten_ab + wegzeit_nach_hause
                    current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                    found_something = True
                    break
                else:
                    letzter_terminzeitpunkt = max(current_terminplan.keys())
                    letzter_termin = current_terminplan[letzter_terminzeitpunkt]
                    safety = testproblem.terminarten[letzter_termin.dauer][1]
                    letzter_termin_fertig_zeit = letzter_terminzeitpunkt + letzter_termin.dauer + safety

                    gleicher_kunde_termine = [term for term in termine_zu_vergeben if
                                              term.kunde.ort == letzter_termin.kunde.ort]
                    if gleicher_kunde_termine:
                        gleicher_kunde_termine.sort(key=lambda x: x.dauer, reverse=True)
                        for term in gleicher_kunde_termine:
                            nach_hause_von_term = berechne_entfernung(current_techniker.heimatort, term.kunde.ort)
                            if letzter_termin_fertig_zeit + term.dauer + nach_hause_von_term <= spaeteste_zeit:
                                current_termin = term
                                found_something = True
                                anfangszeit = letzter_termin_fertig_zeit
                                current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                                break
                        if found_something:
                            break
                    else:

                        wegzeit_zu_kunde = berechne_entfernung(letzter_termin.kunde.ort,
                                                               current_termin.kunde.ort)
                        neuer_termin_gesamt_zeit = wegzeit_zu_kunde + current_termin.dauer + wegzeit_nach_hause
                        if letzter_termin_fertig_zeit + neuer_termin_gesamt_zeit <= spaeteste_zeit:
                            anfangszeit = letzter_termin_fertig_zeit + wegzeit_zu_kunde
                            current_techniker.termine.kalender[tag_nummer][anfangszeit] = current_termin
                            found_something = True
                            break

        if not found_something:
            termine_backlog.append(current_termin)
        termine_zu_vergeben.remove(current_termin)
        anzahl_termine_zu_vergeben -= 1
    return testproblem, termine_backlog


if __name__ == '__main__':
    karte = karten.BasisKarte()
    testproblem = problem.Problem(1, karte, 5, 20, 50)
    auswertungsproblem = greedy_heuristik(testproblem)[0]
