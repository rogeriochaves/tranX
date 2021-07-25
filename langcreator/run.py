#!/usr/bin/env python3

import sys
import os
import os.path as path
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--from', type=str, required=True, help='Your language definition file path, e.g. natural/natural.md')
arg_parser.add_argument('--output', type=str, help='Where to store the generated inputs.txt and outputs.txt files, by default it saves to /dataset on the same folder of --from file')
arg_parser.add_argument('--num', type=int, default=0, help='Number of samples to be generated, by default it will generate 400 * number of definitions')
args = arg_parser.parse_args()

root = path.join(path.dirname(path.realpath(__file__)), "..")
sys.path.append(root)

print("Initializing...")

from langcreator.parser import parse
from langcreator.generator import generate_samples, save_generated

definitions_path = getattr(args, 'from')
with open(definitions_path) as f:
    content = f.read()

generators = parse(content)
n = args.num if args.num > 0 else 400 * len(generators.keys())
print(f"Generating {n} samples...")
samples = generate_samples(generators, n)

output_path = args.output if args.output else path.join(path.dirname(definitions_path), "dataset")
os.makedirs(output_path)
save_generated(samples, output_path)

print(f"Done! Results saved on {output_path}/inputs.txt and {output_path}/outputs.txt")