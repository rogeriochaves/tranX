import string
import nltk  # type: ignore
import re
import numpy as np
from nltk import FreqDist
from nltk.corpus import brown, stopwords  # type: ignore
from typing import List, Optional
from langcreator.common import Generators, InputOutput, InputOutputGenerator, get_tags, T, choice

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
    "jump", "go", "each", "switch", "case", "replace", "match"
] + numbers_written + value_types)
stopwords_en = stopwords.words('english')

letters = list(string.ascii_lowercase)
names = [
    w for w, _ in frequency_list.most_common()[100:300] if w not in
    reserved_words and w not in stopwords_en and re.match("^[a-z]+$", w)
] + letters

numbers = list(range(101))


def generate_samples(generators: Generators, n: int) -> List[InputOutput]:
    return [_generate_sample(generators, None) for _ in range(n)]


def _generate_sample(generators: Generators,
                     key: Optional[str]) -> InputOutput:
    if key is None:
        key = choice(list(generators.keys()))

    if key == "int":
        input = output = str(choice(numbers))
        return (input, output)
    elif key == "name":
        input = output = _generate_name()
        return (input, output)

    generator = generators[key]
    if type(generator) == dict:
        return _generate_input_output_sample(generators, generator, key)

    return ("undefined", "undefined")


def _generate_input_output_sample(generators: Generators,
                                  generator: InputOutputGenerator,
                                  key: str) -> InputOutput:
    input_template = choice(generator["inputs"])
    output_template = generator["output"]

    tags = get_tags(input_template)
    for tag in tags:
        key_ = tag.replace("#", "")
        (input, output) = _generate_sample(generators, key_)
        input_template = input_template.replace(tag, input, 1)
        output_template = output_template.replace(tag, output, 1)

    return (input_template, output_template)


def _generate_name():
    return "_".join(choice(names, choice([1, 2, 3])))