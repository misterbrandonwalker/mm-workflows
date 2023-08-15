
#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

label: This class implements extracting zipped array of files

doc: |-
  This class implements extracting zipped array of files

baseCommand: "true"
requirements:
  - class: InlineJavascriptRequirement

inputs:

  zipped_array:
    type:
      type: array
      items: File

  first_file:
    type: string?

  second_file:
    type: string?

outputs:

  first_file:
    label: output first file from zipped array
    doc: output first file from zipped array
    type: File
    outputBinding:
      outputEval: ${return inputs.zipped_array[0];}

  second_file:
    label: output second file from zipped array
    doc: output second file from zipped array
    type: File

    outputBinding:
      outputEval: ${return inputs.zipped_array[1];}

stdout: stdout

$namespaces:
  edam: https://edamontology.org/