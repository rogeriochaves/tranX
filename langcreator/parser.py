from marko.parser import Parser
from marko.block import Heading, Paragraph, CodeBlock, List
from marko.inline import CodeSpan
from langcreator.common import tag_regex, get_tags
import collections
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
            _check_defined_twice(generators, tag_name)
            generators[tag_name] = {"inputs": [], "output": ""}
        elif type(item) == Paragraph and type(item.children[0]) == CodeSpan:
            output = item.children[0].children
            generators[tag_name]["output"] = output
        elif type(item) == CodeBlock:
            inputs = item.children[0].children.strip().split("\n")
            generators[tag_name]["inputs"] = inputs
            _check_tags(generators, tag_name)
        elif type(item) == List:
            generators[tag_name] = [
                x.children[0].children[0].children for x in item.children
            ]
    _check_previous_generator(generators, tag_name)

    _check_all_used_tags(generators)
    return generators


def _check_tags(generators, name):
    generator = generators[name]
    output = generator["output"]

    necessary_tags = get_tags(output)
    necessary_tags = dict(collections.Counter(necessary_tags))

    for index, input in enumerate(generator["inputs"]):
        input_tags = get_tags(input)
        input_tags = dict(collections.Counter(input_tags))

        for tag, count in input_tags.items():
            tag = tag.replace("'", "")
            if tag not in necessary_tags:
                raise Exception(
                    f"missing {tag} in example {index + 1} of {name} `{output}`"
                )

            diff = necessary_tags[tag] - count
            if diff > 0:
                raise Exception(
                    f"missing {diff} {tag} in example {index + 1} of {name} `{output}`. "
                    +
                    f"Expected to find {necessary_tags[tag]} {tag}, found {count}."
                )


def _check_tag_name(tag):
    if not re.fullmatch(tag_regex, "#" + tag.strip()):
        raise Exception("# %s is invalid, only letters and _ are allowed" %
                        (tag))


def _check_defined_twice(generators, tag):
    if tag in generators:
        raise Exception("# %s is being defined twice" % (tag))


def _check_previous_generator(generators, name):
    if name is None:
        return
    if type(generators[name]) == list:
        return
    if len(generators[name]["inputs"]) == 0:
        raise Exception("input examples missing on # %s" % name)
    if len(generators[name]["output"]) == 0:
        raise Exception("output missing on # %s" % name)


def _check_all_used_tags(generators):
    available_tags = ["#int", "#float", "#string", "#name"
                      ] + ["#" + x for x in generators.keys()]
    for key, generator in generators.items():
        if type(generator) == list:
            for tag in generator:
                if "#" + tag not in available_tags:
                    raise Exception(
                        "- %s is used in # %s but it's not defined anywhere. Defined tags are %s"
                        % (tag, key, ", ".join(available_tags)))
        else:
            tags = get_tags(generator["output"])
            for tag in tags:
                if tag not in available_tags:
                    raise Exception(
                        "%s is used in # %s but it's not defined anywhere. Defined tags are %s"
                        % (tag, key, ", ".join(available_tags)))
