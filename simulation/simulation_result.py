import numpy as np


class SimulationResult:
    """The simulation result class is used to handle the results from a simulation.
    This is generic to allow for different handling of the results themselves."""

    def __init__(self) -> None:
        self.results = []

    def add_result(self, result: float) -> None:
        """Add a result to the list of results

        Args:
            result (float): the result to append
        """
        if result is not None:
            self.results.append(result)

    def get_results(self) -> np.ndarray[float]:
        """Get the results from this simulation result class.

        Returns:
            np.ndarray[float]: a list of results from 0 to t where t is the number of time steps of the simulation
        """
        return np.array(self.results)

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
