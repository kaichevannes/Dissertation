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
#SBATCH --time=06:00:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda
module load openmpi/5.0.0

source activate myenv

mpirun -np 4 python3 main.py distancetogoal -of 0.3 -oe 1 -sp 1 -p 0 -t 20 -f overridefraction0p3overrideentities0to100.json
