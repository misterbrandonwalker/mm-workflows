#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Modify filename

doc: |-
  Add scattered input parameters to filename to prevent filenames being the same in final output

baseCommand: ["python", "/modify_filenames.py"]


hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/modify_diffdock_filenames

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing: |
      ${
        const lst = [];
        for (var i = 0; i < inputs.file_names.length; i++) {
          var dict = {
            "entry": inputs.file_names[i],
            "writable": true // Important!
          };
          lst.push(dict);
        }
        return lst;
      }


inputs:

  file_names:
    type:
      type: array
      items: File
    inputBinding:
      position: 1
      itemSeparator: ","
      separate: false
      prefix: --file_names=

  inference_steps:
    type: int
    inputBinding:
      position: 2
      separate: false
      prefix: --inference_steps=

  samples_per_complex:
    type: int
    inputBinding:
      position: 3
      separate: false
      prefix: --samples_per_complex=

  output_files:
    type: string?

outputs:

  output_files:
    type: File[]
    outputBinding:
      glob: "*mod*"

  stdout:
   type: File
   outputBinding:
     glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl