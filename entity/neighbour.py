from entity.entity import Entity
import numpy as np
import math


class Neighbour:
    """Entity class decorator which provides taurus mapping to entities while keeping the calculations on a grid."""

    def __init__(self, entity: Entity, source: Entity) -> None:
        """
        Args:
            entity (Entity): the neighbour entity
            source (Entity): the source entity
        """
        self._entity = entity
        self._source = source
        self._position = self.calculate_position(self._entity, self._source)

    def calculate_position(
        self, entity: Entity, source: Entity
    ) -> np.ndarray[float, float]:
        """Adjust the position of the neighbour boid so that we can calculate where it should be relative to the source boid"""
        grid_size = source._grid_size
        half_grid_size = grid_size / 2
        # position = np.copy(entity.position)
        position = np.array([float(entity.position[0]), float(entity.position[1])])

        # X-axis update
        if entity.position[0] - source.position[0] > half_grid_size:
            position -= np.array([grid_size, 0])
        elif entity.position[0] - source.position[0] < -half_grid_size:
            position += np.array([grid_size, 0])

        # Y-axis update
        if entity.position[1] - source.position[1] > half_grid_size:
            position -= np.array([0, grid_size])
        elif entity.position[1] - source.position[1] < -half_grid_size:
            position += np.array([0, grid_size])

        return position

    @property
    def position(self) -> np.ndarray[float, float]:
        """position property decorator for the updated position

        Returns:
            np.ndarray[int, int]: the adjusted neighbour position
        """
        return self._position

    @property
    def velocity(self) -> np.ndarray[float, float]:
        """velocity property

        Returns:
            np.ndarray[int, int]: the original entity velocity
        """
        return self._entity.velocity
