#!/bin/bash
#SBATCH --ntasks=30
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=30
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
cd /lyceum/kc2g21/Dissertation
module load conda
source activate myenv
module load openmpi/4.1.1/gcc
mpirun -np 30 python main.py distancetogoal -of 0.3 -oe 70 -sp 70 -p 300 -t 1500 -f of0p3oe0to100.json
