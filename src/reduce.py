#!/usr/bin/env python3

import argparse
import glob
import json
from collections import Counter, defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', default='outputs')
parser.add_argument('--output_path', required=True)  # e.g. 'reduced.lang'
parser.add_argument('--input_type', required=True, choices=['lang', 'country'])
args = parser.parse_args()

total = defaultdict(lambda: Counter())

# find all files of the right type
pattern = f'{args.input_folder}/*.{args.input_type}'
paths = glob.glob(pattern)
print(f'Found {len(paths)} files to reduce')

for path in paths:
    with open(path) as f:
        daily = json.load(f)
    
    for hashtag, counts in daily.items():
        total[hashtag].update(counts)  # Counter.update() adds counts together

with open(args.output_path, 'w') as f:
    json.dump({k: dict(v) for k, v in total.items()}, f)

print(f'Saved to {args.output_path}')
