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
mpirun -np 40 python main.py distancetogoal -of 0.4 -oe 46 -sp 46 -p 300 -t 5829 -f of0p4oe0to100.json
