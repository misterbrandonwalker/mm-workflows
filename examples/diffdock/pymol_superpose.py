"""Generates pymol session files with predicted poses and crystal pose"""
import argparse
from pathlib import Path

from pymol import cmd

parser = argparse.ArgumentParser()
parser.add_argument('--predicted_poses', help='List of predicted pose files')
parser.add_argument('--crystal_pose_path', type=str, help='Crystal pose file path')
parser.add_argument('--pdb_path', type=str, help='protein PDB file path')
args = parser.parse_args()

if args.predicted_poses is not None:
    predicted_poses = args.predicted_poses.split(',')
    pred_poses = [Path(i).name for i in predicted_poses]

    crystal_name = Path(args.crystal_pose_path).name
    crystal_name = crystal_name.split('.')[0]
    pdb_name = args.pdb_path.split('.')[0]
    cmd.load(args.pdb_path, 'pdb')
    cmd.load(args.crystal_pose_path)
    cmd.show('sticks', crystal_name)
    for pred_pose in pred_poses:
        cmd.load(pred_pose)
        pred_pose_name = pred_pose.split('.')[0]
        cmd.show('sticks', pred_pose_name)


    cmd.show('sticks', 'all within 5 of '+crystal_name)
    cmd.label('n. CA within 5 of '+crystal_name, 'resn')
    cmd.zoom(crystal_name)
    cmd.save(crystal_name+'.pse')
