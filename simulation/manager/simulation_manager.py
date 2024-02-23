from simulation.options.simulation_options import SimulationOptions
from order_parameter.order_parameter import OrderParameter


class SimulationManager:
    """The simulation manager class will manage a set of simulations, assigning
    order parameters and values to each simulation as required to run an experiment.
    This will provide multi-threading and collate results. Simulations are instanciated here.
    There should be the option to add to existing results with more values if a
    particular range of values in the graph needs more experiment values.
    """

    def __init__(
        self,
        order_parameter: OrderParameter,
        simulation_options: SimulationOptions,
        num_runs: int,
    ):
        """Order parameter over time constructor

        Args:
            order_parameter (OrderParameter): the order parameter which will be used to evaluate the swarm at each time step
            simulation_options (SimulationOptions, optional): the simulation options that we use to instantiate the simulation. Defaults to None
        """
        # Unsure
        # average alignment over time as noise changes - error bars
        # alignment as time changes - line graph, still error bars?
        # We will have a list of values
        # We will have a list of order parameters to measure, perhaps represented as classes that can be passed to a swarm?
        # For the list of values, we will sometimes have a

        # The two options are:
        # 1 - varying time and measuring an order parameter
        # 2 - varying an order parameter and getting an average convergence value after t0 time steps
        # In this case then 2 factory methods should probably be used for each case.

        # The default case is just measuring an order parameter over time.
        self.order_parameter = order_parameter
        self.simulation_options = simulation_options
        self.num_runs = num_runs
        self.simulation_results = []

    def run_all(self):
        """Run all simulations with the given order parameters and options.

        Raises:
            NotImplementedError: if not implemented
        """
        raise NotImplementedError
