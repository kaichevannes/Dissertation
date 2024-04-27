#!/bin/bash
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=03:00:00
cd /lyceum/kc2g21/Dissertation
module load conda
source activate myenv
module load openmpi/4.1.1/gcc
mpirun -np 10 python main.py distancetogoal -st 3 -aps visceks lanchesters rotation groups -k 3.5 -of 0.85 -oe 62 -sp 62 -p 700 -t 958 -f of0p85oe0to100.json
