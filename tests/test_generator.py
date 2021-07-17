import unittest

from langcreator.generator import generate_samples
import langcreator.common

langcreator.common.set_seed(42)


class GeneratorTestCase(unittest.TestCase):
    def test_generates_output_inputs_examples(self):
        generators = {
            "assignment": {
                "output": "#name = #int",
                "inputs": ["set #name to #int", "let #name to be #int"]
            }
        }
        result = generate_samples(generators, n=2)
        self.assertEqual(result, [
            ("set mind_social_side to 86", "mind_social_side = 86"),
            (
                "set course_without_early to 98",
                "course_without_early = 98",
            ),
        ])
