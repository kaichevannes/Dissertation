from swarm.swarm import Swarm


class OrderParameter:
    """The order parameter class is a base class for implementing order parameters.
    Each order parameter class will represent a specific order parameter and will
    be constructed using a swarm. It will then have some kind of calculate method
    and will return the order parameters value at that time step. Perhaps some
    kind of history mechanism could also be implemented."""

    def set_swarm(self, swarm: Swarm) -> None:
        """Set this order parameters swarm.

        Args:
            swarm (Swarm): the swarm that this order parameter will measure
        """
        self.swarm = swarm

    def get_name(self) -> str:
        """Get the name of this order parameter

        Raises:
            NotImplementedError: if not implemented
        """
        raise NotImplementedError

    def calculate(self) -> float:
        """Calculate this order parameter on the current state of the swarm.

        Raises:
            NotImplementedError: if not implemented, must be implemented in all subclasses

        Returns:
            float: a value between 0 and 1 for this order parameter
        """
        raise NotImplementedError
