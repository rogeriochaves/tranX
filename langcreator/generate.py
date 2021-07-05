from marko.parser import Parser
from marko.block import Heading, Paragraph, CodeBlock
from marko.inline import CodeSpan


def parse(content):
    parser = Parser()
    document = parser.parse(content)

    current_generator = None
    generators = {}
    for item in document.children:
        if type(item) == Heading:
            current_generator = item.children[0].children
            generators[current_generator] = {"inputs": [], "output": ""}
        elif type(item) == Paragraph and type(item.children[0]) == CodeSpan:
            output = item.children[0].children
            generators[current_generator]["output"] = output
        elif type(item) == CodeBlock:
            inputs = item.children[0].children.strip().split("\n")
            generators[current_generator]["inputs"] = inputs
            _check_tags(generators[current_generator])
    return generators


def _check_tags(generator):
    necessary_tags = [
        x for x in generator["output"].split(" ") if x.startswith("#")
    ]
    for index, input in enumerate(generator["inputs"]):
        for tag in necessary_tags:
            if tag not in input:
                raise Exception("missing %s in example %s of assignment `%s`" %
                                (tag, index + 1, generator["output"]))
