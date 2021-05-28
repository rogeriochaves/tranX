from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated
import datasets.natural.datagen.operations.generate as operations
import datasets.natural.datagen.assignment.generate as assignment
from numpy.random import choice

templates = {
  "==": ["#A == #B",
         "#A is #B"],
  ">": ["#A > #B",
        "#A is greater than #B"],
  ">=": ["#A >= #B",
         "#A is greater or equal than #B"],
  "<": ["#A < #B",
        "#A is simaller than #B"],
  "<=": ["#A <= #B",
         "#A is smaller or equal than #B"],
  "!=": ["#A != #B",
         "#A is not #B",
         "#A is different than #B",
         "#A /= #B"]
}

condition_templates = [
  ("if #COND", "if #COND:"),
  ("if #COND", "if #COND:"),
  ("#CASE_TRUE if #COND", "if #COND:\\n  #CASE_TRUE"),
  ("#CASE_TRUE if #COND", "if #COND:\\n  #CASE_TRUE"),
  ("if not #COND", "if not #COND:"),
  ("#CASE_TRUE if #COND else #CASE_FALSE", "if #COND:\\n  #CASE_TRUE\\nelse:\\n  #CASE_FALSE"),
  ("unless #COND", "if not #COND:"),
  ("else", "else:"),
  ("if not then", "else:")
]

def generate_expression_sample():
  if choice(["assignment", "update"]) == "assignment":
    return assignment.generate_sample()
  else:
    return operations.generate_sample_update()

def generate_value_or_operation():
  if choice(["value", "operation"]) == "value":
    return generate_value()
  else:
    return operations.generate_sample()

inputs = []
outputs = []
for i in range(1000):
  comparison = choice(list(templates.keys()))
  template = choice(templates[comparison])
  (a, a_value) = generate_value_or_operation()
  (b, b_value) = generate_value_or_operation()

  (condition_input, condition_output) = condition_templates[choice(len(condition_templates))]
  comparison_input = template.replace("#A", a).replace("#B", b)
  comparison_output = "%s %s %s" % (a_value, comparison, b_value)

  (case_true_input, case_true_output) = generate_expression_sample()
  (case_false_input, case_false_output) = generate_expression_sample()

  input = condition_input.replace("#COND", comparison_input).replace("#CASE_TRUE", case_true_input).replace("#CASE_FALSE", case_false_input)
  output = condition_output.replace("#COND", comparison_output).replace("#CASE_TRUE", case_true_output).replace("#CASE_FALSE", case_false_output)

  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")