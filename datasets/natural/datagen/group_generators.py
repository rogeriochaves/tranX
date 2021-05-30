import datasets.natural.datagen.operations.generate as operations
import datasets.natural.datagen.assignment.generate as assignment
from numpy.random import choice


def generate_statement_sample():
  # TODO: add more expressions? add if?
  if choice(["assignment", "update"]) == "assignment":
    return assignment.generate_sample()
  else:
    return operations.generate_sample_update()


def generate_expression_sample(variable_to_use=None):
  return operations.generate_sample(variable_to_use)