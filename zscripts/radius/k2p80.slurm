#!/bin/bash
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
cd /lyceum/kc2g21/Dissertation
module load conda
source activate myenv
module load openmpi/4.1.1/gcc
mpirun -np 10 python main.py visceks -oe 0 -of 0 -k 2.80 -sp 2.80 -aps rotation lanchesters groups -p 0 -t 5000 -f radius.json
