from datasets.natural.datagen.base_generator import value_types, generate_name, generate_value, save_generated, choice
from datasets.natural.datagen.group_generators import generate_expression_sample


def generate_declaration_sample():
    name = generate_name()
    (params_input, params_output, _) = generate_params()

    return choice([
        f"def {name} {params_input}",
        f"define function {name} {params_input}",
        f"let function {name} {params_input}",
        f"create function {name} {params_input}",
        f"function {name} {params_input}",
        f"fun {name} {params_input}",
        f"fn {name} {params_input}",
        f"subroutine {name} {params_input}",
        f"sub {name} {params_input}",
    ]), f'def {name}({params_output}):'


def generate_lambda_sample():
    name = generate_name()
    (params_input, params_output, params) = generate_params()
    variable_to_use = params[0] if len(params) > 0 else None
    (expr_input, expr_output) = generate_expression_sample(variable_to_use)

    return choice([
        f"{name} {params_input} = {expr_input}",
        f"{name} = lambda {params_input}: {expr_input}",
        f"{name} = {params_input} => {expr_input}",
        f"{name} = \{params_input} -> {expr_input}"
    ]), f"{name} = lambda {params_output}: {expr_output}"


def generate_call_sample(variable_to_use=None):
    return choice([
        generate_call_with_args(variable_to_use),
        generate_call_without_args()
    ])

def generate_call_with_args(variable_to_use=None):
    name = generate_name()
    (args_input, args_output) = generate_args(variable_to_use)

    return choice([
        f"{name}({args_input})",
        f"{name} {args_input}",
        f"call {name} with ({args_input})",
        f"call {name} with {args_input}",
    ]), f"{name}{args_output}"


def generate_call_without_args():
    name = generate_name()

    return choice([f"{name}()", f"call {name}"]), f"{name}()"



def generate_params():
    params_length = choice([0, 1, 1, 1, 2, 2, 2, 3])
    if params_length == 0:
        return ("()", "", [])
    params = [generate_name() for _ in range(params_length)]

    input = choice([ \
        f"({', '.join(params)})",
        ", ".join(params),
        " ".join(params)
    ])

    return input, ", ".join(params), params


def generate_args(variable_to_use=None):
    args_length = choice([1, 1, 1, 2, 2, 2, 3])
    if args_length == 0:
        return ("", "()")

    args = [generate_value(value_types, depth=1) for _ in range(args_length)]
    if variable_to_use is not None and len(args) > 0:
        args[0] = (variable_to_use, variable_to_use)

    args_input = [x[0] for x in args]
    args_output = [x[1] for x in args]

    return choice([", ".join(args_input),
                   " ".join(args_input)]), f"({', '.join(args_output)})"


inputs = []
outputs = []
for i in range(2000):
    (input, output) = choice([
        generate_declaration_sample(),
        generate_lambda_sample(),
        generate_call_sample(),
    ])
    inputs.append(input)
    outputs.append(output)

if __name__ == '__main__':
    save_generated(__file__, inputs, outputs)
    print("Done!")
