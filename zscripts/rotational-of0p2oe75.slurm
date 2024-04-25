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
#SBATCH --time=03:00:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda
source activate myenv

module load openmpi/4.1.1/gcc

mpirun -np 20 python main.py visceks -aps lanchesters rotation -st 1 -of 0.2 -oe 75 -p 500 -t 20000 -f rotational-of0p2oe75.json
