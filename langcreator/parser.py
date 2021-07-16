from marko.parser import Parser
from marko.block import Heading, Paragraph, CodeBlock, List
from marko.inline import CodeSpan
import re


def parse(content):
    parser = Parser()
    document = parser.parse(content)

    tag_name = None
    generators = {}
    for item in document.children:
        if type(item) == Heading:
            _check_previous_generator(generators, tag_name)
            tag_name = item.children[0].children
            _check_tag_name(tag_name)
            generators[tag_name] = {"inputs": [], "output": ""}
        elif type(item) == Paragraph and type(item.children[0]) == CodeSpan:
            output = item.children[0].children
            generators[tag_name]["output"] = output
        elif type(item) == CodeBlock:
            inputs = item.children[0].children.strip().split("\n")
            generators[tag_name]["inputs"] = inputs
            _check_tags(generators[tag_name])
        elif type(item) == List:
            generators[tag_name] = [
                x.children[0].children[0].children for x in item.children
            ]
    _check_previous_generator(generators, tag_name)

    _check_all_used_tags(generators)
    return generators


tag_regex = r"#[\w_]+"


def _check_tags(generator):
    necessary_tags = _get_tags(generator["output"])
    for index, input in enumerate(generator["inputs"]):
        for tag in necessary_tags:
            if tag not in input:
                raise Exception("missing %s in example %s of assignment `%s`" %
                                (tag, index + 1, generator["output"]))


def _check_tag_name(tag):
    if not re.fullmatch(tag_regex, "#" + tag.strip()):
        raise Exception("# %s is invalid, only letters and _ are allowed" %
                        (tag))


def _check_previous_generator(generators, name):
    if name is None:
        return
    if type(generators[name]) == list:
        return
    if len(generators[name]["inputs"]) == 0:
        raise Exception("input examples missing on # %s" % name)
    if len(generators[name]["output"]) == 0:
        raise Exception("output missing on # %s" % name)


def _get_tags(str):
    return [x for x in re.findall(tag_regex, str) if x.startswith("#")]


def _check_all_used_tags(generators):
    available_tags = ["#number", "#string", "#name"
                      ] + ["#" + x for x in generators.keys()]
    for key, generator in generators.items():
        if type(generator) == list:
            for tag in generator:
                if "#" + tag not in available_tags:
                    raise Exception(
                        "- %s is used in # %s but it's not defined anywhere. Defined tags are %s"
                        % (tag, key, ", ".join(available_tags)))
        else:
            tags = _get_tags(generator["output"])
            for tag in tags:
                if tag not in available_tags:
                    raise Exception(
                        "%s is used in # %s but it's not defined anywhere. Defined tags are %s"
                        % (tag, key, ", ".join(available_tags)))
