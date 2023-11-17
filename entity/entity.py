from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from swarm.swarm import Swarm


class Entity:
    """An entity is an individual member of a swarm, taking actions based on a set of rules that must be implemented."""

    def __init__(
        self,
        grid_size: int,
        initial_position: np.ndarray[float, float],
        initial_velocity: np.ndarray[float, float] = np.array([0, 0]),
        initial_acceleration: np.ndarray[float, float] = np.array([0, 0]),
        initial_time_step: int = 0,
    ) -> None:
        """
        Args:
            grid_size (int): The bounding size of the simulation grid.
            initial_position np.ndarray[int, int]: The initial coordinate position of the entity
            initial_velocity (float): The initial velocity of the entity
            initial_time (int, optional): The initial time step of the entity (Defaults to 0)
        """
        self._grid_size = grid_size
        self.time_step = initial_time_step
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.positions = []

    def __str__(self) -> str:
        """Return a representation of this entity as a string.

        Returns:
            str: a string representation of this entity
        """
        grid_size_digits = len(str(self._grid_size - 1))

        return (
            "[{}] | p ({:{width}},{:{width}}) | v ({},{}) | a ({},{}) | t {} |".format(
                type(self).__name__.upper(),
                int(self.position[0]),
                int(self.position[1]),
                round(self.velocity[0], 2),
                round(self.velocity[1], 2),
                round(self.acceleration[0], 2),
                round(self.acceleration[1], 2),
                self.time_step,
                width=grid_size_digits,
            )
        )

    def update_position(self, swarm: "Swarm") -> None:
        """Update the position of this entity by following some rules of a particular model."""
        raise NotImplementedError
