from entity.entity import Entity
from random import randint
import numpy as np


class EntityFactory:
    """The entity factory is an abstract class which is used to generate entities of a generic type."""

    def __init__(self, grid_size: int) -> None:
        """
        Args:
            grid_size (int): the square grid size of a coordinate
        """
        self.grid_size = grid_size

    def _generate_random_coordinates(self) -> np.ndarray[float, float]:
        """Generate the starting coordinates for an entity.

        Returns:
            np.ndarray[int, int]: an entities' starting coordinates
        """
        if self.grid_size < 1:
            raise ValueError("Grid size must be at least 1.")
        x_coordinate = randint(0, self.grid_size - 1)
        y_coordinate = randint(0, self.grid_size - 1)
        return np.array([x_coordinate, y_coordinate])

    def create_entity(self) -> Entity:
        """Factory method.

        Returns:
            Entity: an entity of a concrete type
        """
        raise NotImplementedError
