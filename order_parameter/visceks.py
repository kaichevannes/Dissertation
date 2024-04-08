import numpy as np
from order_parameter.order_parameter import OrderParameter


class Visceks(OrderParameter):
    """The Visceks order parameter tells us how aligned a swarm is in terms of average velocity.
    0 means no alignment (random directions and magnitudes), 1 means full alignment (all boids have the same direction and magnitude).
    """

    def calculate(self, entities):
        """Calculate the Visceks order parameter at this time step.

        Returns:
            float: the Visceks order parameter at this time step
        """
        # from viscek, quoted from Harvey et al
        total_normalised_velocity = np.array([0, 0])
        for entity in entities:
            if np.linalg.norm(entity.velocity) == 0:
                continue
            normalised_velocity = entity.velocity / np.linalg.norm(entity.velocity)
            total_normalised_velocity = np.add(
                total_normalised_velocity,
                normalised_velocity,
            )

        return np.linalg.norm(total_normalised_velocity) / len(entities)

    def get_name(self) -> str:
        return "visceks"
