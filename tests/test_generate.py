import unittest

from langcreator.generate import parse


class GenerateTestCase(unittest.TestCase):
    def test_parses_examples(self):
        example = """
# assignment

`#name = #value`

    set #name to #value
    let #name to be #value
"""
        result = parse(example)
        self.assertEqual(
            result, {
                "assignment": {
                    "inputs":
                    ["set #name to #value", "let #name to be #value"],
                    "output": "#name = #value"
                }
            })

    def test_throws_if_example_does_not_have_all_tags(self):
        example = """
# assignment

`#name = #value`

    set #name
    let #name to be #value
"""
        with self.assertRaisesRegex(
                Exception,
                "missing #value in example 1 of assignment `#name = #value`"):
            parse(example)