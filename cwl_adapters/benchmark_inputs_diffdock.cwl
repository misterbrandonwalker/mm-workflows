
#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: This class implements setting up benchmarking inputs for DiffDock

doc: |-
  This class implements setting up benchmarking inputs for DiffDock

baseCommand: echo
requirements:
  - class: InlineJavascriptRequirement

inputs:

  use_clustering_filter:
    type: boolean?

  use_clustering_filter_out:
    type: string?

  centroid_cutoff:
    type: float

  centroid_cutoff_out:
    type: string?

  protein_path_array:
    type:
      type: array
      items: File
    format:
      - edam:format_1476

  ligand_path_array:
    type:
      type: array
      items: File
    format:
      - edam:format_3814

  samples_per_complex_array:
    type:
      type: array
      items: int

  inference_steps_array:
    type:
      type: array
      items: int

  samples_per_complex:
    type: string?

  inference_steps:
    type: string?

  protein_path_out:
    type: string?

  ligand_path:
    type: string?

  batch_size:
    type: int?

  batch_size_out:
    type: string?

  actual_steps:
    type: int?

  actual_steps_out:
    type: string?

  no_final_step_noise:
    type: boolean?

  no_final_step_noise_out:
    type: string?

  top_n_confident:
    type: float?

  top_n_confident_out:
    type: string?

  top_percent_confidence:
    type: float?

  top_percent_confidence_out:
    type: string?

outputs:

  use_clustering_filter_out:
    label: use_clustering_filter
    doc: |-
      use_clustering_filter
    type: boolean

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.use_clustering_filter
        }

  centroid_cutoff_out:
    label: centroid_cutoff
    doc: |-
      centroid_cutoff
    type: float

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.centroid_cutoff
        }

  samples_per_complex:
    label: samples_per_complex
    doc: |-
      samples_per_complex
    type:
      type: array
      items: int

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.samples_per_complex_array
        }

  inference_steps:
    label: inference_steps
    doc: |-
      inference_steps
    type:
      type: array
      items: int

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.inference_steps_array
        }

  protein_path_out:
    label: protein_path
    doc: |-
      protein_path
    type:
      type: array
      items: File

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.protein_path_array
        }
    format: edam:format_1476

  ligand_path:
    label: ligand_path
    doc: |-
      ligand_path
    type:
      type: array
      items: File

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.ligand_path_array
        }
    format: edam:format_3814

  batch_size_out:
    label: batch_size
    doc: |-
      batch_size
    type: int

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.batch_size
        }

  actual_steps_out:
    label: actual_steps
    doc: |-
      actual_steps
    type: int

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.actual_steps
        }

  no_final_step_noise_out:
    label: no_final_step_noise
    doc: |-
      no_final_step_noise
    type: boolean

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.no_final_step_noise
        }

  top_n_confident_out:
    label: top_n_confident
    doc: |-
      top_n_confident
    type: float

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.top_n_confident
        }

  top_percent_confidence_out:
    label: top_percent_confidence
    doc: |-
      top_percent_confidence
    type: float

    outputBinding:
      glob: ""
      loadContents: true
      outputEval: |
        ${
          return inputs.top_percent_confidence
        }


stdout: stdout

$namespaces:
  edam: https://edamontology.org/