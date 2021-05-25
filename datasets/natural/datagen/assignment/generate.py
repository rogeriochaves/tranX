from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated
import datasets.natural.datagen.operations.generate as addition
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
  output = name + " = " + real_value

  inputs.append(input)
  outputs.append(output)

for i in range(1000):
  name = generate_name()
  (expr_input, expr_output) = addition.generate_sample()

  input = choice(templates).replace("#NAME", name).replace("#VALUE", expr_input)
  output = "%s = %s" % (name, expr_output)

  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")