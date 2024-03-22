import os
import numpy as np

of_initial_values = [500] + list(np.linspace(5000, 13000, 10, dtype=int))
of_end_values = (
    [500]
    + list(np.linspace(13000, 500, 5, dtype=int))
    + list(np.linspace(500, 500, 5, dtype=int))
)
ofs = []

for i in range(len(of_initial_values)):
    if i <= 5:
        of = [500] + list(
            np.linspace(of_initial_values[i], of_end_values[i], 100, dtype=int)
        )
    else:
        of = (
            [500]
            + list(np.linspace(of_initial_values[i], of_end_values[i], 50, dtype=int))
            + list(np.linspace(500, 500, 50, dtype=int))
        )
    ofs.append(of)

for i in range(10):
    for j in range(101):
        if not os.path.isdir(f"of0p{i}"):
            os.mkdir(f"of0p{i}")
        with open(f"./of0p{i}/of0p{i}oe{j}.slurm", "w") as outfile:
            outfile.write("#!/bin/bash\n")
            outfile.write("#SBATCH --ntasks=40\n")
            outfile.write("#SBATCH --nodes=1\n")
            outfile.write("#SBATCH --ntasks-per-node=40\n")
            outfile.write("#SBATCH --cpus-per-task=1\n")
            outfile.write("#SBATCH --time=03:00:00\n")
            outfile.write("cd /lyceum/kc2g21/Dissertation\n")
            outfile.write("module load conda\n")
            outfile.write("source activate myenv\n")
            outfile.write("module load openmpi/4.1.1/gcc\n")
            outfile.write(
                f"mpirun -np 40 python main.py distancetogoal -of 0.{i} -oe {j} -sp {j} -p 300 -t {ofs[i][j]} -f of0p{i}oe0to100.json\n"
            )

for j in range(101):
    if not os.path.isdir("of1p0"):
        os.mkdir("of1p0")
    with open(f"./of1p0/of1p0oe{j}.slurm", "w") as outfile:
        outfile.write("#!/bin/bash\n")
        outfile.write("#SBATCH --ntasks=40\n")
        outfile.write("#SBATCH --nodes=1\n")
        outfile.write("#SBATCH --ntasks-per-node=40\n")
        outfile.write("#SBATCH --cpus-per-task=1\n")
        outfile.write("#SBATCH --time=03:00:00\n")
        outfile.write("cd /lyceum/kc2g21/Dissertation\n")
        outfile.write("module load conda\n")
        outfile.write("source activate myenv\n")
        outfile.write("module load openmpi/4.1.1/gcc\n")
        outfile.write(
            f"mpirun -np 40 python main.py distancetogoal -of 1.0 -oe {j} -sp {j} -p 300 -t {ofs[10][j]} -f of1p0oe0to100.json\n"
        )
