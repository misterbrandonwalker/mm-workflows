"""Ranks predicted poses from DiffDock via confidence score"""
import argparse
from pathlib import Path
import shutil
import os
from typing import List, Tuple

parser = argparse.ArgumentParser()

parser.add_argument('--top_n_confident', type=int, help='Top n confident poses')
parser.add_argument('--top_percent_confidence', type=float, help='top confidence percent cutoff')
args = parser.parse_args()
base_dir = Path().absolute()

# Map confidence value to pose for filtering step
DELIM = "confidence"
confidence_to_pose = {}
for root, dirs, files in os.walk("."):
    for f in files:
        if DELIM in f:
            split = f.split(DELIM)
            rank = split[0]
            second = split[1]
            split = second.split('.')
            ext = split[-1]
            confidence = float(''.join(split[:-1]))
            confidence_to_pose[confidence] = f

# First filter by absolute value top_n_confident
sorted_list = sorted(confidence_to_pose.items(), reverse=True)
sorted_pose_list = [v for (k,v) in sorted_list]
poses = sorted_pose_list[:args.top_n_confident]

# Next filter by top percentage of confident poses
num_poses = int(args.top_percent_confidence*.01*len(poses))
poses = poses[:num_poses]

# Find the output predicted poses and then if its in list of ranked poses,
# copy filename to be used in next workflow step
# Beware of issues with shutil.copy https://docs.python.org/3/library/shutil.html
for root, dirs, files in os.walk("."):
    for f in files:
        if DELIM in f:
            split = f.split(DELIM)
            rank = split[0]
            if f in poses:
                for of in files:
                    split = of.split('.')
                    ext = split[-1]
                    if rank in of and ext == 'pdb':
                        final_path = Path(base_dir).joinpath('ranked'+'_'+f)
                        current_path = Path(root).joinpath(f)
                        shutil.copy(current_path, final_path)
                        final_path = Path(base_dir).joinpath('ranked'+'_'+of)
                        current_path = Path(root).joinpath(of)
                        shutil.copy(current_path, final_path)
