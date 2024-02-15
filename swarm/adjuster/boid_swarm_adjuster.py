from swarm.adjuster.swarm_adjuster import SwarmAdjuster
from swarm.swarm import Swarm


class BoidSwarmAdjuster(SwarmAdjuster):
    """The BoidSwarmAdjuster class is used to modify the manual control we are able to exert on the swarm.
    This will typically take place after the swarm has first stabilised."""

    def set_override_fraction(self, override_fraction: float):
        self.override_fraction = override_fraction

    def set_num_entities(self, n: int):
        self.n = n

    def modify_first(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the first boid in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        first_entity = swarm.entities[0]
        first_entity.override_fraction = self.override_fraction

    def modify_n(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the first n boids in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        for entity in swarm.entities[: self.n]:
            entity.override_fraction = self.override_fraction

    def modify_all(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the every boid in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        for entity in swarm.entites:
            entity.override_fraction = self.override_fraction
