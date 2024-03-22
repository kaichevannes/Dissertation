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
mpirun -np 40 python main.py distancetogoal -of 0.1 -oe 27 -sp 27 -p 300 -t 7101 -f of0p1oe0to100.json
