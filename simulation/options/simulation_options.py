from visualiser.visualiser import Visualiser
from swarm.adjuster.swarm_adjuster import SwarmAdjuster
import numpy as np


class SimulationOptions:
    """The simulation options class will allow you to provide custom options to
    the simulation manager."""

    def __init__(
        self,
        swarm_size: int,
        swarm_density: float,
        visualiser: Visualiser,
        max_time_step: int,
        pre_simulation_steps: int,
        swarm_adjuster: SwarmAdjuster,
    ):
        """
        Args:
            swarm_size (int): the number of entities in a swarm
            swarm_density (float): the number of entities per unit squared
            visualiser (Visualiser): the visualiser class which is used to visualiser this simulation
            max_time_step (int): the maximum time step for this simulation
            pre_simulation_steps (int): the number of time steps to perform before recoding results
            swarm_adjuster (SwarmAdjuster): the swarm adjuster to manually override members of the swarm at a certain time frame
        """
        self.swarm_size = swarm_size
        self.swarm_density = swarm_density
        self.grid_size = np.sqrt(self.swarm_size / self.swarm_density) - 1
        self.visualiser = visualiser
        self.max_time_step = max_time_step
        self.pre_simulation_steps = pre_simulation_steps
        self.swarm_adjuster = swarm_adjuster
