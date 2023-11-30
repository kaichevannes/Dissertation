from swarm.swarm import Swarm
from entity_factory.boid_factory import BoidFactory
import time
from matplotlib import animation
import matplotlib.pyplot as plt
import argparse
import numpy as np

"""Visualisation settings"""
VISUALISATION_NORMAL = 60
VISUALISATION_REAL_TIME = 0

"""Noise percentage"""
NOISE_FRACTION = 0.103
# NOISE_FRACTION = 0

"""Swarm size and density"""
SWARM_SIZE = 100
# Swarm density is measured in entities / area (grid_size^2)
# A swarm density of 1 means 1 boid per grid unit, meaning a density of 1 with a swarm size of 100 will produce a grid of size 10x10
SWARM_DENSITY = 0.6
GRID_SIZE = np.sqrt(SWARM_SIZE / SWARM_DENSITY) - 1

"""Parameter tuning"""
RADIUS_MODEL = "EXTENDED_MARUYAMA"

match RADIUS_MODEL:
    case "MARUYAMA":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE * 0.01
        VELOCITY_MATCHING_RADIUS = GRID_SIZE * 0.05
        FLOCK_CENTERING_RADIUS = GRID_SIZE * 0.05
    case "FULL":
        COLLISION_AVOIDANCE_RADIUS = GRID_SIZE
        VELOCITY_MATCHING_RADIUS = GRID_SIZE
        FLOCK_CENTERING_RADIUS = GRID_SIZE
    case "EXTENDED_MARUYAMA":
        EXTENDED_MULTIPLIER = 3.5
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
        COLLISION_AVOIDANCE_WEIGHTING = 0.002
        VELOCITY_MATCHING_WEIGHTING = 0.06
        FLOCK_CENTERING_WEIGHTING = 0.008
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

RANDOM_SEED = 123456789


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
        swarm = Swarm(SWARM_SIZE, boid_factory, RANDOM_SEED)
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
            fig, swarm.update_plot, frames=1000, interval=interval, repeat=False
        )
        plt.show()
    else:
        order_params = []
        for value in [
            1,
            0.95,
            0.9,
            0.85,
            0.8,
            0.75,
            0.7,
            0.65,
            0.6,
            0.55,
            0.5,
            0.45,
            0.4,
            0.35,
            0.3,
            0.25,
            0.2,
            0.15,
            0.1,
            0.05,
            0,
        ]:
            boid_factory = BoidFactory(
                grid_size=GRID_SIZE,
                random_seed=RANDOM_SEED,
                collision_avoidance_radius=COLLISION_AVOIDANCE_RADIUS,
                velocity_matching_radius=VELOCITY_MATCHING_RADIUS,
                flock_centering_radius=FLOCK_CENTERING_RADIUS,
                collision_avoidance_weighting=COLLISION_AVOIDANCE_WEIGHTING,
                velocity_matching_weighting=VELOCITY_MATCHING_WEIGHTING,
                flock_centering_weighting=FLOCK_CENTERING_WEIGHTING,
                noise_fraction=value,
            )
            swarm = Swarm(SWARM_SIZE, boid_factory)
            swarm.generate_entities()

            total_order_parameter = 0
            for t in range(500):
                swarm.step()
                print(swarm)
            for t in range(500):
                swarm.step()
                print(swarm)
                total_order_parameter += swarm.calculate_visceks_order_parameter()
            print(total_order_parameter / 500)
            order_params.append(total_order_parameter / 500)
        print(order_params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration",
        description="Simulates a swarm",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    main(parser.parse_args())
