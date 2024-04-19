import os
import numpy as np

# 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0
# This is top to bottom, how many runs on that column?
of_initial_values = (
    [500]
    + list(np.linspace(750, 750, 5, dtype=int))
    + list(np.linspace(750, 500, 5, dtype=int))
    + list(np.linspace(500, 500, 5, dtype=int))
    + list(np.linspace(500, 500, 5, dtype=int))
)
of_quarter_values = (
    [500]
    + list(np.linspace(750, 1500, 5, dtype=int))
    + list(np.linspace(1500, 5000, 5, dtype=int))
    + list(np.linspace(5000, 500, 5, dtype=int))
    + list(np.linspace(500, 2100, 5, dtype=int))
)
of_middle_values = (
    [500]
    + list(np.linspace(1500, 1500, 5, dtype=int))
    + list(np.linspace(1500, 1200, 5, dtype=int))
    + list(np.linspace(1200, 800, 5, dtype=int))
    + list(np.linspace(800, 5300, 5, dtype=int))
)
of_three_quarter_values = (
    [500]
    + list(np.linspace(1000, 5000, 5, dtype=int))
    + list(np.linspace(5000, 500, 5, dtype=int))
    + list(np.linspace(500, 2300, 5, dtype=int))
    + list(np.linspace(2300, 5300, 5, dtype=int))
)
of_end_values = (
    [500]
    + list(np.linspace(500, 500, 5, dtype=int))
    + list(np.linspace(500, 500, 5, dtype=int))
    + list(np.linspace(500, 1000, 5, dtype=int))
    + list(np.linspace(1000, 500, 5, dtype=int))
)
ofs = []

# This time change this to just have 21 values instead of all 100. This will literally make it run 5x faster, enabling finished runs in around 2 days.
# For the normal velocity/radius changes, just do that with a 11x11 grid. Obviously this is less clarity but it is a necessary sacrifice.
# Also change the number of pre time steps to be 500, this is because im now starting them all with a positive velocity.
for i in range(len(of_initial_values)):
    of = (
        [500]
        + list(np.linspace(of_initial_values[i], of_quarter_values[i], 25, dtype=int))
        + list(np.linspace(of_quarter_values[i], of_middle_values[i], 25, dtype=int))
        + list(
            np.linspace(of_middle_values[i], of_three_quarter_values[i], 25, dtype=int)
        )
        + list(np.linspace(of_three_quarter_values[i], of_end_values[i], 25, dtype=int))
    )
    ofs.append(of)

for i in range(10):
    # 0.1, 0.2, etc
    for j in range(101):
        if not (j == 0 or j == 1 or j == 99 or j % 5 == 0):
            continue
        if not os.path.isdir(f"of0p{i}"):
            os.mkdir(f"of0p{i}")
        with open(f"./of0p{i}/of0p{i}oe{j}.slurm", "w") as outfile:
            outfile.write("#!/bin/bash\n")
            outfile.write("#SBATCH --ntasks=10\n")
            outfile.write("#SBATCH --nodes=1\n")
            outfile.write("#SBATCH --ntasks-per-node=10\n")
            outfile.write("#SBATCH --cpus-per-task=1\n")
            outfile.write("#SBATCH --time=03:00:00\n")
            outfile.write("cd /lyceum/kc2g21/Dissertation\n")
            outfile.write("module load conda\n")
            outfile.write("source activate myenv\n")
            outfile.write("module load openmpi/4.1.1/gcc\n")
            outfile.write(
                f"mpirun -np 10 python main.py distancetogoal -aps visceks lanchesters rotation groups -k 3.5 -of 0.{i} -oe {j} -sp {j} -p 700 -t {ofs[2*i][j]} -f of0p{i}oe0to100.json\n"
            )

for i in range(10):
    # 0.05, 0.15, 0.25, etc
    new_i = i + 0.5
    formatted_new_i = f"{int(new_i * 10):02}"
    for j in range(101):
        if not (j == 0 or j == 1 or j == 99 or j % 5 == 0):
            continue
        if not os.path.isdir(f"of0p{formatted_new_i}"):
            os.mkdir(f"of0p{formatted_new_i}")
        with open(
            f"./of0p{formatted_new_i}/of0p{formatted_new_i}oe{j}.slurm", "w"
        ) as outfile:
            outfile.write("#!/bin/bash\n")
            outfile.write("#SBATCH --ntasks=10\n")
            outfile.write("#SBATCH --nodes=1\n")
            outfile.write("#SBATCH --ntasks-per-node=10\n")
            outfile.write("#SBATCH --cpus-per-task=1\n")
            outfile.write("#SBATCH --time=03:00:00\n")
            outfile.write("cd /lyceum/kc2g21/Dissertation\n")
            outfile.write("module load conda\n")
            outfile.write("source activate myenv\n")
            outfile.write("module load openmpi/4.1.1/gcc\n")
            outfile.write(
                f"mpirun -np 10 python main.py distancetogoal -aps visceks lanchesters rotation groups -k 3.5 -of 0.{formatted_new_i} -oe {j} -sp {j} -p 700 -t {ofs[(2 * i) + 1][j]} -f of0p{formatted_new_i}oe0to100.json\n"
            )

for j in range(101):
    if not (j == 0 or j == 1 or j == 99 or j % 5 == 0):
        continue
    if not os.path.isdir("of1p0"):
        os.mkdir("of1p0")
    with open(f"./of1p0/of1p0oe{j}.slurm", "w") as outfile:
        outfile.write("#!/bin/bash\n")
        outfile.write("#SBATCH --ntasks=10\n")
        outfile.write("#SBATCH --nodes=1\n")
        outfile.write("#SBATCH --ntasks-per-node=10\n")
        outfile.write("#SBATCH --cpus-per-task=1\n")
        outfile.write("#SBATCH --time=03:00:00\n")
        outfile.write("cd /lyceum/kc2g21/Dissertation\n")
        outfile.write("module load conda\n")
        outfile.write("source activate myenv\n")
        outfile.write("module load openmpi/4.1.1/gcc\n")
        outfile.write(
            f"mpirun -np 10 python main.py distancetogoal -aps visceks lanchesters rotation groups -k 3.5 -of 1.0 -oe {j} -sp {j} -p 700 -t {ofs[20][j]} -f of1p0oe0to100.json\n"
        )
