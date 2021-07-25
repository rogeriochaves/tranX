#!/usr/bin/env python3

import sys
import os.path as path
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--name', type=str, required=True, help='Dataset to be generated, e.g. "natural" will match the langcreator/natural.md file')
arg_parser.add_argument('--samples', type=int, default=0, help='Number of samples to be generated, by default it will generate 400 * number of definitions')
args = arg_parser.parse_args()

root = path.join(path.dirname(path.realpath(__file__)), "..")
sys.path.append(root)

print("Initializing...")

from langcreator.parser import parse
from langcreator.generator import generate_samples, save_generated

with open(f"langcreator/{args.name}.md") as f:
    content = f.read()

generators = parse(content)
n = args.samples if args.samples > 0 else 400 * len(generators.keys())
print(f"Generating {n} samples...")
samples = generate_samples(generators, n)

dataset_path = path.join(path.dirname(__file__), "..", "datasets", args.name)
save_generated(samples, dataset_path)

print(f"Done! Results saved on datasets/{args.name}/inputs.txt and datasets/{args.name}/outputs.txt")