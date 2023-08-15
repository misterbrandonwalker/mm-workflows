#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Copy cache file from container

# cp -r doesnt work but rsync -r does
baseCommand: rsync
arguments: ["-r", $(inputs.cache_path), $(runtime.outdir)]

requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: mrbrandonwalker/diffdock_cpu

inputs:

  cache_path:
    type: string?
    default: "/DiffDock/"

  cache:
    type: string?
 
outputs:

  cache:
    type: 
      type: array
      items: [File, Directory]
    outputBinding:
      glob: ".*npy"

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl