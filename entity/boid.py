from typing import TYPE_CHECKING
from entity.entity import Entity
from swarm.swarm import Swarm
import numpy as np

if TYPE_CHECKING:
    from entity.boid import Boid


class Boid(Entity):
    """Represent a Boid from the Reynolds paper."""

    def __init__(
        self,
        neighbour_radius: int,
        grid_size: int,
        initial_position: np.ndarray[float, float],
        initial_velocity: np.ndarray[float, float] = np.array([0, 0]),
        initial_acceleration: np.ndarray[float, float] = np.array([0, 0]),
        initial_time_step: int = 0,
        collision_avoidance_weighting: float = 400.0,
        velocity_matching_weighting: float = 1.0,
        flock_centering_weighting: float = 10.0,
    ):
        """
        Args:
            neighbour_radius (int): the visual range of this boid
            grid_size (int): the bounding size of the simulation grid
            initial_position (np.array[int, int]): the initial position of the boid
            initial_velocity (np.array[int, int], optional): the initial velocity of the boid (Defaults to [0,0])
            initial_acceleration (np.array[int, int], optional): the initial acceleration of the boid (Defaults to [0,0])
            initial_time (int, optional): the initial time step of the boid (Defaults to 0)
            collision_avoidance_weighting (int, optional): how much this boid wants to avoid collisions (Defaults to 400)
            velocity_matching_weighting (int, optional): how much this boid wants to match velocities with neighbouring boids (Defaults to 1)
            flock_centering_weighting (int, optional): how much this boid wants to move towards its neighbours center of mass (Defaults to 10)
        """
        super().__init__(
            grid_size=grid_size,
            initial_position=initial_position,
            initial_velocity=initial_velocity,
            initial_acceleration=initial_acceleration,
            initial_time_step=initial_time_step,
        )
        self._neighbour_radius = neighbour_radius
        total_weighting = (
            collision_avoidance_weighting
            + velocity_matching_weighting
            + flock_centering_weighting
        )
        self._collision_avoidance_weighting = (
            collision_avoidance_weighting / total_weighting
        )
        self._velocity_matching_weighting = (
            velocity_matching_weighting / total_weighting
        )
        self._flock_centering_weighting = flock_centering_weighting / total_weighting

    def _calculate_neighbours(self, swarm: Swarm) -> list["Boid"]:
        """Calculate the neighbours of this boid, other boids within this boids visual radius.

        Returns:
            list[Boid]: the neighbours of this boid
        """
        neighbours = []
        for boid in swarm.entities:
            distance_to_boid = np.linalg.norm(boid.position - self.position)
            if distance_to_boid < self._neighbour_radius:
                neighbours.append(boid)

        # TODO: Represent neighbours as a matrix for more efficient numpy operations.
        return neighbours

    def update_position(self, swarm: Swarm) -> None:
        """Update the position of this boid based on the updated velocity

        Args:
            swarm (Swarm): the entire swarm
        """
        # Rule 1: Collision avoidance
        # Rule 2: Velocity matching
        # Rule 3: Flock centering

        self.positions.append(
            [
                self.position,
                self.velocity,
                self.acceleration,
                self.time_step,
            ]
        )

        if (
            self.position[0] < 0
            or self.position[0] > self._grid_size
            or self.position[1] < 0
            or self.position[1] > self._grid_size
        ):
            self.velocity = -self.velocity
        else:
            self._update_velocity(swarm)
        self.position = self.position + self.velocity
        self.time_step += 1

        # Move towards the center of mass of all boids

    def _update_velocity(self, swarm: Swarm) -> None:
        """Update the velocity of this boid based on the updated acceleration.

        Args:
            swarm (Swarm): the entire swarm
        """
        self._update_acceleration(swarm)
        current_velocity = self.velocity
        updated_velocity = self.velocity + self.acceleration
        # self.velocity = np.linalg.norm(current_velocity) * (
        #     updated_velocity / np.linalg.norm(updated_velocity)
        # )
        self.velocity = updated_velocity

    def _update_acceleration(self, swarm: Swarm) -> None:
        """Update the acceleration of this boid based on the three boid rules: Collision avoidance, Velocity matching, Flock centering.

        Args:
            swarm (Swarm): the entire swarm
        """
        neighbours = self._calculate_neighbours(swarm)
        self.acceleration = (
            self._collision_avoidance_acceleration(neighbours)
            + self._velocity_matching_acceleration(neighbours)
            + self._flock_centering_acceleration(neighbours)
        )

    def _collision_avoidance_acceleration(
        self, neighbours: list["Boid"]
    ) -> np.ndarray[float, float]:
        total_normalised_distance_from_neighbours = np.array([0, 0])
        for neighbour in neighbours:
            displaced_distance = self.position - neighbour.position
            normalised_displaced_distance = 1 / (
                1 + np.linalg.norm(neighbour.position - self.position) ** 2
            )

            total_normalised_distance_from_neighbours = np.add(
                total_normalised_distance_from_neighbours,
                (normalised_displaced_distance * displaced_distance),
            )

        return (
            self._collision_avoidance_weighting
            * (1 / len(neighbours))
            * total_normalised_distance_from_neighbours
        )

    def _velocity_matching_acceleration(
        self, neighbours: list["Boid"]
    ) -> np.ndarray[float, float]:
        average_position_of_neighbours = np.array([0, 0])
        for neighbour in neighbours:
            average_position_of_neighbours = np.add(
                average_position_of_neighbours,
                neighbour.position,
            )

        return (
            self._velocity_matching_weighting
            * (1 / len(neighbours))
            * average_position_of_neighbours
        )

    def _flock_centering_acceleration(
        self, neighbours: list["Boid"]
    ) -> np.ndarray[float, float]:
        total_distance_to_neighbours = np.array([0, 0])
        for neighbour in neighbours:
            total_distance_to_neighbours = np.add(
                total_distance_to_neighbours,
                neighbour.position - self.position,
            )

        return (
            self._flock_centering_weighting
            * (1 / len(neighbours))
            * total_distance_to_neighbours
        )
