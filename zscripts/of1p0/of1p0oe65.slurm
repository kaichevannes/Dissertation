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
mpirun -np 30 python main.py distancetogoal -of 1.0 -oe 65 -sp 65 -p 300 -t 1000 -f of1p0oe0to100.json
