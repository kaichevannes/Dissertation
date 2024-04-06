import os
import numpy as np

noise = np.linspace(0, 1, 101)
for nf in noise:
    if not os.path.isdir("noise"):
        os.mkdir("noise")
    normal_version = "%.2f" % nf
    with open(f"./noise/nf{normal_version.replace('.','p')}.slurm", "w") as outfile:
        outfile.write("#!/bin/bash\n")
        outfile.write("#SBATCH --ntasks=10\n")
        outfile.write("#SBATCH --nodes=1\n")
        outfile.write("#SBATCH --ntasks-per-node=10\n")
        outfile.write("#SBATCH --cpus-per-task=1\n")
        outfile.write("#SBATCH --time=01:00:00\n")
        outfile.write("cd /lyceum/kc2g21/Dissertation\n")
        outfile.write("module load conda\n")
        outfile.write("source activate myenv\n")
        outfile.write("module load openmpi/4.1.1/gcc\n")
        outfile.write(
            f"mpirun -np 10 python main.py distancetogoal -k 3.5 -nf {normal_version} -sp {normal_version} -p 0 -t 5000 -f noise.json\n"
        )
