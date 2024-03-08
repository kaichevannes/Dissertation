#!/bin/bash
#SBATCH --ntasks=40
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --time=00:40:00
cd /lyceum/kc2g21/Dissertation
module load conda
source activate myenv
module load openmpi/4.1.1/gcc
mpirun -np 40 python main.py distancetogoal -of 0.3 -oe 88 -sp 88 -p 500 -t 2500 -f of0p3oe0to100.json
