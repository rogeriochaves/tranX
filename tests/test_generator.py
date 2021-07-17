from datasets.natural.datagen.base_generator import save_generated
import unittest

from langcreator.generator import generate_samples, save_generated
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

    def test_save_generated(self):
        generated = [("foo input", "foo"), ("bar input", "bar")]

        save_generated(generated, path="/tmp/")

        with open("/tmp/inputs.txt") as f:
            content = f.read()
        self.assertEqual(content, "foo input\nbar input")

        with open("/tmp/outputs.txt") as f:
            content = f.read()
        self.assertEqual(content, "foo\nbar")

    def test_matches_prime_orders(self):
        generators = {
            "list": {
                "output":
                "[ #int, #int', #int'' ]",
                "inputs": [
                    "second item #int', first and foremost #int and last but not least #int''"
                ]
            },
        }
        result = generate_samples(generators, n=1)

        self.assertEqual(result, [
            ("second item 45, first and foremost 50 and last but not least 37",
             '[ 50, 45, 37 ]'),
        ])
