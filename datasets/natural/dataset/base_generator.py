import os
import string
import nltk
import re
from nltk import FreqDist
from nltk.corpus import brown, stopwords
from numpy.random import rand, choice
nltk.download('brown')
nltk.download('stopwords')

templates = [
  "sum #A and #B",
  "add #A plus #A",
  "#A plus #B",
  "#A + #B",
]

update_templates = [
  "#A += #B",
  "add #A to #B"
]

frequency_list = FreqDist(w.lower() for w in brown.words() if len(w) > 2)
reserved_words = set(["get", "if", "while", "for", "break", "continue", "end", "any", "and",
                      "or", "remove", "delete", "set", "between", "same", "greater", "smaller",
                      "equals", "use", "set", "let", "equals", "be", "to", "is"])
stopwords_en = stopwords.words('english')

letters = list(string.ascii_lowercase)
names = [ w for w, _ in frequency_list.most_common()[100:300]
            if w not in reserved_words
            and w not in stopwords_en
            and re.match("^[a-z]+$", w) ] + letters

numbers = list(range(101))
numbers_written = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

value_types = ['string', 'number', 'written_number', 'variable']

def generate_name():
  return "_".join(choice(names, int(rand() * 3 + 1)))

def generate_string():
  text = " ".join(choice(names, int(rand() * 3 + 1)))
  quote = "'" if rand() > 0.5 else '"'
  return quote + text + quote

def generate_value(possible_types=value_types):
  value_type = choice(possible_types)
  if value_type == 'string':
    value = real_value = generate_string()
  elif value_type == 'number':
    value = real_value = choice(numbers)
  elif value_type == 'written_number':
    value = choice(numbers_written)
    real_value = numbers_written.index(value)
  elif value_type == 'variable':
    value = real_value = generate_name()

  return (str(value), str(real_value))

def save_generated(file, inputs, outputs):
  path = os.path.dirname(file)
  with open(path + '/inputs.txt', 'w') as f:
    f.write("\n".join(inputs))

  with open(path + '/outputs.txt', 'w') as f:
    f.write("\n".join(outputs))
