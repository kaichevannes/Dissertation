import numpy as np


class SimulationResult:
    """The simulation result class is used to handle the results from a simulation.
    This is generic to allow for different handling of the results."""

    def __init__(
        self,
        order_parameter_name: str,
        simulation_parameter_value=None,
    ) -> None:
        """Initialise results to be an empty dict."""
        self.results = {}
        self.overriden = False
        self.order_parameter_name = order_parameter_name
        self.simulation_parameter_value = simulation_parameter_value

    def add_result(self, timestep: int, result: float) -> None:
        """Add a result to the list of results

        Args:
            result (float): the result to append
        """
        if result is not None:
            self.results[timestep] = result

    def get_results(self) -> dict[int, float]:
        """Get the results from this simulation result class.

        Returns:
            dict[int,float]: a dict of results [timestep, value] from 0 to t where t is the number of time steps of the simulation
        """
        return self.results

    def average_after_t0(self, t0: int) -> float:
        """Get the average value of the simulation after the t0'th value.

        Args:
            t0 (int): the point to average the values after

        Raises:
            ValueError: if t0 is larger than the number of results we have

        Returns:
            float: the average result
        """
        if t0 > len(self.results):
            raise ValueError("t0 cannot be larger than the number of results.")

        remaining_results = np.array(self.results[t0:])
        return np.average(remaining_results)
