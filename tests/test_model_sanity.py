import unittest
import json
from components.standalone_parser import StandaloneParser


config = json.load(open("config/server/config_py3.json"))['natural']

parser = StandaloneParser(parser_name=config['parser'],
                          model_path=config['model_path'],
                          example_processor_name=config['example_processor'],
                          beam_size=config['beam_size'],
                          reranker_path=config['reranker_path'],
                          cuda=False)

def parse(input):
    hypotheses = parser.parse(input, debug=False)
    return hypotheses[0].code


class ModelSanityTestCase(unittest.TestCase):
    def test_simple_assignment(self):
        self.assertEqual(parse("foo = 1"), "foo = 1")

    def test_string_assignment(self):
        self.assertEqual(parse("foo = 'bar'"), "foo = 'bar'")

    def test_function_assignment(self):
        self.assertEqual(parse("x = rand()"), "x = rand()")

    def test_if_condition(self):
        self.assertEqual(parse("if rand() > 5"), "if rand() > 5:\n    pass")

    def test_postfix_if_call(self):
        self.assertEqual(parse("print(x) if x > 0"), "if x > 0:\n    print(x)")

    def test_simple_comparisson(self):
        self.assertEqual(parse("x > 1"), "x > 1")

    def test_ternary(self):
        self.assertEqual(parse('x = "heads" if rand() > 5 else "tails"'), "x = 'heads' if rand() > 5 else 'tails'")

    def test_postfix_loop(self):
        self.assertEqual(parse("throw_coin() 20 times"), "for _ in range(20):\n    throw_coin()")

    def test_math_operation(self):
        self.assertEqual(parse("h = 1 / (i + j)"), "h = 1 / (i + j)")

    def test_idomatic_assignment(self):
        self.assertEqual(parse("set total to 1"), "total = 1")

    def test_ranged_loop(self):
        self.assertEqual(parse("total times n for n in 2..i"), "for n in range(2, i):\n    total * n")

    def test_decimal_numbers(self):
        self.assertEqual(parse("0.1 + 0.2"), "0.1 + 0.2")
