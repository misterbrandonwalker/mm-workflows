"""Generate tables and plots for DiffDock"""
import sys
import json
import csv
from typing import Dict, List

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


json_files = sys.argv[1:]


def get_confidence(file_name: str) -> float:
    """This function return confidence score from filename

    Args:
        file_name: The filename of output pose

    Returns:
        retval: The confidence value from pose
    """
    delim = "confidence"
    split = file_name.split(delim)
    second = split[1]
    split = second.split('.')
    conf = float(''.join(split[:-1]))
    return conf


def rmsd_fraction_gen_smples_top_confidence(samples_per_complex_ins: int, top_n_confidence: int,\
                             gen_samples_to_pose_info_ins: Dict, rmsd_cutoff: float) -> float:
    """This function returns the fraction of poses that have RMSD below input cutoff 
    for a given samples_per_complex_ins 

    Args:
        samples_per_complex_ins: Number of samples generated for DiffDock
        top_n_confidence: Number of highest confident poses to return 
        gen_samples_to_pose_info_ins: Dictionary containing information such as RMSD and 
        confidence values
        rmsd_cutoff: Cutoff value for RMSD, return all poses that have RMSD below or 
        equal to this value

    Returns:
        retval: fraction of poses that have RMSD below input cutoff
    """
    pose_dict = gen_samples_to_pose_info_ins[samples_per_complex_ins]
    confidence_to_pose = {}
    for pose, value_ins in pose_dict.items():
        rmsd_value = value_ins['RMSD']
        confidence_ins = value_ins['confidence']
        if rmsd_value <= rmsd_cutoff:
            confidence_to_pose[confidence_ins] = pose
    sorted_dict = dict(sorted(confidence_to_pose.items(), reverse=True))
    poses = list(sorted_dict.values())[:top_n_confidence]
    return len(poses)/len(pose_dict.items())


def plot_diffdock_rmsd_performance(gen_samples_to_pose_info_ins: Dict, \
                                   rmsd_cutoff: float = 2) -> None:
    """This function plots RMSD performance (beneath cutoff) vs number of generated poses

    Args: 
        gen_samples_to_pose_info_ins: Dictionary containing information such as RMSD and 
        confidence values
        rmsd_cutoff: Cutoff value for RMSD, return all poses that have RMSD below or 
        equal to this value

    """
    plt.clf()
    plt.title("DiffDock Performance")
    confidence_array = [1, 5, 10]
    for top_n_confidence in confidence_array:
        hist_array = []
        samples_array = []
        for samples_per_complex_ins in gen_samples_to_pose_info_ins.keys():
            fraction = rmsd_fraction_gen_smples_top_confidence(
                samples_per_complex, top_n_confidence, gen_samples_to_pose_info_ins, rmsd_cutoff)
            hist_array.append(fraction)
            samples_array.append(samples_per_complex_ins)

        plt.plot(samples_array, hist_array, label="Top-"+str(top_n_confidence)+' Performance')
    plt.legend()
    plt.xlabel('Number of generative samples')
    plt.ylabel('Fraction with RMSD <'+str(rmsd_cutoff)+'angstroms')
    plt.show()
    plt.savefig('DiffDockPerformance.png')


def grab_array(gen_samples_to_pose_info_ins: Dict) -> List[float]:
    """This function returns all of the RMSD values for all poses

    Args: 
        gen_samples_to_pose_info_ins: Dictionary containing information such as RMSD and 
        confidence values

    Returns:
        retval: array of RMSD values for all poses
    """
    rmsd_array = []
    for samples_per_complex_ins, pose_dict in gen_samples_to_pose_info_ins.items():
        for pose in pose_dict.keys():
            rmsd_ins = pose_dict[pose]['RMSD']
            rmsd_array.append(rmsd_ins)
    return rmsd_array


def plot_rmsd_cdf(gen_samples_to_pose_info_ins: Dict) -> None:
    """This function plots the cumulative distribution function for RMSD

    Args: 
        gen_samples_to_pose_info_ins: Dictionary containing information such as RMSD and 
        confidence values
    """
    rmsd_array = grab_array(gen_samples_to_pose_info_ins)
    count, bins_count = np.histogram(rmsd_array)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.clf()
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
    plt.xlabel('RMSD (Å)')
    plt.ylabel('Fraction with lower RMSD')
    plt.show()
    plt.savefig('DiffDockPerformanceRMSD-CDF.png')


gen_samples_to_pose_info:Dict[int, Dict[str, Dict]] = {}
headers = ['Protein', 'Ligand', 'Inference Steps', 'Samples Per Complex', \
           'Batch Size', 'Actual Steps', 'Top N Confident Poses',
           'Top % Confident Poses', 'No Final Step Noise', 'Wall Time', \
            'Pose', 'RMSD', 'Diffusion Trajectory', 'Pymol']
with open('DiffDockResults.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for i, json_file in enumerate(json_files):
        row = []
        f = open(json_file, encoding='UTF-8')
        meta_dict = json.load(f)
        ligand_path = meta_dict['ligand']
        protein_path = meta_dict['protein']
        exec_time = meta_dict['time']
        if 'rmsd' in meta_dict:
            rmsd_dict = meta_dict['rmsd']
        else:
            rmsd_dict = {}
        inference_steps = meta_dict['inference_steps']
        samples_per_complex = meta_dict['samples_per_complex']
        if samples_per_complex not in gen_samples_to_pose_info:
            gen_samples_to_pose_info[samples_per_complex] = {}
        top_percent_confidence = meta_dict['top_percent_confidence']
        batch_size = meta_dict['batch_size']
        actual_steps = meta_dict['actual_steps']
        top_n_confident = meta_dict['top_n_confident']
        no_final_step_noise = meta_dict['no_final_step_noise']
        if 'pymol' in meta_dict:
            SESSION = meta_dict['pymol']
        else:
            SESSION = ''
        row.append(protein_path)
        row.append(ligand_path)
        row.append(inference_steps)
        row.append(samples_per_complex)
        row.append(batch_size)
        row.append(actual_steps)
        row.append(top_n_confident)
        row.append(top_percent_confidence)
        row.append(no_final_step_noise)
        row.append(exec_time)
        CUR_LENTGH = len(row)
        for key, value in rmsd_dict.items():
            if len(row) == 0:
                row = [""]*CUR_LENTGH
            rmsd = value['RMSD']
            traj = value['traj']
            POSE = str(key)
            confidence = get_confidence(POSE)
            gen_samples_to_pose_info[samples_per_complex][POSE] = {}
            gen_samples_to_pose_info[samples_per_complex][POSE]['RMSD'] = rmsd
            gen_samples_to_pose_info[samples_per_complex][POSE]['confidence'] = confidence
            row.append(POSE)
            row.append(rmsd)
            row.append(traj)
            row.append(SESSION)
            writer.writerow(row)
            row = []

plot_diffdock_rmsd_performance(gen_samples_to_pose_info)
plot_rmsd_cdf(gen_samples_to_pose_info)
