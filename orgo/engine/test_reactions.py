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

    def test2
