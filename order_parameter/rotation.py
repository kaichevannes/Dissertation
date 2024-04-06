from order_parameter.order_parameter import OrderParameter
import numpy as np


class Rotation(OrderParameter):
    """The rotation order parameter is used to calculate rotation of the swarm by
    average how much rotation there is for each entity over z time steps and then
    averaging them."""

    def __init__(self, z=10):
        """
        Args:
            z (int, optional): how many time steps are counted to average rotation. Defaults to 10.
        """
        self.z = z
        self.velocities = []

    def calculate(self) -> float:
        """Calculate the rotation order parameter for this swarm, this will take
        z time steps to initialise and then return results for all other values.

        Returns:
            float: the amount of rotation of the swarm from 0 being no rotation to 1 being circular rotation
        """
        t = self.swarm.entities[0].time_step
        entities = self.swarm.entities

        if t == 0:
            self.velocities = []
            return None

        time_step_velocities = []
        for entity in entities:
            time_step_velocities.append(entity.velocity)
        self.velocities.append(time_step_velocities)

        if t < self.z:
            return None

        total_global_velocity_difference = 0
        for entity_index in range(len(entities)):
            total_velocity_difference = 0

            for velocity_index in range(self.z - 2):
                velocity_k = self.velocities[velocity_index][entity_index]
                velocity_k_plus_1 = self.velocities[velocity_index + 1][entity_index]
                total_velocity_difference += (
                    np.cross(velocity_k, velocity_k_plus_1)
                    - np.cross(velocity_k_plus_1, velocity_k)
                ) / (np.linalg.norm(velocity_k) * np.linalg.norm(velocity_k_plus_1))
            total_global_velocity_difference += (
                np.abs(total_velocity_difference) / self.z
            )

        self.velocities = self.velocities[1:]
        return total_global_velocity_difference / len(entities)

    def get_name(self) -> str:
        return "rotation"
