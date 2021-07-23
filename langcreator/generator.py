import os
import string
import nltk  # type: ignore
import re
from nltk import FreqDist
from nltk.corpus import brown, stopwords  # type: ignore
from typing import List
from langcreator.common import Generators, InputOutput, InputOutputGenerator, get_tags, choice, builtin_generators

nltk.download('brown', quiet=True)
nltk.download('stopwords', quiet=True)

value_types = ['string', 'number', 'written_number', 'variable', 'list']
numbers_written = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten'
]

frequency_list = FreqDist(w.lower() for w in brown.words() if len(w) > 2)
reserved_words = set([
    "get", "if", "while", "for", "break", "continue", "end", "any", "and",
    "or", "remove", "delete", "set", "between", "same", "greater", "smaller",
    "equals", "use", "set", "let", "equals", "be", "to", "is", "do", "done",
    "exit", "break", "continue", "times", "end", "let", "remove", "update",
    "jump", "go", "each", "switch", "case", "replace", "match", "small",
    "greater", "than"
] + numbers_written + value_types)
stopwords_en = stopwords.words('english')

letters = list(string.ascii_lowercase)
names = [
    w for w, _ in frequency_list.most_common()[100:300] if w not in
    reserved_words and w not in stopwords_en and re.match("^[a-z]+$", w)
] + letters

numbers = list(range(101))


def generate_samples(generators: Generators, n: int) -> List[InputOutput]:
    return [
        _generate_sample(generators, choice(list(generators.keys())))
        for _ in range(n)
    ]


def _generate_sample(generators: Generators, key: str) -> InputOutput:
    key = key.replace("'", "")
    if key in builtin_generators:
        return _generate_builtin(key)

    generator = generators[key]
    if type(generator) == dict:
        return _generate_input_output_sample(generators, generator)
    elif type(generator) == list:
        return _generate_sample(generators, choice(generator))
    else:
        raise Exception(f"Invalid generator {key}")


def _generate_builtin(key: str):
    if key == "int":
        input = output = str(choice(numbers))
        return (input, output)
    elif key == "name":
        input = output = _generate_name()
        return (input, output)
    elif key == "float":
        input = output = str(choice(numbers) / choice([10, 100]))
        return (input, output)
    elif key == "string":
        input = output = _generate_string()
        return (input, output)
    else:
        raise Exception(f"Builtin generator for {key} not implemented yet")


def _generate_input_output_sample(
        generators: Generators,
        generator: InputOutputGenerator) -> InputOutput:
    output_template = choice(list(generator.keys()))
    input_template = choice(generator[output_template])

    tags = get_tags(input_template)
    for tag in tags:
        key_ = tag.replace("#", "")
        (input, output) = _generate_sample(generators, key_)
        output = _adjust_indentation(output)
        output = _adjust_ending(output)
        input_template = input_template.replace(tag, input, 1)
        output_template = output_template.replace(tag, output, 1)

    return (input_template, output_template)


def _generate_name():
    return "_".join(choice(names, choice([1, 2, 3])))


def _generate_string():
    text = " ".join(choice(names, choice([1, 2, 3])))
    quote = choice(["'", '"'])
    return quote + text + quote

def _adjust_indentation(output: str):
    return output.replace("\\n", "\\n\\t")

def _adjust_ending(output: str):
    if len(output) > 0 and output[-1] == ':':
       return output + ' pass'
    return output

def save_generated(generated: List[InputOutput], path: str = None):
    if path is None:
        path = os.path.dirname(__file__)

    inputs = [i for i, _ in generated]
    outputs = [o for _, o in generated]

    with open(os.path.join(path, 'inputs.txt'), 'w') as f:
        f.write("\n".join(inputs))

    with open(os.path.join(path, 'outputs.txt'), 'w') as f:
        f.write("\n".join(outputs))
