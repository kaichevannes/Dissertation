import numpy as np
from order_parameter.order_parameter import OrderParameter


class DistanceToGoal(OrderParameter):
    """The DistanceToGoal order parameter will calculate the average distance to
    the goal position of the swarm, a distance of 0 means all swarm members are
    exactly on the goal position."""

    def calculate(self):
        """Calculate the DistanceToGoal order parameter at this time step.

        Returns:
            float: the average distance to goal of the swarm at this time step
        """
        entities = self.swarm.entities
        goal_position = self.swarm.goal_position
        total_distance = 0
        for entity in entities:
            total_distance += np.linalg.norm(goal_position - entity.position)

        return total_distance / len(entities)
