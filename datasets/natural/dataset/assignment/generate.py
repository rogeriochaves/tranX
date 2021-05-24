import os
import string
import nltk
import re
from numpy.random import rand, choice
from nltk import FreqDist
from nltk.corpus import brown, stopwords
nltk.download('brown')
nltk.download('stopwords')

templates = [
  "set #NAME to #VALUE",
  "let #NAME be #VALUE",
  "#NAME = #VALUE",
  "#NAME is #VALUE",
  "set #NAME equals #VALUE",
  "let #NAME equals #VALUE"
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

inputs = []
outputs = []
for i in range(1000):
  name = "_".join(choice(names, int(rand() * 3 + 1)))
  value_type = choice(value_types)
  if value_type == 'string':
    text = " ".join(choice(names, int(rand() * 3 + 1)))
    quote = "'" if rand() > 0.5 else '"'
    value = real_value = quote + text + quote
  elif value_type == 'number':
    value = real_value = choice(numbers)
  elif value_type == 'written_number':
    value = choice(numbers)
    real_value = numbers.index(value)
  elif value_type == 'variable':
    value = real_value = "_".join(choice(names, int(rand() * 3 + 1)))

  input = choice(templates).replace("#NAME", name).replace("#VALUE", str(value))
  output = name + " = " + str(real_value)

  inputs.append(input)
  outputs.append(output)


path = os.path.dirname(__file__)
with open(path + '/inputs.txt', 'w') as f:
  f.write("\n".join(inputs))

with open(path + '/outputs.txt', 'w') as f:
  f.write("\n".join(outputs))

print("Done!")