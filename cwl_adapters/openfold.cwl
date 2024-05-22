#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: OpenFold Inference

baseCommand: ["python3", "run_pretrained_openfold.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/openfold-tool:0.1.0

inputs:

  input_fasta_dir:
    type: Directory
    inputBinding:
      position: 1

  mmcif_dir:
    type: Directory
    inputBinding:
      position: 2

  output_dir:
    type: Directory
    inputBinding:
      prefix: --output_dir
      position: 3

  config_preset:
    type: string?
    default: model_1_ptm
    inputBinding:
      prefix: --config_preset

  uniref90_database_path:
    type: Directory
    inputBinding:
      prefix: --uniref90_database_path
      position: 4

  mgnify_database_path:
    type: File
    inputBinding:
      prefix: --mgnify_database_path
      position: 5

  pdb70_database_path:
    type: Directory
    inputBinding:
      prefix: --pdb70_database_path
      position: 6

  uniclust30_database_path:
    type: Directory
    inputBinding:
      prefix: --uniclust30_database_path
      position: 7

  bfd_database_path:
    type: File
    inputBinding:
      prefix: --bfd_database_path
      position: 8

  model_device:
    type: string?
    default: "cuda:0"
    inputBinding:
      prefix: --model_device

outputs:

  stdout:
    type: File
    outputBinding:
      glob: stdout

stdout: stdout


$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl

