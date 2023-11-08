from swarm.swarm import Swarm
from entity_factory.boid_factory import BoidFactory
import time
from matplotlib import animation
import matplotlib.pyplot as plt

NEIGHBOUR_RADIUS = 100
SWARM_SIZE = 50
GRID_SIZE = 200


def main():
    boid_factory = BoidFactory(grid_size=GRID_SIZE, neighbour_radius=NEIGHBOUR_RADIUS)
    swarm = Swarm(SWARM_SIZE, boid_factory)
    swarm.generate_entities()

    fig, ax = plt.subplots()
    swarm.initialise_plot(ax)
    plt.xlim(0, GRID_SIZE)
    plt.ylim(0, GRID_SIZE)

    ani = animation.FuncAnimation(fig, swarm.plot, frames=2, interval=100, repeat=True)
    plt.show()


if __name__ == "__main__":
    main()
