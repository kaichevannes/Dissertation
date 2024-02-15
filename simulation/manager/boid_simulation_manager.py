from order_parameter.manager.order_parameter_manager import OrderParameterManager
from simulation.options.boid_simulation_options import BoidSimulationOptions
from simulation.manager.simulation_manager import SimulationManager


class BoidSimulationManager(SimulationManager):
    """The manager class for a boid simulation, if no constructor is given, default values are taken from Maruyama et al."""

    def __init__(
        self,
        order_parameter_manager: OrderParameterManager = None,
        simulation_options: BoidSimulationOptions = BoidSimulationOptions(),
    ):
        """
        Args:
            order_parameter_manager (OrderParameterManager, optional): the order parameter manager that is used to evaluate the swarm. Defaults to None.
            simulation_options (BoidSimulationOptions, optional): the options for the simulation. Defaults to BoidSimulationOptions().
        """
        super().__init__(order_parameter_manager, simulation_options)

        # Maybe set a simulation per order parameter in the order parameter manager?
        # This is a very wasteful approach

    def run_all(self):
        pass
