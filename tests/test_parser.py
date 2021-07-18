import unittest

from langcreator.parser import parse


class ParserTestCase(unittest.TestCase):
    def test_parses_examples(self):
        example = """
# assignment

`#name = #int`

    set #name to #int
    let #name to be #int

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
                    "inputs": ["set #name to #int", "let #name to be #int"],
                    "output": "#name = #int"
                },
                "function": {
                    "inputs":
                    ["define function #name #params", "fun #name #params"],
                    "output":
                    "def #name(#params):"
                },
                "params": ["name"]
            })

    def test_parses_composition_tags(self):
        example = """
# value

- string
- int
"""
        result = parse(example)
        self.assertEqual(result, {"value": ["string", "int"]})

    def test_parses_prime_tags(self):
        example = """
# list_processing

`[ x[#name] for x in [#int] ]`

    select #name from [#int]
    from [#int] map #name
    [#int].map(#name' => #name'[#name])
"""
        result = parse(example)
        self.assertEqual(
            result, {
                "list_processing": {
                    "inputs": [
                        "select #name from [#int]", "from [#int] map #name",
                        "[#int].map(#name' => #name'[#name])"
                    ],
                    "output":
                    "[ x[#name] for x in [#int] ]"
                },
            })

    def test_throws_if_example_does_not_have_all_tags(self):
        example = """
# assignment

`#name = #int`

    set #name
    let #name to be #int
"""
        with self.assertRaisesRegex(
                Exception,
                "missing #int in example 1 of assignment `#name = #int`"):
            parse(example)

    def test_throws_if_example_does_not_have_all_tags(self):
        example = """
# params

`(#string, #string, #string)`

    (#string, #string, #string)
    (#string #string)
"""
        with self.assertRaisesRegex(
                Exception,
                "missing 1 #string in example 2 of params `\(#string, #string, #string\)`. Expected to find 3 #string, found 2."
        ):
            parse(example)

    def test_throws_for_invalid_tag_name(self):
        example = """
# assignment:

`#name = #int`

    set #name to #int
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

`#name = #int`

    set #name to #int
"""
        with self.assertRaisesRegex(Exception,
                                    "input examples missing on # foo"):
            parse(example)

    def test_throws_for_missing_output(self):
        example = """
# foo

    1 + 1

# assignment

`#name = #int`

    set #name to #int
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
                "#banana is used in # assignment but it's not defined anywhere. Defined tags are #int, #float, #string, #name, #assignment"
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
                "- banana is used in # foo but it's not defined anywhere. Defined tags are #int, #float, #string, #name, #foo"
        ):
            parse(example)

    def test_parses_full_natural_definition_raising_no_exceptions(self):
        with open("langcreator/natural.md") as f:
            content = f.read()

        parse(content)

    def test_throws_when_defined_twice(self):
        example = """
# foo

- name
- string

# foo

- string
- int
"""
        with self.assertRaisesRegex(Exception, "# foo is being defined twice"):
            parse(example)