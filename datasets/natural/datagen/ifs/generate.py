from datasets.natural.datagen.base_generator import generate_value, save_generated
from datasets.natural.datagen.group_generators import generate_statement_or_expression
import datasets.natural.datagen.operations.generate as operations
from numpy.random import choice

templates = {
  "==": ["#A == #B",
         "#A is #B"],
  ">": ["#A > #B",
        "#A is greater than #B"],
  ">=": ["#A >= #B",
         "#A is greater or equal than #B"],
  "<": ["#A < #B",
        "#A is smaller than #B"],
  "<=": ["#A <= #B",
         "#A is smaller or equal than #B"],
  "!=": ["#A != #B",
         "#A is not #B",
         "#A is different than #B",
         "#A /= #B"]
}

composition_templates = {
  "and": ["#0 and #1",
          "#0 && #1"],
  "or": ["#0 or #1",
         "#0 || #1"],
}

condition_templates = [
  ("if #COND", "if #COND:"),
  ("if #COND", "if #COND:"),
  ("if #COND", "if #COND:"),
  ("#CASE_TRUE if #COND", "if #COND:\\n  #CASE_TRUE"),
  ("#CASE_TRUE if #COND", "if #COND:\\n  #CASE_TRUE"),
  ("#CASE_TRUE if #COND", "if #COND:\\n  #CASE_TRUE"),
  ("if not #COND", "if not #COND:"),
  ("if not #COND", "if not #COND:"),
  ("#CASE_TRUE if #COND else #CASE_FALSE", "if #COND:\\n  #CASE_TRUE\\nelse:\\n  #CASE_FALSE"),
  ("#CASE_TRUE if #COND else #CASE_FALSE", "if #COND:\\n  #CASE_TRUE\\nelse:\\n  #CASE_FALSE"),
  ("unless #COND", "if not #COND:"),
  ("unless #COND", "if not #COND:"),
  ("else", "else:"),
  ("if not then", "else:")
]


def generate_value_or_operation():
  if choice(["value", "operation"]) == "value":
    return generate_value()
  else:
    return operations.generate_sample()


def generate_comparison():
  comparison = choice(list(templates.keys()))
  template = choice(templates[comparison])
  (a, a_value) = generate_value_or_operation()
  (b, b_value) = generate_value_or_operation()

  comparison_input = template.replace("#A", a).replace("#B", b)
  comparison_output = "%s %s %s" % (a_value, comparison, b_value)

  if choice(["single", "nested"]) == "single":
    return (comparison_input, comparison_output)
  else:
    composition = choice(list(composition_templates.keys()))
    composition_template = choice(composition_templates[composition])

    (nested_input, nested_output) = generate_comparison()

    if choice(["parens", "no_parens"]) == "parens":
      composition_input = composition_template.replace("#0", "(" + comparison_input + ")").replace("#1", "(" + nested_input + ")")
      composition_output = "(%s) %s (%s)" % (comparison_output, composition, nested_output)
    else:
      composition_input = composition_template.replace("#0", comparison_input).replace("#1", nested_input)
      composition_output = "%s %s %s" % (comparison_output, composition, nested_output)

    return (composition_input, composition_output)


inputs = []
outputs = []
for i in range(2000):
  (comparison_input, comparison_output) = generate_comparison()
  (condition_input, condition_output) = condition_templates[choice(len(condition_templates))]

  (case_true_input, case_true_output) = generate_statement_or_expression()
  (case_false_input, case_false_output) = generate_statement_or_expression()

  input = condition_input.replace("#COND", comparison_input).replace("#CASE_TRUE", case_true_input).replace("#CASE_FALSE", case_false_input)
  output = condition_output.replace("#COND", comparison_output).replace("#CASE_TRUE", case_true_output).replace("#CASE_FALSE", case_false_output)

  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")