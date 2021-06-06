from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated
from datasets.natural.datagen.group_generators import generate_expression_sample
from numpy.random import choice

templates = [
  "set #NAME to #VALUE",
  "let #NAME be #VALUE",
  "#NAME = #VALUE",
  "#NAME is #VALUE",
  "set #NAME equals #VALUE",
  "let #NAME equals #VALUE",
  "put #VALUE into #NAME",
  "define #NAME as #VALUE",
  "initialize #NAME as #VALUE"
]

inputs = []
outputs = []
for i in range(1000):
  name = generate_name()
  (value, real_value) = generate_value()

  input = choice(templates).replace("#NAME", name).replace("#VALUE", value)
  output = "%s = %s" % (name, real_value)

  inputs.append(input)
  outputs.append(output)

def generate_sample(variable_to_use=None):
  name = generate_name()
  if variable_to_use:
    name = variable_to_use
  (expr_input, expr_output) = generate_expression_sample()

  input = choice(templates).replace("#NAME", name).replace("#VALUE", expr_input)
  output = "%s = %s" % (name, expr_output)

  return (input, output)

for i in range(1000):
  (input, output) = generate_sample()

  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")