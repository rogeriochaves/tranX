from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated
from numpy.random import choice

templates = {
  "+": ["sum #A and #B",
        "add #A and #B",
        "add #A plus #B",
        "#A plus #B",
        "#A + #B",
        "concatenate #A with #B",
        "join #A and #B"],
  "-": ["#A minus #B",
        "#A - #B"],
  "*": ["#A times #B",
        "#A multiplied by #B",
        "#A * #B"],
  "/": ["#A divided by #B",
        "#A / #B"],
  "**": ["#A to the power of #B",
         "#A ^ #B",
         "#A ** #B",
         "#A squared"],
}

update_templates = {
  "+": ["#NAME += #VALUE",
        "add #VALUE to #NAME"],
  "-": ["#NAME -= #VALUE",
        "subtract #VALUE from #NAME"],
  "*": ["#NAME *= #VALUE",
        "multiply #NAME by #VALUE"],
  "/": ["#NAME /= #VALUE",
        "divide #NAME by #VALUE"],
  "**": ["raise #NAME to the power of #VALUE",
         "square #NAME"]
}

def generate_sample(variable_to_use=None):
  operation = choice(list(templates.keys()))
  possible_types = ['number', 'written_number', 'variable']
  template = choice(templates[operation])
  if 'join' in template or 'concatenate' in template:
    possible_types = ['string', 'variable']
  if 'add' in template or '+' in template:
    possible_types += ['string']

  (a, a_value) = generate_value(possible_types)
  (b, b_value) = generate_value(possible_types)

  if variable_to_use is not None:
    a = a_value = variable_to_use

  input = template.replace("#A", a).replace("#B", b)
  if "squared" in input:
    output = "%s ** 2" % a_value
  else:
    output = "%s %s %s" % (a_value, operation, b_value)

  return (input, output)

def generate_sample_update():
  operation = choice(list(update_templates.keys()))
  possible_types = ['number', 'written_number', 'variable']
  template = choice(update_templates[operation])
  if 'add' in template or '+' in template:
    possible_types += ['string']

  name = generate_name()
  (value, real_value) = generate_value(possible_types)

  input = template.replace("#NAME", name).replace("#VALUE", value)
  if "square" in input:
    output = "%s **= 2" % name
  else:
    output = "%s %s= %s" % (name, operation, real_value)

  return (input, output)

inputs = []
outputs = []
for i in range(500):
  (input, output) = generate_sample()
  inputs.append(input)
  outputs.append(output)

for i in range(500):
  (input, output) = generate_sample_update()
  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")