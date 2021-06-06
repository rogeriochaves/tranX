from numpy.random import choice


def generate_statement_sample(variable_to_use=None):
  import datasets.natural.datagen.operations.generate as operations
  import datasets.natural.datagen.assignment.generate as assignment

  # TODO: add more expressions? add if?
  if choice(["assignment", "update"]) == "assignment":
    return assignment.generate_sample(variable_to_use)
  else:
    return operations.generate_sample_update(variable_to_use)


def generate_expression_sample(variable_to_use=None):
  import datasets.natural.datagen.operations.generate as operations
  import datasets.natural.datagen.functions.generate as functions

  type = choice(["expression", "function call"])
  if type == "expression":
    return operations.generate_sample(variable_to_use)
  elif type == "function call":
    return functions.generate_call_sample(variable_to_use)

  raise Exception()


def generate_statement_or_expression(variable_to_use=None):
  if choice(["statement", "expression"]) == "statement":
    return generate_statement_sample(variable_to_use)
  else:
    return generate_expression_sample(variable_to_use)