from numpy.random import choice


def generate_statement_sample():
  import datasets.natural.datagen.operations.generate as operations
  import datasets.natural.datagen.assignment.generate as assignment

  # TODO: add more expressions? add if?
  if choice(["assignment", "update"]) == "assignment":
    return assignment.generate_sample()
  else:
    return operations.generate_sample_update()


def generate_expression_sample(variable_to_use=None):
  import datasets.natural.datagen.operations.generate as operations
  import datasets.natural.datagen.functions.generate as functions

  type = choice(["expression", "function call"])
  if type == "expression":
    return operations.generate_sample(variable_to_use)
  elif type == "function call":
    return functions.generate_call_sample(variable_to_use)

  raise Exception()