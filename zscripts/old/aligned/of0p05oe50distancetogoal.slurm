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
#SBATCH --time=02:00:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda
source activate myenv

module load openmpi/4.1.1/gcc

mpirun -np 40 python main.py distancetogoal -of 0.05 -oe 50 -k 3.5 -p 2000 -t 20000 -f of0p05oe50distancetogoal.json
