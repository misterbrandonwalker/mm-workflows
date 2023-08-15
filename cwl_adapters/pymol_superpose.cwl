#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Super pose crystal pose and predicted poses and save in pymol session

doc: |-
  Super pose crystal pose and predicted poses and save in pymol session

baseCommand: ["python", "/pymol_superpose.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/pymol_docking_poses

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing: |
      ${
        const lst = [];
        for (var i = 0; i < inputs.predicted_poses.length; i++) {
          lst.push(inputs.predicted_poses[i]);
        }
        lst.push(inputs.crystal_pose_path);
        lst.push(inputs.pdb_path);
        return lst;
      }

inputs:

  predicted_poses:
    type:
      type: array
      items: File
    inputBinding:
      itemSeparator: ","
      separate: false
      prefix: --predicted_poses=

  pdb_path:
    type: File
    default: ""
    inputBinding:
      separate: false
      prefix: --pdb_path=

  crystal_pose_path:
    type: File
    default: ""
    inputBinding:
      separate: false
      prefix: --crystal_pose_path=

  output_pymol_session:
    type: string?

outputs:

  output_pymol_session:
    type: File?
    outputBinding:
      glob: "*.pse"

  stdout:
    type: File
    outputBinding:
      glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl