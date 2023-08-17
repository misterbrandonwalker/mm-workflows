
#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Outputs DiffDock parameters

doc: |-
  This class outputs DiffDock parameters

baseCommand: ["python", "/output_diffdock_parameters.py"]
hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/save_diffdock_parameters

requirements:
  ScatterFeatureRequirement: {}

inputs:

  execution_time:
    type: float?
    inputBinding:
      position: 1
      separate: false
      prefix: --execution_time=

  rmsd:
    type: File?
    inputBinding:
      position: 2
      separate: false
      prefix: --rmsd=

  output_json_name:
    type: string
    default: "output.json"
    inputBinding:
      position: 3
      separate: false
      prefix: --output_json_name=

  protein_path:
    type: File
    inputBinding:
      position: 4
      separate: false
      prefix: --protein_path=

  ligand_path:
    type: File
    inputBinding:
      position: 5
      separate: false
      prefix: --ligand_path=

  inference_steps:
    type: int
    inputBinding:
      position: 6
      separate: false
      prefix: --inference_steps=

  samples_per_complex:
    type: int
    inputBinding:
      position: 7
      separate: false
      prefix: --samples_per_complex=

  batch_size:
    type: int
    inputBinding:
      position: 8
      separate: false
      prefix: --batch_size=

  actual_steps:
    type: int
    inputBinding:
      position: 9
      separate: false
      prefix: --actual_steps=

  no_final_step_noise:
    type: boolean
    inputBinding:
      position: 11
      prefix: --no_final_step_noise

  top_n_confident:
    type: float
    inputBinding:
      position: 10
      separate: false
      prefix: --top_n_confident=

  pymol_session:
    type: File
    inputBinding:
      position: 12
      separate: false
      prefix: --pymol_session=

  top_percent_confidence:
    type: float
    inputBinding:
      position: 13
      separate: false
      prefix: --top_percent_confidence=

  output_json:
    type: string?

outputs:

  output_json:
    type: File
    format: edam:format_3000
    outputBinding:
      glob: $(inputs.output_json_name)


stdout: stdout

$namespaces:
  edam: https://edamontology.org/