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
#SBATCH --time=00:40:00   # walltime

cd /lyceum/kc2g21/Dissertation

module load conda
source activate myenv

module load openmpi/4.1.1/gcc

mpirun -np 40 python main.py lanchesters -of 0.9 -oe 10 -p 500 -t 2000 -f of0p9oe10lanchesters.json
