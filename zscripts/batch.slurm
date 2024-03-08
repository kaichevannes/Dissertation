#!/bin/bash

####################################
#  Iridis 5 slurm script template
#
#  Submit script: sbatch filename
#
####################################
#SBATCH --ntasks=4     # Number of processor cores (i.e. tasks)
#SBATCH --nodes=1     # Number of nodes requested
#SBATCH --ntasks-per-node=4     # Tasks per node
#SBATCH --cpus-per-task=1     # Threads per task
#SBATCH --time=00:40:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda
source activate myenv

module load openmpi/4.1.1/gcc

python -V

mpirun -np 4 python main.py distancetogoal -of 0.3 -oe 1 -sp 1 -p 0 -t 20 -f overridefraction0p3overrideentities0to100.json
