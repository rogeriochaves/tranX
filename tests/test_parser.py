import unittest

from langcreator.parser import parse


class GenerateTestCase(unittest.TestCase):
    def test_parses_examples(self):
        example = """
# assignment

`#name = #number`

    set #name to #number
    let #name to be #number

# function

`def #name(#params):`

    define function #name #params
    fun #name #params

# params

- name
"""
        result = parse(example)
        self.assertEqual(
            result, {
                "assignment": {
                    "inputs":
                    ["set #name to #number", "let #name to be #number"],
                    "output": "#name = #number"
                },
                "function": {
                    "inputs":
                    ["define function #name #params", "fun #name #params"],
                    "output":
                    "def #name(#params):"
                },
                "params": [
                    "name"
                ]
            })

    def test_parses_composition_tags(self):
        example = """
# value

- string
- number
"""
        result = parse(example)
        self.assertEqual(result, {"value": ["string", "number"]})

    def test_throws_if_example_does_not_have_all_tags(self):
        example = """
# assignment

`#name = #number`

    set #name
    let #name to be #number
"""
        with self.assertRaisesRegex(
                Exception,
                "missing #number in example 1 of assignment `#name = #number`"
        ):
            parse(example)

    def test_throws_for_invalid_tag_name(self):
        example = """
# assignment:

`#name = #number`

    set #name to #number
"""
        with self.assertRaisesRegex(
                Exception,
                "# assignment: is invalid, only letters and _ are allowed"):
            parse(example)

    def test_throws_for_missing_input(self):
        example = """
# foo

`1 + 1`

# assignment

`#name = #number`

    set #name to #number
"""
        with self.assertRaisesRegex(Exception,
                                    "input examples missing on # foo"):
            parse(example)

    def test_throws_for_missing_output(self):
        example = """
# foo

    1 + 1

# assignment

`#name = #number`

    set #name to #number
"""
        with self.assertRaisesRegex(Exception, "output missing on # foo"):
            parse(example)

    def test_throws_for_missing_output(self):
        example = """
# assignment

`#name = #banana`

    set #name to #banana
"""
        with self.assertRaisesRegex(
                Exception,
                "#banana is used in # assignment but it's not defined anywhere. Defined tags are #number, #string, #name, #assignment"
        ):
            parse(example)


    def test_throws_for_missing_output(self):
        example = """
# foo

- name
- banana
"""
        with self.assertRaisesRegex(
                Exception,
                "- banana is used in # foo but it's not defined anywhere. Defined tags are #number, #string, #name, #foo"
        ):
            parse(example)
