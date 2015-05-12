from unittest import TestCase
from helperFunctions import *

class TestHelperFunctions(TestCase):
    def test_moleculeSame(self):
        oxygen = Atom("O")
        WATER = Molecule(oxygen)
        WATER.addAtom(Atom("H"), oxygen)
        WATER.addAtom(Atom("H"), oxygen)
        
        oxygen2 = Atom("O")
        WATER2 = Molecule(oxygen2)
        WATER2.addAtom(Atom("H"), oxygen2)
        WATER2.addAtom(Atom("H"), oxygen2)

        self.assertTrue(moleculeSame(WATER, WATER2))

class TestReactions(TestCase):
    def assertReaction(before, reaction, after):
        ## before :: [Molecule]
        ## reaction :: Molecule -> Molecule
        ## after :: [Molecule]
