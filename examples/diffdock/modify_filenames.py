"""Append variables to filename"""
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--file_names', type=str, help='file paths')
parser.add_argument('--inference_steps', type=str, help='inference_steps')
parser.add_argument('--samples_per_complex', type=str, help='samples_per_complex')
args = parser.parse_args()
if args.file_names is not None:
    file_names = args.file_names.split(',')
    file_names = [Path(i).name for i in file_names]
    for file_name in file_names:
        new_file_name = f"mod_{args.inference_steps}_{args.samples_per_complex}_{file_name}"
        shutil.copy(file_name, new_file_name)
