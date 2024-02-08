from swarm.swarm import Swarm
import numpy as np


class Simulation:
    """Represent a base simulation class, this will be used to run simulations on any entity."""

    def __init__(
        self,
        swarm_size: int,
        swarm_density: float,
        visualise: bool,
    ):
        """Simulation constructor.

        Args:
            swarm_size (int): the number of entities in a swarm.
            swarm_density (float): the number of entities per unit area.
            visualise (bool): whether or not to visualise this simulation.
        """
        self.swarm_size = swarm_size
        self.swarm_density = swarm_density
        self.visualise = visualise
        self.grid_size = np.sqrt(self.swarm_size / self.swarm_density) - 1

    def initialise_swarm(self) -> Swarm:
        pass
