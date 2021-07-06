from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated, choice
from datasets.natural.datagen.group_generators import generate_expression_sample


def generate_sample(variable_to_use=None):
    name = variable_to_use if variable_to_use else generate_name()
    (value, value_output) = choice([generate_value(), generate_expression_sample()])

    return choice([
        f'set {name} to {value}',
        f'let {name} be {value}',
        f'{name} = {value}',
        f'{name} is {value}',
        f'set {name} equals {value}',
        f'let {name} equals {value}',
        f'put {name} into {value}',
        f'define {name} as {value}',
        f'initialize {name} as {value}',
    ]), f'{name} = {value_output}'


inputs = []
outputs = []
for i in range(2000):
    (input, output) = generate_sample()

    inputs.append(input)
    outputs.append(output)

if __name__ == '__main__':
    save_generated(__file__, inputs, outputs)
    print("Done!")
