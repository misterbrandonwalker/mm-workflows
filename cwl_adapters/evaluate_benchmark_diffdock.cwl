
#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Evaluate DiffDock benchmarks

doc: |-
  Evaluate DiffDock benchmarks

baseCommand: ["python", "/diffdock_benchmark.py"]
hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/evaluate_diffdock_results

requirements:
  InlineJavascriptRequirement: {}

inputs:

  input_json_files:
    type:
      type: array
      items: File
    inputBinding:
      position: 1
      separate: true

outputs:

  output_plots:
    label: Benchmark plots
    type: File[]
    outputBinding:
      glob: ./*.png

  output_csv:
    label: Benchmark csv files
    type: File[]
    outputBinding:
      glob: ./*.csv

  stdout:
    type: File
    outputBinding:
      glob: stdout


stdout: stdout

$namespaces:
  edam: https://edamontology.org/