from typing import Dict, List, Tuple, TypeVar, TypedDict, Union
import re
import random
import numpy as np


class InputOutputGenerator(TypedDict):
    output: str
    inputs: List[str]


ListGenerator = List[str]

Generators = Dict[str, Union[InputOutputGenerator, ListGenerator]]

T = TypeVar('T')

InputOutput = Tuple[str, str]

tag_regex = r"#[\w_]+"

rng = np.random.default_rng()


def get_tags(str) -> List[str]:
    return [x for x in re.findall(tag_regex, str) if x.startswith("#")]


def set_seed(n: int):
    global rng

    random.seed(n)
    rng = np.random.default_rng(n)


def choice(list: List[T], size=None) -> T:
    return rng.choice(list, size)  # type: ignore