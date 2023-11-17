from typing import TYPE_CHECKING
import numpy as np
import copy

if TYPE_CHECKING:
    from entity.boid.boid import Boid


class BoidNeighbour:
    """A neighbour to a boid."""

    def __init__(
        self, radius: int, neighbour_boid: "Boid", source_boid: "Boid"
    ) -> None:
        """
        Args:
            neighbour_boid (Boid): the neighbour boid this class is a proxy for
            source_boid (Boid): the source boid which this neighbour is relative to
        """
        # if neighbour_boid == source_boid:
        #     raise ValueError("Neighbour and source boid must be different.")
        self.neighbour_radius = radius
        self.neighbour_boid = copy.deepcopy(
            neighbour_boid
        )  # We want a copy of the neighbour boid as we adjust its position and don't want that side effect to affect the calculations for that boid.
        self.source_boid = source_boid
        self.adjust_neighbour_position()

    def adjust_neighbour_position(self) -> None:
        """Adjust the position of the neighbour boid so that we can calculate where it should be relative to the source boid"""
        grid_size = self.source_boid._grid_size
        half_grid_size = grid_size / 2
        if (
            self.neighbour_boid.position[0] - self.source_boid.position[0]
            > half_grid_size
        ):
            self.neighbour_boid.position -= np.array([grid_size, 0])
        elif (
            self.neighbour_boid.position[0] - self.source_boid.position[0]
            < -half_grid_size
        ):
            self.neighbour_boid.position += np.array([grid_size, 0])

        if (
            self.neighbour_boid.position[1] - self.source_boid.position[1]
            > half_grid_size
        ):
            self.neighbour_boid.position -= np.array([0, grid_size])
        elif (
            self.neighbour_boid.position[1] - self.source_boid.position[1]
            < -half_grid_size
        ):
            self.neighbour_boid.position += np.array([0, grid_size])

    def is_neighbour(self) -> bool:
        """Check if the provided neighbour is a neighbour to the provided source boid.

        Returns:
            bool: true if the provided neighbour is a neighbour to the provided source, false otherwise
        """
        distance_to_source = np.linalg.norm(
            self.neighbour_boid.position - self.source_boid.position
        )
        return distance_to_source <= self.neighbour_radius
