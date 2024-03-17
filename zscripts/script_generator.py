import os

for i in range(10):
    for j in range(101):
        if not os.path.isdir(f"of0p{i}"):
            os.mkdir(f"of0p{i}")
        with open(f"./of0p{i}/of0p{i}oe{j}.slurm", "w") as outfile:
            outfile.write("#!/bin/bash\n")
            outfile.write("#SBATCH --ntasks=10\n")
            outfile.write("#SBATCH --nodes=1\n")
            outfile.write("#SBATCH --ntasks-per-node=10\n")
            outfile.write("#SBATCH --cpus-per-task=1\n")
            outfile.write("#SBATCH --time=00:30:00\n")
            outfile.write("cd /lyceum/kc2g21/Dissertation\n")
            outfile.write("module load conda\n")
            outfile.write("source activate myenv\n")
            outfile.write("module load openmpi/4.1.1/gcc\n")
            outfile.write(
                f"mpirun -np 10 python main.py distancetogoal -of 0.{i} -oe {j} -sp {j} -p 300 -t {3000/(i+1)} -f of0p{i}oe0to100.json\n"
            )

for j in range(101):
    if not os.path.isdir("of1p0"):
        os.mkdir("of1p0")
    with open(f"./of1p0/of1p0oe{j}.slurm", "w") as outfile:
        outfile.write("#!/bin/bash\n")
        outfile.write("#SBATCH --ntasks=10\n")
        outfile.write("#SBATCH --nodes=1\n")
        outfile.write("#SBATCH --ntasks-per-node=10\n")
        outfile.write("#SBATCH --cpus-per-task=1\n")
        outfile.write("#SBATCH --time=00:30:00\n")
        outfile.write("cd /lyceum/kc2g21/Dissertation\n")
        outfile.write("module load conda\n")
        outfile.write("source activate myenv\n")
        outfile.write("module load openmpi/4.1.1/gcc\n")
        outfile.write(
            f"mpirun -np 10 python main.py distancetogoal -of 1.0 -oe {j} -sp {j} -p 300 -t 300 -f of1p0oe0to100.json\n"
        )
