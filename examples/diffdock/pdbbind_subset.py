"""Collects post-processed PDB bind subset from DiffDock docker image"""
import argparse
import shutil
from pathlib import Path
import os

parser = argparse.ArgumentParser()

parser.add_argument('--pdb_ids', type=str, help='File of PDB ids to use')
parser.add_argument('--max_output', type=int, \
                    help='Max number of output PDB complexes for debugging purposes')
args = parser.parse_args()
cur_dir = Path().absolute()

# Grab subset of PDB id's to copy for DiffDock
temp = open(args.pdb_ids, 'r', encoding='UTF-8')
results = temp.readlines()
temp.close()
subset_pdbs = []
for line in results:
    line_split = line.split()
    pdb_id = line_split[0]
    subset_pdbs.append(pdb_id)

# Copy PDB files from Docker image location into working directory
COUNT = 0
files = os.listdir("/DiffDock/data/")
for f in files:
    if COUNT >= args.max_output:
        break
    if Path(f).is_dir():
        if Path(f).name in subset_pdbs:
            inner_files = os.listdir(f)
            for inner_file in inner_files:
                inner_file = Path(inner_file).name
                ext = inner_file.split('.')[1]
                if ext == 'sdf' or ext == 'pdb':
                    new_path = Path(cur_dir).joinpath(inner_file)
                    shutil.copy(inner_file, new_path.resolve())
                    COUNT += 1
