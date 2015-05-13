## Unit tests!

import unittest

from toMolecule import moleculify
from toSmiles import smilesify
from toCanonical import to_canonical
from reaction_functions import *

class TestReactions(unittest.TestCase):

    def assertReaction(self, reaction_function, input_smiles, output_smiles):
        self.assertEqual(
            to_canonical(smilesify(moleculify(output_smiles))),
            to_canonical(smilesify(reaction_function(moleculify(input_smiles))))
        )

    def test1(self):
        self.assertReaction(hydrobrominate_it, "CC=C", "CC(Br)C")
        self.assertReaction(hydrobrominate_it, "CC(C)=C", "CC(C)(Br)C")
        self.assertReaction(hydrobrominate_it, "CCC", "CCC")

    def test2(self):
        self.assertReaction(hydrogenate_it, "CC=C", "CCC")
        self.assertReaction(hydrogenate_it, "CC=C(C)C", "CCC(C)C")
        self.assertReaction(hydrogenate_it, "CC#C", "CCC")
        self.assertReaction(hydrogenate_it, "CC#CCC=C", "CCCCCC")
        self.assertReaction(hydrogenate_it, "CC#CC#CCC=CCC=C", "CCCCCCCCCCC")
        self.assertReaction(hydrogenate_it, "CCC", "CCC")
        self.assertReaction(hydrogenate_it, "CCBr", "CCBr")

    def test3(self):
        self.assertReaction(hydroiodinate_it, "CC=C(CC)C", "CCC(I)(CC)C")
        self.assertReaction(hydroiodinate_it, "C=C", "ICC")
        self.assertReaction(hydroiodinate_it, "CCC", "CCC")

    def test4(self):
        self.assertReaction(hydrochlorinate_it, "C1CC=CCC1", "C1CCC(Cl)CC1")
        self.assertReaction(hydrochlorinate_it, "C1CC(C)=CCC1", "C1CCC(Cl)(C)CC1")
        self.assertReaction(hydrochlorinate_it, "CCC", "CCC")
