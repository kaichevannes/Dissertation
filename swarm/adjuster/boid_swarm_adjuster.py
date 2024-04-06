from swarm.adjuster.swarm_adjuster import SwarmAdjuster
from swarm.swarm import Swarm

# Circular import error if import from boid_simulation_options, should make a new const file but this will never change from this point.
COLLISION_AVOIDANCE_RADIUS_SCALAR = 0.01
VELOCITY_MATCHING_RADIUS_SCALAR = 0.05
FLOCK_CENTERING_RADIUS_SCALAR = 0.05


class BoidSwarmAdjuster(SwarmAdjuster):
    """The BoidSwarmAdjuster class is used to modify the manual control we are able to exert on the swarm.
    This will typically take place after the swarm has first stabilised."""

    def set_override_fraction(self, override_fraction: float):
        self.override_fraction = override_fraction

    def set_num_entities(self, n: int):
        self.n = n

    def set_k(self, k: float):
        self.k = k

    def set_velocity_multiplier(self, velocity_multiplier: float):
        self.velocity_multiplier = velocity_multiplier

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

    def modify_n_plus_radius(self, swarm: Swarm) -> None:
        """Adjust the lambda value and k for the first n boids in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """

        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        if self.k is None:
            raise LookupError("k must be set.")
        for entity in swarm.entities[: self.n]:
            entity.override_fraction = self.override_fraction
            entity._collision_avoidance_radius = (
                COLLISION_AVOIDANCE_RADIUS_SCALAR * self.k
            )
            entity._velocity_matching_radius = VELOCITY_MATCHING_RADIUS_SCALAR * self.k
            entity._flock_centering_radius = FLOCK_CENTERING_RADIUS_SCALAR * self.k

    def modify_n_plus_velocity(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the first n boids in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        for entity in swarm.entities[: self.n]:
            entity.override_fraction = self.override_fraction
            entity.velocity_multiplier = self.velocity_multiplier

    def modify_all(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the every boid in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        for entity in swarm.entities:
            entity.override_fraction = self.override_fraction
