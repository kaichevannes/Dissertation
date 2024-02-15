from simulation.options.simulation_options import SimulationOptions
from order_parameter.order_parameter import OrderParameter
import numpy as np


class Simulation:
    """Represent a base simulation class, this will be used to run simulations on any entity.
    A simulation will be for a specific set of options and measure an order parameter.
    """

    def __init__(
        self,
        simulation_options: SimulationOptions,
        order_parameter: OrderParameter = None,
    ):
        """
        Args:
            simulation_options (SimulationOptions): the options for this simulation
            order_parameter (OrderParameter, optional): the order parameter to measure. Defaults to None
        """
        # TODO: Actually use this somehow???
        # self.swarm_size = simulation_options.swarm_size
        # self.swarm_density = simulation_options.swarm_density
        # self.visualiser = simulation_options.visualiser
        # self.grid_size = np.sqrt(self.swarm_size / self.swarm_density) - 1

    def run(self) -> None:
        """Run this simulation.

        Raises:
            NotImplementedError: if the run function is not implemented
        """
        raise NotImplementedError
