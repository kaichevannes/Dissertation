from swarm.swarm import Swarm
from collections.abc import Callable


class SwarmAdjuster:

    def __init__(self, continuous: bool = False):
        self.continuous = continuous

    def set_strategy(self, strategy: Callable[[], None]):
        """Set the strategy for this adjuster.

        Args:
            strategy (Callable[[], None]): the strategy function, usually defined in a subclass
        """
        self.strategy = strategy

    def adjust_swarm(self, swarm: Swarm):
        if self.strategy is None:
            raise LookupError("No strategy is assigned to this SwarmAdjuster.")

        self.strategy(swarm)
