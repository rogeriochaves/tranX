#!/usr/bin/env python3

import sys
import os.path as path

root = path.join(path.dirname(path.realpath(__file__)), "..")
sys.path.append(root)

print("Initializing...")

from langcreator.parser import parse
from langcreator.generator import generate_samples, save_generated

with open("langcreator/natural.md") as f:
    content = f.read()

generators = parse(content)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 400 * len(generators.keys())
print(f"Generating {n} samples...")
samples = generate_samples(generators, n)
save_generated(samples)

print("Done!")