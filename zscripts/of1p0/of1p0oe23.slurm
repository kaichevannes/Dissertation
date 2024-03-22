#!/bin/bash
#SBATCH --ntasks=40
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --time=03:00:00
cd /lyceum/kc2g21/Dissertation
module load conda
source activate myenv
module load openmpi/4.1.1/gcc
mpirun -np 40 python main.py distancetogoal -of 1.0 -oe 23 -sp 23 -p 300 -t 7387 -f of1p0oe0to100.json
