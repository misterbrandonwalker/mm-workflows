#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Grab subset of PDBBind database

doc: |-
  Grab subset of PDBBind database

baseCommand: ["python", "/pdbbind_subset.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/pdbbind_subset

requirements:
  InlineJavascriptRequirement: {}

inputs:

  pdb_ids:
    type: File
    inputBinding:
      position: 1
      separate: false
      prefix: --pdb_ids=

  max_output:
    type: int
    inputBinding:
      position: 2
      separate: false
      prefix: --max_output=

  output_pdb_files:
    type: string?

  output_ligand_files:
    type: string?


outputs:

  output_pdb_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*.pdb"
    format: edam:format_1476

  output_ligand_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*.sdf"
    format: edam:format_3814

  stdout:
    type: File
    outputBinding:
      glob: stdout


stdout: stdout


$namespaces:
  edam: https://edamontology.org/
  cwltool: http://commonwl.org/cwltool#

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl