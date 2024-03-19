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
mpirun -np 30 python main.py distancetogoal -of 0.1 -oe 59 -sp 59 -p 300 -t 2500 -f of0p1oe0to100.json
