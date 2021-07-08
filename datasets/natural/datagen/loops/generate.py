from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated, choice
from datasets.natural.datagen.group_generators import generate_statement_or_expression
import datasets.natural.datagen.ifs.generate as ifs
from numpy.random import rand


def loop():
    var = generate_name()
    (list_input, list_output) = generate_value(['variable', 'list'])
    min = choice([0, 1, 5, 10])
    max = str(
        min +
        choice([1, 5, 10, 50, 100])) if rand() < 0.5 else generate_name()
    min = str(min) if rand() < 0.9 else generate_name()
    (comparison_input, comparison_output) = ifs.generate_comparison()
    (expr_input,
     expr_output) = generate_statement_or_expression(variable_to_use=var)

    for_each = choice([ \
      f"for {var} in {list_input}",
      f"each {var} in {list_input}"
    ]), f"for {var} in {list_output}:"

    for_each_do = choice([ \
      f"{expr_input} for each {var} in {list_input}",
      f"{expr_input} for each {var} of {list_input}"
    ]), f"for {var} in {list_output}:\\n  {expr_output}"

    times_loop = choice([ \
      f"{max} times do",
      f"repeat {max} times",
      f"do {max} times"
    ]), f"for _ in range({max}):"

    times_loop_do = choice([ \
      f"{expr_input} {max} times",
      f"repeat {expr_input} {max} times",
      f"do {expr_input} {max} times"
    ]), f"for _ in range({max}):\\n  {expr_output}"

    for_range = choice([ \
       f"for {var} in {min} to {max}",
       f"for {var} in {min}..{max}"
    ]), f"for {var} in range({min}, {max}):"

    for_range_do = choice([ \
      f"{expr_input} for {var} in {min} to {max}",
      f"{expr_input} for {var} in {min}..{max}"
    ]), f"for {var} in range({min}, {max}):\\n  {expr_output}"

    while_ = choice([ \
      f"while {comparison_input}",
      f"while {comparison_input} do"
    ]), f"while {comparison_output}:"

    while_do = f"{expr_input} while {comparison_input}", \
      f"while {comparison_output}:\\n  {expr_output}"

    until_do = f"{expr_input} until {comparison_input}", \
      f"while not {comparison_output}:\\n  {expr_output}"

    infinite = choice([ \
      "while true",
      "loop"
    ]), "while True:"

    break_ = choice([ \
      "break",
      "exit loop",
      "end the loop"
    ]), "break"

    continue_ = choice([ \
      "continue",
      "next",
      "jump to next item in the loop"
    ]), "continue"

    return choice([
        for_each, for_each_do, times_loop, times_loop_do, for_range,
        for_range_do, while_, while_do, until_do, infinite, break_, continue_
    ])


inputs = []
outputs = []
for i in range(2000):
    input, output = loop()

    inputs.append(input)
    outputs.append(output)

if __name__ == '__main__':
    save_generated(__file__, inputs, outputs)
    print("Done!")
