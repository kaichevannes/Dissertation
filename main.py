from swarm.swarm import Swarm
from entity_factory.boid_factory import BoidFactory
import time
from matplotlib import animation
import matplotlib.pyplot as plt
import argparse

# location dispersion


# WEIGHTING_TYPE = "AVOIDANCE"
GRID_SIZE = 100
WEIGHTING_TYPE = "ZHANG"
COLLISION_AVOIDANCE_RADIUS = GRID_SIZE * 0.01
VELOCITY_MATCHING_RADIUS = GRID_SIZE * 0.05
FLOCK_CENTERING_RADIUS = GRID_SIZE * 0.05
COLLISION_AVOIDANCE_RADIUS = 20
VELOCITY_MATCHING_RADIUS = 30
FLOCK_CENTERING_RADIUS = 40

# (400,1,10) / (1,30,4)
if WEIGHTING_TYPE == "ZHANG":  # From Zhang et al.
    COLLISION_AVOIDANCE_WEIGHTING = 400
    VELOCITY_MATCHING_WEIGHTING = 1
    FLOCK_CENTERING_WEIGHTING = 10
elif WEIGHTING_TYPE == "MARUYAMA":  # From Maruyama et al.
    COLLISION_AVOIDANCE_WEIGHTING = 0.002
    VELOCITY_MATCHING_WEIGHTING = 0.06
    FLOCK_CENTERING_WEIGHTING = 0.008

COLLISION_AVOIDANCE_WEIGHTING = 0
VELOCITY_MATCHING_WEIGHTING = 1
FLOCK_CENTERING_WEIGHTING = 0

NOISE_FRACTION = 1
SWARM_SIZE = 30
VISUALISATION_NORMAL = 60
VISUALISATION_REAL_TIME = 0


def main(args):
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

    if args.visualise:
        fig, ax = plt.subplots()
        swarm.initialise_plot(ax)
        plt.xlim(0, GRID_SIZE)
        plt.ylim(0, GRID_SIZE)

        ani = animation.FuncAnimation(
            fig, swarm.plot, frames=2, interval=VISUALISATION_NORMAL, repeat=True
        )
        plt.show()
    else:
        for t in range(100):
            swarm.step()
            print(swarm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration",
        description="Simulates a swarm",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    main(parser.parse_args())
