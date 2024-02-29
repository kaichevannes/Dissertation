#!/bin/bash

####################################
#  Iridis 5 slurm script template
#
#  Submit script: sbatch filename
#
####################################
#SBATCH --ntasks=40     # Number of processor cores (i.e. tasks)
#SBATCH --nodes=1     # Number of nodes requested
#SBATCH --ntasks-per-node=40     # Tasks per node
#SBATCH --cpus-per-task=1     # Threads per task
#SBATCH --time=12:00:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda

source activate myenv

python3 main.py distancetogoal -n 10 -of 0.3 -oe 1 -sp 1 -f overridefraction0p3overrideentities0to100.json