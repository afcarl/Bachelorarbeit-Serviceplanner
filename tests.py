__author__ = 'Sebastian Gehrmann'

import karten, model, problem
import unittest


class TestModel(unittest.TestCase):
    def setUp(self):
        self.servicetechniker = model.Techniker("Hans", (0, 0))
        self.termin_fuer_7 = self.servicetechniker.termine.gib_termine_fuer_tag(7)

    def test_initialisiert_kalender(self):
        self.assertEqual(self.termin_fuer_7, {})


class TestBasisKarte(unittest.TestCase):
    def setUp(self):
        self.karte = karten.BasisKarte()
        self.zufallspunkt = self.karte.gib_Zufallspunkt()

    def test_obere_grenzen(self):
        self.assertEqual(self.karte.max_x, 10)
        self.assertEqual(self.karte.max_y, 10)

    def test_zufallspunkt(self):
        #print "Der Zufaellige Punkt liegt hier: (%d, %d)" % (self.zufallspunkt[0], self.zufallspunkt[1])
        self.assertTrue(self.zufallspunkt[0] >= 0 and self.zufallspunkt[1] >= 0)
        self.assertTrue(self.zufallspunkt[0] <= 10 and self.zufallspunkt[1] <= 10)

class TestProblem(unittest.TestCase):
    def setUp(self):
        self.terminarten = {1: (1.1, 1)}
        self.techniker = [model.Techniker("Hans", (11, 0))]
        self.kunden = [model.Kunde("Hugo", (0,0))]
        self.karte = karten.BasisKarte()

    def test_invalider_techniker(self):
        with self.assertRaises(ValueError):
            problem.Problem({}, self.karte, self.techniker, self.kunden, 0)

    def test_invalide_terminart(self):
        with self.assertRaises(ValueError):
            problem.Problem(self.terminarten, self.karte, 0, 0, 0)


if __name__ == '__main__':
    unittest.main()


'''
In case the unit tests fail, here is a safety pig
                         _
 _._ _..._ .-',     _.._(`))
'-. `     '  /-._.-'    ',/
   )         \            '.
  / _    _    |             \
 |  a    a    /              |
 \   .-.                     ;
  '-('' ).-'       ,'       ;
     '-;           |      .'
        \           \    /
        | 7  .__  _.-\   \
        | |  |  ``/  /`  /
       /,_|  |   /,_/   /
          /,_/      '`-'
'''
