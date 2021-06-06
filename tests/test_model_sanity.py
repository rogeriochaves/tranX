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

    def test_postfix_if_call(self):
        self.assertEqual(parse("print(x) if x > 0"), "if x > 0:\n  print(x)")