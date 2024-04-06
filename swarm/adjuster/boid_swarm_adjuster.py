from swarm.adjuster.swarm_adjuster import SwarmAdjuster
from swarm.swarm import Swarm
import numpy as np

# Circular import error if I just import from boid_simulation_options,
# should make a new const file but this will never change from this point so its easier to just copy paste.
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

    def modify_n_from_edge(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the swarm members on the edge of the swarm,
        this will be done at every time step.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")

        # 1. Find the centre of the swarm
        total_position = np.array([0, 0])
        entities = swarm.entities
        for entity in entities:
            total_position = np.add(entity.position, total_position)

        swarm_centre = total_position / len(entities)

        # 2. Order entities by distance from centre
        sorted_entites = sorted(
            entities,
            key=lambda entity: np.linalg.norm(swarm_centre - entity.position),
            reverse=True,
        )

        # 3. Take a moment to thank God for python
        # :)

        # 4. Override the members on the edge of the swarm
        for entity in sorted_entites[: self.n]:
            entity.override_fraction = self.override_fraction

        # 5. Unoverride all other members
        for entity in sorted_entites[self.n :]:
            entity.override_fraction = 0

    def modify_all(self, swarm: Swarm) -> None:
        """Adjust the lambda value for the every boid in the swarm.

        Args:
            swarm (Swarm): the swarm to modify
        """
        if self.override_fraction is None:
            raise LookupError("Override fraction must be set.")
        for entity in swarm.entities:
            entity.override_fraction = self.override_fraction
