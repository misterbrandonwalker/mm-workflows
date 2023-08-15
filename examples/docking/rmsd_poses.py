"""Cluster predicted diffdock poses by centroid, \
    keep most confident from each cluster then compute RMSD to crystal pose"""
import argparse
import json
from pathlib import Path
import shutil
from typing import Dict, Any

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolTransforms as rdmt
from openbabel import openbabel
import numpy as np



parser = argparse.ArgumentParser()
parser.add_argument('--predicted_poses', help='List of predicted pose files', required=True)
parser.add_argument('--diffusion_trajectory', \
                    help='each diffusion trajectory saved in PDB', required=True)
parser.add_argument('--crystal_pose_path', type=str, help='Crystal pose file path')
parser.add_argument('--output_json_name', type=str, help='Output json file')
parser.add_argument('--centroid_cutoff', type=float, \
                    help='RMSD cutoff for clusters of poses in same protein pocket')
parser.add_argument('--use_clustering_filter', dest='use_clustering_filter', \
                    action='store_true', help='')
parser.set_defaults(use_clustering_filter=False)
args = parser.parse_args()

obConversion = openbabel.OBConversion()
obConversion.SetInFormat('sdf')
obConversion.SetOutFormat('mol')

# strip file path and just keep filenames
if args.predicted_poses is not None:
    predicted_poses = args.predicted_poses.split(',')
    predicted_poses = [Path(i).name for i in predicted_poses]
    poses = []
    for pred_pose in predicted_poses:
        ligmol = openbabel.OBMol()
        obConversion.ReadFile(ligmol, pred_pose)
        molname = pred_pose.replace('.sdf', '.mol')
        obConversion.WriteFile(ligmol, molname)
        poses.append(molname)

diffusion_trajectory = args.diffusion_trajectory.split(',')
diffusion_trajectory = [Path(i).name for i in diffusion_trajectory]

args.crystal_pose_path = Path(args.crystal_pose_path).name


def return_json_file(input_dict: Dict, output_file: str) -> None:
    """This function returns a json file from an input dictionary

    Args: 
        input_dict: Input dictionary to be saved as a json file
        output_file: Name of json file to be saved
    """
    with open(output_file, "w", encoding='UTF-8') as outfile:
        json.dump(input_dict, outfile, indent=2)


def parse_confidence(file_name: str) -> float:
    """This function return confidence score from filename

    Args:
        file_name: The filename of output pose

    Returns:
        retval: The confidence value from pose
    """
    delim_ins = "confidence"
    split_ins = file_name.split(delim_ins)
    second = split_ins[1]
    split_ins = second.split('.')
    confidence = float(''.join(split_ins[:-1]))
    return confidence

# Compute centroid distance for each pose pair
pred_mols = [Chem.MolFromMolFile(i) for i in poses]
mat = np.zeros((len(pred_mols), len(pred_mols)))
index_to_name = {}
for i, pred_mol in enumerate(pred_mols):
    pred_name = poses[i]
    index_to_name[i] = pred_name
    conf = pred_mol.GetConformers()[0]
    center = rdmt.ComputeCentroid(conf)
    for j, opred_mol in enumerate(pred_mols):
        opred_mol = pred_mols[j]
        opred_name = poses[j]
        oconf = opred_mol.GetConformers()[0]
        ocenter = rdmt.ComputeCentroid(oconf)
        mat[i, j] = np.linalg.norm(center-ocenter)

# Cluster a pose into group of other poses via centroid distance if beneath threshold
true_poses = []
for i, pred_name in enumerate(poses):
    centroid_row = mat[i, :]
    indices = []
    for j, entry in enumerate(centroid_row):
        if entry <= args.centroid_cutoff:
            indices.append(j)
    names = [index_to_name[k] for k in indices]
    confidences = [parse_confidence(k) for k in names]
    confidence_to_name = dict(zip(confidences, names))
    max_confidence = max(confidence_to_name.keys())
    max_name = confidence_to_name[max_confidence]
    new_name = 'filtered_'+max_name
    shutil.copy(max_name, new_name)
    true_poses.append(new_name)

if args.use_clustering_filter is False:
    true_poses = poses[:]

# Generate rdkit objects for computing RMSD
ref_mol = Chem.MolFromMolFile(args.crystal_pose_path)
pred_mols = [Chem.MolFromMolFile(i) for i in true_poses]

# map predicted pose to corresponding diffusion trajectory file
DELIM = "_"
ligand_to_pocket = {}
for i in range(len(pred_mols)):
    pose = true_poses[i]
    split = pose.split(DELIM)
    rank = split[-2]
    for j, traj in enumerate(diffusion_trajectory):
        if rank in traj:
            ligand_to_pocket[pose] = traj

# save pose name, RMSD and diffusion trajectory filename to json file
output: Dict[str, Dict[str, Any]] = {}
for i, pred_mol in enumerate(pred_mols):
    pred_name = true_poses[i]
    RMSD = AllChem.GetBestRMS(pred_mol, ref_mol)
    output[pred_name] = {}
    output[pred_name]['traj'] = ligand_to_pocket[pred_name]
    output[pred_name]['RMSD'] = RMSD

return_json_file(output, args.output_json_name)
