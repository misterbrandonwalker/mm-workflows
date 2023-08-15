#!/bin/bash -e
# Unlike the default github action runners which spin up a brand new machine every time,
# self-hosted runners are not necessarily isolated. In particular, the docker cache
# needs to be manually updated by explicitly performing docker pull/build commands.
# NOTE: For now use the following explicit list. In the future, consider using the
# cwl-utils library to recursively search for the dockerPull: tags within each workflow.

cd ..

cd examples/data/
sudo docker build --no-cache --pull -f Dockerfile_data -t jakefennick/data .
cd ../..

cd examples/scripts/
sudo docker build --no-cache --pull -f Dockerfile_autodock_vina -t jakefennick/autodock_vina .
sudo docker build --no-cache --pull -f Dockerfile_scripts -t jakefennick/scripts .
sudo docker build --no-cache --pull -f Dockerfile_biosimspace -t jakefennick/biosimspace .
sudo docker build --no-cache --pull -f Dockerfile_PDBBind_refined -t pdbbind_refined_v2020 .  # NOTE: no username
cd ../..

cd examples/diffdock/
sudo docker build --no-cache --pull -f Dockerfile_sanitize_mol -t mrbrandonwalker/sanitize_mol .
sudo docker build --no-cache --pull -f Dockerfile_rmsd_poses -t mrbrandonwalker/rmsd_poses .
sudo docker build --no-cache --pull -f Dockerfile_pymol_docking_poses -t mrbrandonwalker/pymol_docking_poses .
sudo docker build --no-cache --pull -f Dockerfile_rank_diffdock_poses -t mrbrandonwalker/rank_diffdock_poses .
sudo docker build --no-cache --pull -f Dockerfile_create_diffdock_inputs -t mrbrandonwalker/create_diffdock_inputs .
sudo docker build --no-cache --pull -f Dockerfile_diffdock_cpu -t mrbrandonwalker/diffdock_cpu .
sudo docker build --no-cache --pull -f Dockerfile_diffdock_gpu -t mrbrandonwalker/diffdock_gpu .
cd ../..