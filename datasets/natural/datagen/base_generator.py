import os
import string
import nltk
import re
from nltk import FreqDist
from nltk.corpus import brown, stopwords
import numpy as np
from numpy.random import rand

nltk.download('brown', quiet=True)
nltk.download('stopwords', quiet=True)

templates = [
    "sum #A and #B",
    "add #A plus #A",
    "#A plus #B",
    "#A + #B",
]

update_templates = ["#A += #B", "add #A to #B"]

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

rng = np.random.default_rng()


def choice(list, size=None):
    return rng.choice(list, size)


def generate_name():
    return "_".join(choice(names, int(rand() * 3 + 1)))


def generate_string():
    text = " ".join(choice(names, int(rand() * 3 + 1)))
    quote = "'" if rand() > 0.5 else '"'
    return quote + text + quote


def generate_value(possible_types=value_types, depth=0):
    value_type = choice(possible_types)
    if value_type == 'string':
        value = real_value = generate_string()
    elif value_type == 'number':
        if choice(['int', 'int', 'float']) == 'int':
            value = real_value = choice(numbers)
        else:
            value = real_value = choice(numbers) / choice([10, 100])
    elif value_type == 'written_number':
        value = choice(numbers_written)
        real_value = numbers_written.index(value)
    elif value_type == 'variable':
        value = real_value = generate_name()
    elif value_type == 'list':
        (value, real_value) = generate_list(depth)

    return (str(value), str(real_value))


def generate_list(depth=0):
    if depth == 0:
        list_type = choice(value_types)
    else:
        list_type = choice(['string', 'number', 'variable'])
    list_length = int(rand() * 10)
    if depth == 0:
        list_style = choice(
            ["curly braces", "square brackets", "parens", "list of"])
    else:
        list_style = choice(["curly braces", "square brackets", "parens"])
    list = [
        generate_value([list_type], depth=(depth + 1))
        for _ in range(list_length)
    ]

    real_value = "[" + ", ".join([rv for _, rv in list]) + "]"
    if list_style == 'square brackets':
        value = "[" + ", ".join([v for v, _ in list]) + "]"
    elif list_style == 'curly braces':
        value = "{" + ", ".join([v for v, _ in list]) + "}"
    elif list_style == 'parens':
        value = "(" + ", ".join([v for v, _ in list]) + ")"
    elif list_style == 'list of':
        connector = choice(["of", "with", "containing"])
        if len(list) == 0:
            value = "empty list"
        elif len(list) == 1:
            value = "list %s %s" % (connector, list[0][0])
        else:
            value = "list %s %s and %s" % (connector, ", ".join(
                [v for v, _ in list[0:-1]]), list[-1][0])

    return (value, real_value)


def save_generated(file, inputs, outputs):
    path = os.path.dirname(file)
    with open(os.path.join(path, 'inputs.txt'), 'w') as f:
        f.write("\n".join(inputs))

    with open(os.path.join(path, 'outputs.txt'), 'w') as f:
        f.write("\n".join(outputs))
