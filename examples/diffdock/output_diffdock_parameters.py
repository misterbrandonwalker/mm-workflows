"""Collect DiffDock inputs and outputs into json file"""
import argparse
import json
from typing import Dict
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument('--execution_time', help='Execution time value', required=True)
parser.add_argument('--rmsd', help='RMSD dictionary', required=True)
parser.add_argument('--output_json_name', type=str, help='Output json file')
parser.add_argument('--protein_path', type=str, help='Protein used')
parser.add_argument('--ligand_path', type=str, help='Ligand used')
parser.add_argument('--inference_steps', type=str, help='inference_steps')
parser.add_argument('--samples_per_complex', type=str, help='samples_per_complex')
parser.add_argument('--batch_size', type=str, help='batch_size')
parser.add_argument('--actual_steps', type=str, help='actual_steps')
parser.add_argument('--no_final_step_noise', dest='no_final_step_noise',
                    action='store_true', help='no_final_step_noise')
parser.add_argument('--top_n_confident', type=str, help='top_n_confident')
parser.add_argument('--top_percent_confidence', type=str, help='top_percent_confidence')
parser.add_argument('--pymol_session', type=str, help='Pymol session')
parser.set_defaults(no_final_step_noise=False)
args = parser.parse_args()


def return_json_file(input_dict: Dict, output_file: str) -> None:
    """This function returns a json file from an input dictionary

    Args: 
        input_dict: Input dictionary to be saved as a json file
        output_file: Name of json file to be saved
    """
    with open(output_file, "w", encoding='UTF-8') as outfile:
        json.dump(input_dict, outfile, indent=2)


ligand_path = Path(args.ligand_path).name
protein_path = Path(args.protein_path).name

results = {}
results['top_percent_confidence'] = args.top_percent_confidence
results['inference_steps'] = args.inference_steps
results['samples_per_complex'] = args.samples_per_complex
results['batch_size'] = args.batch_size
results['actual_steps'] = args.actual_steps
results['no_final_step_noise'] = args.no_final_step_noise
results['top_n_confident'] = args.top_n_confident
results['ligand'] = ligand_path
results['protein'] = protein_path
results['time'] = args.execution_time
if args.pymol_session is not None:
    results['pymol'] = Path(args.pymol_session).name
results['rmsd'] = {}
with open(args.rmsd, encoding='UTF-8') as user_file:
    parsed_json = json.load(user_file)
    for key, value in parsed_json.items():
        results['rmsd'][key] = value

return_json_file(results, args.output_json_name)
