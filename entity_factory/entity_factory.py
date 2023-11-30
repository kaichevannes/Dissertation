from entity.entity import Entity
import random
import numpy as np
import math


class EntityFactory:
    """The entity factory is an abstract class which is used to generate entities of a generic type."""

    def __init__(self, grid_size: int, random_seed: int) -> None:
        """
        Args:
            grid_size (int): the square grid size of a coordinate
        """
        self.grid_size = grid_size
        if random_seed is not None:
            random.seed(random_seed)

    def _generate_random_coordinates(self) -> np.ndarray[float, float]:
        """Generate the starting coordinates for an entity.

        Returns:
            np.ndarray[int, int]: an entities' starting coordinates
        """
        if self.grid_size < 1:
            raise ValueError("Grid size must be at least 1.")
        x_coordinate = random.randint(0, math.ceil(self.grid_size))
        y_coordinate = random.randint(0, math.ceil(self.grid_size))
        return np.array([x_coordinate, y_coordinate])

    def create_entity(self) -> Entity:
        """Factory method.

        Returns:
            Entity: an entity of a concrete type
        """
        raise NotImplementedError
