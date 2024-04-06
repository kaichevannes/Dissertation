# from order_parameter.order_parameter import OrderParameter
from order_parameter.manager.order_parameter_manager import OrderParameterManager
from simulation.options.boid_simulation_options import BoidSimulationOptions
from simulation.manager.simulation_manager import SimulationManager
from simulation.boid_simulation import BoidSimulation
from simulation.simulation_result import SimulationResult
from simulation.manager.simulation_saver import SimulationSaver
from mpi4py import MPI
import sys


class BoidSimulationManager(SimulationManager):
    """The manager class for a boid simulation, if no constructor is given, default values are taken from Maruyama et al."""

    def __init__(
        self,
        order_parameter_manager: OrderParameterManager = None,
        simulation_options: BoidSimulationOptions = BoidSimulationOptions(),
        num_runs: int = 10,
    ):
        """
        Args:
            order_parameter (OrderParameter, optional): the order parameter that is used to evaluate the swarm. Defaults to None.
            simulation_options (BoidSimulationOptions, optional): the options for the simulation. Defaults to BoidSimulationOptions().
        """
        super().__init__(order_parameter_manager, simulation_options, num_runs)

        # Maybe set a simulation per order parameter in the order parameter manager?
        # This is a very wasteful approach

    def run_all(self):
        # Instantiate simulations
        # threadpool = ThreadPool(processes=self.num_runs)
        # simulation_threads = []
        # for _ in range(self.num_runs):
        #     simulation = BoidSimulation(self.simulation_options, self.order_parameter)
        #     simulation_threads.append(threadpool.apply_async(simulation.run))

        # for async_result in simulation_threads:
        #     self.simulation_results.append(async_result.get())

        # When using MPI, we are basically just running the code n times and here
        # we know which rank we are on. If the rank is 0, then wait here for the
        # others to be done.
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        data = self._run_one()

        if rank == 0:
            self.simulation_results.append(data)
            for i in range(1, self.num_runs):
                mpi_data = comm.recv(source=i)
                self.simulation_results.append(mpi_data)
        else:
            comm.send(data, dest=0)
            sys.exit()

    def _run_one(self) -> list[SimulationResult]:
        simulation = BoidSimulation(
            self.simulation_options, self.order_parameter_manager
        )
        return simulation.run()

    def save_to_file(self, filename):
        for order_parameter_i in range(len(self.simulation_results[0])):
            simulation_dict = {}
            for i in range(len(self.simulation_results)):
                simulation_dict[i] = self.simulation_results[i][
                    order_parameter_i
                ].get_results()

            simulation_parameter = self.simulation_options.simulation_parameter

            simulation_saver = SimulationSaver(
                filename.split(".")[0]
                + "-"
                + self.simulation_results[0][order_parameter_i].order_parameter_name
                + "."
                + filename.split(".")[1],
                simulation_dict,
                simulation_parameter,
            )
            simulation_saver.save()

        # using_simulation_parameters = simulation_parameter is not None

        # write_file = f"./data/{filename}"
        # file_exists = Path(write_file).is_file()

        # # if the file exists,

        # if file_exists:
        #     with open(write_file, "r") as outfile:
        #         if using_simulation_parameters:
        #             existing_data = json.load(outfile)
        #             if existing_data["simulation_parameter"]:
        #                 existing_data[simulation_parameter] = simulation_dict
        #                 simulation_dict = existing_data
        #             else:
        #                 # ew, damn it
        #                 temp_simulation_dict = simulation_dict
        #                 simulation_dict = {}
        #                 simulation_dict[simulation_parameter] = temp_simulation_dict
        #                 simulation_dict["simulation_parameter"] = True
        #         else:
        #             simulation_dict["simulation_parameter"] = False

        # with open(write_file, "w+") as outfile:
        #     # this is so stupid but i cant think of a better way to do this at the moment
        #     if not file_exists:
        #         if using_simulation_parameters:
        #             temp_simulation_dict = simulation_dict
        #             simulation_dict = {}
        #             simulation_dict[simulation_parameter] = temp_simulation_dict
        #             simulation_dict["simulation_parameter"] = True
        #         else:
        #             simulation_dict["simulation_parameter"] = False

        #     json.dump(simulation_dict, outfile)
