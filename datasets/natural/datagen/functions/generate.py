from datasets.natural.datagen.base_generator import value_types, generate_name, generate_value, save_generated
from datasets.natural.datagen.group_generators import generate_expression_sample
from numpy.random import choice, rand

declaration_templates = ["def #NAME #PARAMS",
                         "define function #NAME #PARAMS",
                         "let function #NAME #PARAMS",
                         "create function #NAME #PARAMS",
                         "function #NAME #PARAMS",
                         "fun #NAME #PARAMS",
                         "fn #NAME #PARAMS",
                         "subroutine #NAME #PARAMS",
                         "sub #NAME #PARAMS"]

lambda_templates = ["#NAME #PARAMS = #EXPR",
                    "#NAME = lambda #PARAMS: #EXPR",
                    "#NAME = #PARAMS => #EXPR",
                    "#NAME = \#PARAMS -> #EXPR"]

call_templates = ["#NAME #ARGS",
                  "#NAME #ARGS",
                  "#NAME #ARGS",
                  "call #NAME with #ARGS",
                  "call #NAME"]

# Function definition
templates_params = [
  lambda params: "(" + ", ".join(params) + ")",
  lambda params: ",".join(params),
  lambda params: " ".join(params),
]

# Calling function
templates_args = [
  lambda params: "(" + ", ".join(params) + ")",
  lambda params: ",".join(params),
  lambda params: " ".join(params),
]

def generate_params():
  params_length = int(rand() * 3) + 1
  if params_length == 0:
    return ("()", "")

  params = [ generate_name() for _ in range(params_length) ]
  params_input = choice(templates_params)(params)
  params_output = ", ".join(params)

  return (params_input, params_output, params)

def generate_args():
  args_length = choice([0, 1, 1, 1, 2, 2, 2, 3])
  if args_length == 0:
    return ("()", "()")

  args = [ generate_value(value_types, depth=1) for _ in range(args_length) ]
  args_input = [ x[0] for x in args ]
  args_output = [ x[1] for x in args ]
  args_input = choice(templates_args)(args_input)
  args_output = "(" + ", ".join(args_output) + ")"

  return (args_input, args_output)

def generate_declaration_sample():
  template = choice(declaration_templates)
  name = generate_name()
  (params_input, params_output, _) = generate_params()

  input = template.replace("#NAME", name).replace("#PARAMS", params_input)
  output = "def %s(%s):" % (name, params_output)

  return input, output

def generate_lambda_sample():
  template = choice(lambda_templates)
  name = generate_name()
  (params_input, params_output, params) = generate_params()
  variable_to_use = params[0] if len(params) > 0 else None
  (expr_input, expr_output) = generate_expression_sample(variable_to_use)

  input = template.replace("#NAME", name).replace("#PARAMS", params_input).replace("#EXPR", expr_input)
  output = "%s = lambda %s: %s" % (name, params_output, expr_output)

  return input, output

def generate_call_sample(variable_to_use=None):
  template = choice(call_templates)

  name = generate_name()
  if variable_to_use is not None:
    name = variable_to_use
  (args_input, args_output) = generate_args()

  input = template.replace("#NAME", name).replace("#ARGS", args_input)
  if args_input[0] == "(" and args_input[-1] == ")":
    input = input.replace(" (", "(").replace("with(", "with (")
  output = "%s%s" % (name, args_output)
  if "#ARGS" not in template:
    output = "%s()" % (name)

  return input, output

inputs = []
outputs = []
for i in range(500):
  (input, output) = generate_declaration_sample()
  inputs.append(input)
  outputs.append(output)

for i in range(500):
  (input, output) = generate_lambda_sample()
  inputs.append(input)
  outputs.append(output)

for i in range(1000):
  (input, output) = generate_call_sample()
  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")