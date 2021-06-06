from datasets.natural.datagen.base_generator import generate_name, generate_value, save_generated
from datasets.natural.datagen.group_generators import generate_statement_or_expression
import datasets.natural.datagen.ifs.generate as ifs
from numpy.random import choice

templates = {
  "for-each": ["for #VAR in #LIST",
               "each #VAR in #LIST"],
  "for-each-do": ["#EXPR for each #VAR in #LIST",
                  "#EXPR for each #VAR of #LIST"],
  "times-loop": ["#MAX times do",
                 "repeat #MAX times",
                 "do #MAX times"],
  "times-loop-do": ["#EXPR #MAX times",
                    "repeat #EXPR #MAX times",
                    "do #EXPR #MAX times"],
  "for-range": ["for #VAR in #MIN to #MAX",
                "for #VAR in #MIN..#MAX",
                "from #MIN to #MAX do"],
  "for-range-do": ["#EXPR for #VAR in #MIN to #MAX",
                   "#EXPR for #VAR in #MIN..#MAX"],
  "while": ["while #COND",
            "while #COND do"],
  "while-do": ["#EXPR while #COND"],
  "until-do": ["#EXPR until #COND"],
  "infinite": ["while true",
               "loop"],
  "break": ["break", "exit loop", "end the loop"],
  "continue": ["continue", "next", "jump to next item in the loop"],
}


inputs = []
outputs = []
for i in range(2000):
  loop = choice(list(templates.keys()))
  template = choice(templates[loop])

  var = generate_name()
  (list_input, list_output) = generate_value(['variable', 'list'])
  min = choice([0, 1, 5, 10])
  max = str(min + choice([0, 1, 5, 10, 50, 100]))
  min = str(min)
  (comparison_input, comparison_output) = ifs.generate_comparison()
  (expr_input, expr_output) = generate_statement_or_expression(variable_to_use=var)

  if loop == "for-each":
    input = template.replace("#VAR", var).replace("#LIST", list_input)
    output = "for %s in %s:" % (var, list_output)
  elif loop == "for-each-do":
    input = template.replace("#VAR", var).replace("#LIST", list_input).replace("#EXPR", expr_input)
    output = "for %s in %s:\\n  %s" % (var, list_output, expr_output)
  elif loop == "times-loop":
    input = template.replace("#MAX", max)
    output = "for _ in range(%s):" % (max)
  elif loop == "times-loop-do":
    input = template.replace("#MAX", max).replace("#EXPR", expr_input)
    output = "for _ in range(%s):\\n  %s" % (max, expr_output)
  elif loop == "for-range":
    input = template.replace("#VAR", var).replace("#MIN", min).replace("#MAX", max)
    output = "for %s in range(%s, %s):" % (var, min, max)
  elif loop == "for-range-do":
    input = template.replace("#VAR", var).replace("#MIN", min).replace("#MAX", max).replace("#EXPR", expr_input)
    output = "for %s in range(%s, %s):\\n  %s" % (var, min, max, expr_output)
  elif loop == "while":
    input = template.replace("#COND", comparison_input)
    output = "while %s:" % (comparison_output)
  elif loop == "while-do":
    input = template.replace("#COND", comparison_input).replace("#EXPR", expr_input)
    output = "while %s:\\n  %s" % (comparison_output, expr_output)
  elif loop == "until-do":
    input = template.replace("#COND", comparison_input).replace("#EXPR", expr_input)
    output = "while not %s:\\n  %s" % (comparison_output, expr_output)
  elif loop == "infinite":
    input = template
    output = "while True:"
  elif loop == "break":
    input = template
    output = "break"
  elif loop == "continue":
    input = template
    output = "continue"

  inputs.append(input)
  outputs.append(output)

if __name__ == '__main__':
  save_generated(__file__, inputs, outputs)
  print("Done!")