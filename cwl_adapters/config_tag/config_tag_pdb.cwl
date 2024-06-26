#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0

label: Returns a dictionary of the given arguments as a JSON-encoded string.
doc: |-
  Returns a dictionary of the given arguments as a JSON-encoded string.

baseCommand: echo # Anything, unused

requirements:
  InlineJavascriptRequirement: {}

inputs:
  pdb_id:
    type: string
    format:
    - edam:format_2330
  # Note: Even though the "filter" argument has a boolean type, it cannot accept the value True.
  # https://biobb-io.readthedocs.io/en/latest/api.html#module-api.pdb
  filter:
    type: ["null", boolean, {"type": "array", "items": "string"}]

outputs:
  output_config_string:
    label: A dictionary of the given arguments as a JSON-encoded string.
    doc: |-
      A dictionary of the given arguments as a JSON-encoded string.
    type: string
    #format: edam:format_2330 # "'str' object does not support item assignment""
    outputBinding:
      outputEval: |
        ${
          var config = {};
          config["pdb_code"] = inputs.pdb_id;
          if (inputs.filter == true) {
            throw new Error("Error! filter doesn't accept True value");
          }
          else {
          config["filter"] = inputs.filter;
          }
          return JSON.stringify(config);
        }

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
