from datasets.python3.datagen.base_generator import save_generated
import unittest

from langcreator.generator import generate_samples, save_generated
import langcreator.common


class GeneratorTestCase(unittest.TestCase):
    def setUp(self):
        langcreator.common.set_seed(42)

    def test_generates_simple_examples(self):
        generators = {
            "assignment": {
                "#name = #number": ["set #name to #number", "let #name to be #number"]
            },
            "number": ["int", "float"]
        }
        result = generate_samples(generators, n=3)

        self.assertEqual(
            result,
            [('let present_social to be 0.08', 'present_social = 0.08'),
             ('set v_help to 0.72', 'v_help = 0.72'), ('84', '84')])

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
                "[ #int, #int', #int'' ]": ["second item #int', first and foremost #int and last but not least #int''"]
            },
        }
        result = generate_samples(generators, n=1)

        self.assertEqual(result, [
            ("second item 9, first and foremost 78 and last but not least 66",
             '[ 78, 9, 66 ]'),
        ])

    def test_generate_all_builtins(self):
        builtins = ", ".join(
            ["#" + x for x in langcreator.common.builtin_generators])
        generators = {
            "example": {
                f"({builtins})": [f"list of {builtins}"]
            },
            "number": ["int", "float"]
        }
        result = generate_samples(generators, n=1)

        self.assertEqual(
            result, [('list of 78, 6.6, "feet states", without',
                      '(78, 6.6, "feet states", without)')])

    def test_generate_nested_identation(self):
        generators = {
            "if": {
                "if True:\\n\\t#nested_if": ["#nested_if if True"]
            },
            "nested_if": {
                "if False:\\n\\tprint('hello')\\nelse:\\nprint('bye')": ["never print hello"]
            },
        }
        result = generate_samples(generators, n=1)

        self.assertEqual(result,
                         [('never print hello if True',
                           "if True:\\n\\tif False:\\n\\t\\tprint('hello')\\n\\telse:\\n\\tprint('bye')")])

    def test_generate_complete_hanging_if(self):
        generators = {
            "nested_if": {
                "if False:\\n\\t#lonely_if\\nelse:\\nprint('whatever')": ["never #lonely_if"]
            },
            "lonely_if": {
                "if True:": ["always"]
            },
        }
        result = generate_samples(generators, n=1)

        self.assertEqual(result,
                         [('never always', "if False:\\n\\tif True: pass\\nelse:\\nprint('whatever')")])