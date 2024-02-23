from order_parameter.order_parameter import OrderParameter
from simulation.options.boid_simulation_options import BoidSimulationOptions
from simulation.manager.simulation_manager import SimulationManager
from simulation.boid_simulation import BoidSimulation
from multiprocessing.pool import ThreadPool
import json


class BoidSimulationManager(SimulationManager):
    """The manager class for a boid simulation, if no constructor is given, default values are taken from Maruyama et al."""

    def __init__(
        self,
        order_parameter: OrderParameter = None,
        simulation_options: BoidSimulationOptions = BoidSimulationOptions(),
        num_runs: int = 10,
    ):
        """
        Args:
            order_parameter (OrderParameter, optional): the order parameter that is used to evaluate the swarm. Defaults to None.
            simulation_options (BoidSimulationOptions, optional): the options for the simulation. Defaults to BoidSimulationOptions().
        """
        super().__init__(order_parameter, simulation_options, num_runs)

        # Maybe set a simulation per order parameter in the order parameter manager?
        # This is a very wasteful approach

    def run_all(self):
        # Instantiate simulations
        threadpool = ThreadPool(processes=self.num_runs)
        simulation_threads = []
        for _ in range(self.num_runs):
            simulation = BoidSimulation(self.simulation_options, self.order_parameter)
            simulation_threads.append(threadpool.apply_async(simulation.run))

        for async_result in simulation_threads:
            self.simulation_results.append(async_result.get())

    def save_to_file(self, filename):
        simulation_dict = {}
        for i in range(len(self.simulation_results)):
            simulation_dict[i] = self.simulation_results[i].get_results()

        print(simulation_dict)

        with open(f"./data/{filename}", "w") as outfile:
            outfile.write(json.dumps(simulation_dict))
