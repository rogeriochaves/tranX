import unittest

from langcreator.generator import generate_samples
import langcreator.common

langcreator.common.set_seed(42)


class GeneratorTestCase(unittest.TestCase):
    def test_generates_simple_examples(self):
        generators = {
            "assignment": {
                "output": "#name = #number",
                "inputs": ["set #name to #number", "let #name to be #number"]
            },
            "number": ["int", "float"]
        }
        result = generate_samples(generators, n=3)

        self.assertEqual(result,
                         [('let social_side to be 0.08', 'social_side = 0.08'),
                          ('set v_help to 0.72', 'v_help = 0.72'),
                          ('84', '84')])
