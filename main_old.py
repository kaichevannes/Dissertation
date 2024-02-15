from swarm.swarm import Swarm
from entity.factory.boid_factory import BoidFactory
import time
from matplotlib import animation
import matplotlib.pyplot as plt
import argparse
import numpy as np
import json

# plan: circling then splitting

"""Visualisation settings"""
VISUALISATION_NORMAL = 60
VISUALISATION_REAL_TIME = 0

"""Noise percentage"""
# NOISE_FRACTION = 1
NOISE_FRACTION = 0.05
# NOISE_FRACTION = 0

"""Swarm size and density"""
SWARM_SIZE = 100
# SWARM_SIZE = 50
# Swarm density is measured in entities / area (grid_size^2)
# A swarm density of 1 means 1 boid per grid unit, meaning a density of 1 with a swarm size of 100 will produce a grid of size 10x10
SWARM_DENSITY = 0.25
# SWARM_DENSITY = 0.6
GRID_SIZE = np.sqrt(SWARM_SIZE / SWARM_DENSITY) - 1

"""Parameter tuning"""
# RADIUS_MODEL = "MIN_MARUYAMA"
# RADIUS_MODEL = "MARUYAMA"
RADIUS_MODEL = "EXTENDED_MARUYAMA"
# RADIUS_MODEL = "DIRECTIONAL_MARUYAMA"
# RADIUS_MODEL = "CIRCULAR_MARUYAMA"
# RADIUS_MODEL = "MAXIMUM_MARUYAMA"

match RADIUS_MODEL:
    case "FULL":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE
        VELOCITY_MATCHING_RADIUS = GRID_SIZE
        FLOCK_CENTERING_RADIUS = GRID_SIZE
    case "MARUYAMA":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = GRID_SIZE * 0.05
    case "MIN_MARUYAMA":
        EXTENDED_MULTIPLIER = 0.5
        COLLISION_AVOIDANCE_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
    case "EXTENDED_MARUYAMA":
        EXTENDED_MULTIPLIER = 3.5
        COLLISION_AVOIDANCE_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
    case "DIRECTIONAL_MARUYAMA":
        EXTENDED_MULTIPLIER = 5
        COLLISION_AVOIDANCE_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
    case "CIRCULAR_MARUYAMA":
        EXTENDED_MULTIPLIER = 5.5
        COLLISION_AVOIDANCE_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
    case "MAXIMUM_MARUYAMA":
        EXTENDED_MULTIPLIER = 20
        COLLISION_AVOIDANCE_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = EXTENDED_MULTIPLIER * GRID_SIZE * 0.05
    case "EQUAL":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE * 0.25
        VELOCITY_MATCHING_RADIUS = GRID_SIZE * 0.25
        FLOCK_CENTERING_RADIUS = GRID_SIZE * 0.25
    case "STAGGERED":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE * 0.2
        VELOCITY_MATCHING_RADIUS = GRID_SIZE * 0.25
        FLOCK_CENTERING_RADIUS = GRID_SIZE * 0.3

# (400,1,10) / (1,30,4)
WEIGHTING_MODEL = "MARUYAMA"
# WEIGHTING_MODEL = "ZHANG"

match WEIGHTING_MODEL:
    case "ZHANG":  # From Zhang et al.
        COLLISION_AVOIDANCE_WEIGHTING = 400
        VELOCITY_MATCHING_WEIGHTING = 1
        FLOCK_CENTERING_WEIGHTING = 10
    case "MARUYAMA":  # From Maruyama et al.
        COLLISION_AVOIDANCE_WEIGHTING = 0.002  # 1/35
        VELOCITY_MATCHING_WEIGHTING = 0.06  # 30/35
        FLOCK_CENTERING_WEIGHTING = 0.008  # 4/35
    case "COLLISION_AVOIDANCE":
        COLLISION_AVOIDANCE_WEIGHTING = 1
        VELOCITY_MATCHING_WEIGHTING = 0
        FLOCK_CENTERING_WEIGHTING = 0
    case "VELOCITY_MATCHING":
        COLLISION_AVOIDANCE_WEIGHTING = 0
        VELOCITY_MATCHING_WEIGHTING = 1
        FLOCK_CENTERING_WEIGHTING = 0
    case "FLOCK_CENTERING":
        COLLISION_AVOIDANCE_WEIGHTING = 0
        VELOCITY_MATCHING_WEIGHTING = 0
        FLOCK_CENTERING_WEIGHTING = 1
    case "EQUAL":
        COLLISION_AVOIDANCE_WEIGHTING = 1
        VELOCITY_MATCHING_WEIGHTING = 1
        FLOCK_CENTERING_WEIGHTING = 1
    case _:
        raise ValueError("Invalid weighting model")

# RANDOM_SEED = 123456789


def main(args):
    if args.visualise:
        boid_factory = BoidFactory(
            grid_size=GRID_SIZE,
            collision_avoidance_radius=COLLISION_AVOIDANCE_RADIUS,
            velocity_matching_radius=VELOCITY_MATCHING_RADIUS,
            flock_centering_radius=FLOCK_CENTERING_RADIUS,
            collision_avoidance_weighting=COLLISION_AVOIDANCE_WEIGHTING,
            velocity_matching_weighting=VELOCITY_MATCHING_WEIGHTING,
            flock_centering_weighting=FLOCK_CENTERING_WEIGHTING,
            noise_fraction=NOISE_FRACTION,
        )
        swarm = Swarm(SWARM_SIZE, boid_factory)
        swarm.generate_entities()

        fig, ax = plt.subplots()
        swarm.initialise_plot(ax)
        plt.xlim(0, GRID_SIZE)
        plt.ylim(0, GRID_SIZE)

        if args.slow:
            interval = VISUALISATION_NORMAL
        else:
            interval = VISUALISATION_REAL_TIME
        _ = animation.FuncAnimation(
            fig, swarm.update_plot, frames=4000, interval=interval, repeat=False
        )
        plt.show()
    else:
        order_params = []
        # for value in [
        #     1,
        #     0.95,
        #     0.9,
        #     0.85,
        #     0.8,
        #     0.75,
        #     0.7,
        #     0.65,
        #     0.6,
        #     0.55,
        #     0.5,
        #     0.45,
        #     0.4,
        #     0.35,
        #     0.3,
        #     0.25,
        #     0.2,
        #     0.15,
        #     0.1,
        #     0.05,
        #     0
        #     # 0.14,
        #     # 0.13,
        #     # 0.12,
        #     # 0.11,
        #     # 0.109,
        #     # 0.108,
        #     # 0.107,
        #     # 0.106,
        #     # 0.105,
        #     # 0.104,
        #     # 0.103,
        #     # 0.102,
        #     # 0.101,
        #     # 0.1,
        # ]:
        # alignment_dict = {}
        # rotation_dict = {}
        # for value in [
        #     0,
        #     0.5,
        #     1,
        #     1.5,
        #     2,
        #     2.5,
        #     3,
        #     3.5,
        #     4,
        #     4.5,
        #     5,
        #     5.1,
        #     5.2,
        #     5.3,
        #     5.4,
        #     5.5,
        #     6,
        #     6.5,
        #     7,
        #     7.5,
        #     8,
        #     8.5,
        #     9,
        #     9.5,
        #     10,
        #     11,
        #     12,
        #     13,
        #     14,
        #     15,
        #     16,
        #     17,
        #     18,
        #     19,
        #     20,
        # ]:
        # alignment_runs = []
        # rotation_runs = []
        alignment_dict = {}
        rotation_dict = {}
        clustering_dict = {}
        groups_dict = {}
        for i in range(5):
            boid_factory = BoidFactory(
                grid_size=GRID_SIZE,
                collision_avoidance_radius=COLLISION_AVOIDANCE_RADIUS,
                velocity_matching_radius=VELOCITY_MATCHING_RADIUS,
                flock_centering_radius=FLOCK_CENTERING_RADIUS,
                collision_avoidance_weighting=COLLISION_AVOIDANCE_WEIGHTING,
                velocity_matching_weighting=VELOCITY_MATCHING_WEIGHTING,
                flock_centering_weighting=FLOCK_CENTERING_WEIGHTING,
                noise_fraction=NOISE_FRACTION,
            )
            swarm = Swarm(SWARM_SIZE, boid_factory)
            swarm.generate_entities()

            # print(swarm.calculate_visceks_order_parameter())
            # lanchesters_vs_time = [swarm.calculate_lanchesters_index()]
            # groups_vs_time = [swarm.calculate_number_of_groups()]
            # total_order_parameter = 0

            alignment = []
            rotation = []
            clustering = []
            groups = []

            # for t in range(130):
            #     swarm.step()
            #     # print(swarm)
            #     # print(swarm.calculate_lanchesters_index())
            #     # print(swarm.calculate_number_of_groups())
            #     # lanchesters_vs_time.append(swarm.calculate_lanchesters_index())
            #     # groups_vs_time.append(swarm.calculate_number_of_groups())
            # for t in range(130, 150):
            #     swarm.step()
            #     swarm.calculate_rotation_order_parameter(t - 130)
            # for t in range(150, 300):
            #     swarm.step()
            #     # print(swarm)
            #     #     total_order_parameter += swarm.calculate_visceks_order_parameter()
            #     # order_vs_time.append(swarm.calculate_visceks_order_parameter())
            #     alignment.append(swarm.calculate_visceks_order_parameter())
            #     rotation.append(swarm.calculate_rotation_order_parameter(t))
            for t in range(3000):
                swarm.step()
                alignment.append(swarm.calculate_visceks_order_parameter())
                rotation_param = swarm.calculate_rotation_order_parameter(t)
                if rotation_param is not None:
                    rotation.append(rotation_param)
                clustering.append(swarm.calculate_lanchesters_index())
                groups.append(swarm.calculate_number_of_groups())

            print(f"{i}")
            # print(f"alignment = {alignment}")
            # print(f"rotation = {rotation}")
            # alignment_runs.append(np.mean(np.array(alignment)))
            # rotation_runs.append(np.mean(np.array(rotation)))
            # lanchesters_dict[i] = lanchesters_vs_time
            # groups_dict[i] = groups_vs_time
            alignment_dict[i] = alignment
            rotation_dict[i] = rotation
            clustering_dict[i] = clustering
            groups_dict[i] = groups
        # print(f"alignment_runs = {alignment_runs}")
        # print(f"rotation_runs = {rotation_runs}")

        # alignment_dict[value] = np.mean(np.array(alignment_runs))
        # rotation_dict[value] = np.mean(np.array(rotation_runs))

        with open("./data/alignment_vs_time_low_density.json", "w") as outfile:
            outfile.write(json.dumps(alignment_dict))

        with open("./data/rotation_vs_time_low_density.json", "w") as outfile:
            outfile.write(json.dumps(rotation_dict))

        with open("./data/clustering_vs_time_low_density.json", "w") as outfile:
            outfile.write(json.dumps(clustering_dict))

        with open("./data/groups_vs_time_low_density.json", "w") as outfile:
            outfile.write(json.dumps(groups_dict))

        # print(total_order_parameter / 500)
        #     order_params.append(total_order_parameter / 500)
        # print(order_params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration",
        description="Simulates a swarm",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    main(parser.parse_args())
