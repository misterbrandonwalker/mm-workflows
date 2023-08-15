#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: DiffDock Diffusion based protein ligand docking

doc: |-
  DiffDock Diffusion based protein ligand docking

baseCommand: ["python", "/gen_diffdock_inputs.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/create_diffdock_inputs

requirements:
  InlineJavascriptRequirement: {}


inputs:

  protein_path:
    type: File
    inputBinding:
      position: 1
      separate: false
      prefix: --protein_path=

  ligand_path:
    type: File
    inputBinding:
      position: 2
      separate: false
      prefix: --ligand_path=

  output_name:
    type: string?
    inputBinding:
      position: 3
      separate: false
      prefix: --output_name=
    default: protein_ligand.csv

  output:
    type: string?
    default: ""

  protein_path_out:
    type: string?
    default: ""

  ligand_path_out:
    type: string?
    default: ""

outputs:

  output:
    type: File?
    outputBinding:
      glob: $(inputs.output_name)

  protein_path_out:
    type: File?
    outputBinding:
      outputEval: ${return inputs.protein_path}

  ligand_path_out:
    type: File?
    outputBinding:
      outputEval: ${return inputs.ligand_path}

  output_name:
    type: File
    outputBinding:
      glob: $(inputs.output_name)

  stdout:
    type: File
    outputBinding:
      glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl