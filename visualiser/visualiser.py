from swarm.swarm import Swarm
from simulation.simulation_result import SimulationResult

VISUALISATION_SLOW = 60
VISUALISATION_REAL_TIME = 0


class Visualiser:
    """The visualiser class will be used to visualise a swarm, decoupling it
    from the visual output and allowing for different implementations of visualisation.
    """

    def __init__(
        self, slow: bool = False, save_interval: int = None, savefolder: str = None
    ):
        """Visualiser constructor.

        Args:
            slow (bool, optional): a flag to set the simulation speed to be slower. Defaults to False.
        """
        if slow:
            self.interval = VISUALISATION_SLOW
        else:
            self.interval = VISUALISATION_REAL_TIME

        self.save_interval = save_interval
        self.savefolder = savefolder

    def set_swarm(self, swarm: Swarm):
        """Set the swarm to be visualised.

        Args:
            swarm (Swarm): the swarm being visualised
        """
        self.swarm = swarm

    def set_steps(self, steps: int):
        self.steps = steps

    def set_grid_size(self, grid_size: int):
        self.grid_size = grid_size

    def initialise_visualisation(self):
        raise NotImplementedError

    def visualise(self):
        raise NotImplementedError
