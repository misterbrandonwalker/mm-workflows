#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: DiffDock Diffusion based protein ligand docking

doc: |-
  DiffDock Diffusion based protein ligand docking

baseCommand: ["bash", "diffdock_cmds.sh"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/diffdock_cpu

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing: |
      ${
        const lst = [];
        for (var i = 0; i < ; i++) {
          lst.push(inputs.cached_files.length);
        }
        lst.push();
        lst.push();
        lst.push(inputs.protein_path);
        return lst;
      }

inputs:

  script_path:
    type: File

  cached_files:
    type: 
      type: array
      items: [File, Directory]

  protein_path:
    type: File

  ligand_path:
    type: File

  protein_ligand_inputs:
    type: File
    inputBinding:
      separate: true
      prefix: --protein_ligand_csv

  inference_steps:
    type: int?
    inputBinding:
      separate: true
      prefix: --inference_steps
    default: 20

  samples_per_complex:
    type: int?
    inputBinding:
      separate: true
      prefix: --samples_per_complex
    default: 40

  batch_size:
    type: int?
    inputBinding:
      separate: true
      prefix: --batch_size
    default: 10

  actual_steps:
    type: int?
    inputBinding:
      separate: true
      prefix: --actual_steps
    default: 18

  out_dir:
    type: string?
    inputBinding:
      separate: true
      prefix: --out_dir
    default: results/

  model_dir:
    type: string?
    inputBinding:
      separate: true
      prefix: --model_dir
    default:  /DiffDock/workdir/paper_score_model/ 

  confidence_model_dir:
    type: string?
    inputBinding:
      separate: true
      prefix: --confidence_model_dir
    default:  /DiffDock/workdir/paper_confidence_model

  no_final_step_noise:
    type: boolean?
    inputBinding:
      prefix: --no_final_step_noise
    default: true

  save_visualisation:
    type: boolean?
    inputBinding:
      prefix: --save_visualisation
    default: true

  output_files:
    type: string?
    default: ""

  execution_time:
    type: string?

outputs:

  output_files:
    type: Directory?
    outputBinding:
      glob: $(inputs.out_dir)

  stdout:
    type: File
    outputBinding:
      glob: stdout

  stderr:
    type: File
    outputBinding:
      glob: stderr

  execution_time:
    label: Time to run DiffDock
    doc: |-
      Time to run DiffDock
    type: float
    outputBinding:
      glob: stderr
      loadContents: true
      outputEval: |
        ${
          const lines = self[0].contents.split("\n");
          for (var i = 0; i < lines.length; i++) {
            const indices = lines[i].split(" ");
            if (indices.length == 1) {
              if (indices[0] != '') {
                  const datum = parseFloat(indices[0]);
                  return datum;
              }
            }
          }
        }


stdout: stdout

stderr: stderr

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl