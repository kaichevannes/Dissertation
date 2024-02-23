from typing import TYPE_CHECKING, Callable
from entity.entity import Entity
from entity.neighbour import Neighbour
from swarm.swarm import Swarm
import numpy as np

if TYPE_CHECKING:
    from entity.boid import Boid

MAX_SPEED = 12

# Think about it as a Taurus wrapping around.


class Boid(Entity):
    """Represent a Boid from the Reynolds paper."""

    def __init__(
        self,
        collision_avoidance_radius: int,
        velocity_matching_radius: int,
        flock_centering_radius: int,
        grid_size: float,
        initial_position: np.ndarray[float, float],
        initial_velocity: np.ndarray[float, float] = np.array([0, 0]),
        initial_acceleration: np.ndarray[float, float] = np.array([0, 0]),
        initial_time_step: int = 0,
        collision_avoidance_weighting: int = 400,
        velocity_matching_weighting: int = 1,
        flock_centering_weighting: int = 10,
        noise_fraction: int = 0,
        override_fraction: float = 0,
    ):
        """
        Args:
            collision_avoidance_radius (int): the collision range of this boid
            velocity_matching_radius (int): the velocity matching radius of this boid
            flock_centering_radius (int): the flock centering range of this boid
            grid_size (int): the bounding size of the simulation grid
            initial_position (np.array[int, int]): the initial position of the boid
            initial_velocity (np.array[int, int], optional): the initial velocity of the boid (Defaults to [0,0])
            initial_acceleration (np.array[int, int], optional): the initial acceleration of the boid (Defaults to [0,0])
            initial_time (int, optional): the initial time step of the boid (Defaults to 0)
            collision_avoidance_weighting (int, optional): how much this boid wants to avoid collisions (Defaults to 400)
            velocity_matching_weighting (int, optional): how much this boid wants to match velocities with neighbouring boids (Defaults to 1)
            flock_centering_weighting (int, optional): how much this boid wants to move towards its neighbours center of mass (Defaults to 10)
            noise_fraction (int, optional): how much noise impacts this boids movements from 0 being none to 1 being totally random
            override_fraction (float, optional): how much control we are taking over this boid from 0 being none to 1 being total
        """
        super().__init__(
            grid_size=grid_size,
            initial_position=initial_position,
            initial_velocity=initial_velocity,
            initial_acceleration=initial_acceleration,
            initial_time_step=initial_time_step,
        )
        self._collision_avoidance_radius = collision_avoidance_radius
        self._velocity_matching_radius = velocity_matching_radius
        self._flock_centering_radius = flock_centering_radius
        _total_weighting = (
            collision_avoidance_weighting
            + velocity_matching_weighting
            + flock_centering_weighting
        )
        non_noise_component = (
            1 - noise_fraction
        )  # TODO: Enforce noise weighting between 0 and 1
        if non_noise_component != 0:
            self._collision_avoidance_weighting = non_noise_component * (
                collision_avoidance_weighting / _total_weighting
            )
            self._velocity_matching_weighting = non_noise_component * (
                velocity_matching_weighting / _total_weighting
            )
            self._flock_centering_weighting = non_noise_component * (
                flock_centering_weighting / _total_weighting
            )
        else:
            self._collision_avoidance_weighting = 0
            self._velocity_matching_weighting = 0
            self._flock_centering_weighting = 0
        self._noise_fraction = noise_fraction
        self.override_fraction = override_fraction

    def __deepcopy__(self, memo=None) -> "Boid":
        """Create a copy of this boid.

        Returns:
            Boid: a copy of this boid
        """
        if memo is None:
            memo = {}

        position_copy = np.copy(self.position)
        velocity_copy = np.copy(self.velocity)
        acceleration_copy = np.copy(self.acceleration)
        return self.__class__(
            self._collision_avoidance_radius,
            self._flock_centering_radius,
            self._velocity_matching_radius,
            self._grid_size,
            position_copy,
            velocity_copy,
            acceleration_copy,
            self.time_step,
            self._collision_avoidance_weighting,
            self._velocity_matching_weighting,
            self._flock_centering_weighting,
            self._noise_fraction,
        )

    def _calculate_neighbours(self, radius: int, swarm: Swarm) -> list["Boid"]:
        """Calculate the neighbours of this boid, other boids within this boids visual radius extending viewing the plane as a taurus.

        Returns:
            tuple[list[Boid], list[Boid]]: the neighbours and long neighbours of this boid
        """
        neighbours = []
        for boid in swarm.entities:
            if boid == self:
                continue

            neighbour = Neighbour(boid, self)
            distance_between_boids = np.linalg.norm(neighbour._position - self.position)
            if distance_between_boids <= radius:
                neighbours.append(neighbour)

        # TODO: Represent neighbours as a matrix for more efficient numpy operations.
        return neighbours

    def update_position(self, swarm: Swarm) -> None:
        """Update the position of this boid by a combination of boids movement and direct to goal movement

        Args:
            swarm (Swarm): the entire swarm
        """
        # Rule 1: Collision avoidance
        # Rule 2: Velocity matching
        # Rule 3: Flock centering

        # self.positions.append(
        #     [
        #         self.position,
        #         self.velocity,
        #         self.acceleration,
        #         self.time_step,
        #     ]
        # )

        if self.position[0] < 0:
            self.position[0] += self._grid_size
        elif self.position[0] > self._grid_size:
            self.position[0] -= self._grid_size

        if self.position[1] < 0:
            self.position[1] += self._grid_size
        elif self.position[1] > self._grid_size:
            self.position[1] -= self._grid_size

        normalised_to_goal_velocity = np.array([0, 0])
        if swarm.goal_position is not None:
            x_difference = swarm.goal_position[0] - self.position[0]
            y_difference = swarm.goal_position[1] - self.position[1]
            to_goal_velocity = np.array([x_difference, y_difference])
            normalised_to_goal_velocity = to_goal_velocity / np.linalg.norm(
                to_goal_velocity
            )

        self._update_velocity(swarm)
        self.velocity = (self.override_fraction) * normalised_to_goal_velocity + (
            1 - self.override_fraction
        ) * self.velocity

        self.position = self.position + self.velocity

        self.time_step += 1

    def _update_velocity(self, swarm: Swarm) -> None:
        """Update the velocity of this boid based on the updated acceleration.

        Args:
            swarm (Swarm): the entire swarm
        """
        self._update_acceleration(swarm)
        updated_velocity = self.velocity + self.acceleration
        self.velocity = updated_velocity / np.linalg.norm(updated_velocity)

    def _update_acceleration(self, swarm: Swarm) -> None:
        """Update the acceleration of this boid based on the three boid rules: Collision avoidance, Velocity matching, Flock centering.

        Args:
            swarm (Swarm): the entire swarm
        """
        (
            flock_centering_acceleration,
            flock_centering_neighbours,
        ) = self._flock_centering_acceleration(swarm)

        (
            velocity_matching_acceleration,
            velocity_matching_neighbours,
        ) = self._flock_centering_acceleration(
            Swarm(None, None, flock_centering_neighbours)
        )

        (
            collision_avoidance_accleration,
            collision_avoidance_neighbours,
        ) = self._collision_avoidance_acceleration(
            Swarm(None, None, velocity_matching_neighbours)
        )

        random_acceleration = np.random.normal(size=2) * self._noise_fraction

        # TODO: Enforce collision avoidance, velocity_matching, flock_centering being constrainted by size in that order increasing.
        self.acceleration = (
            collision_avoidance_accleration
            + velocity_matching_acceleration
            + flock_centering_acceleration
            + random_acceleration
        )
        # print(f"collision_avoidance_accleration = {collision_avoidance_accleration}")
        # print(f"velocity_matching_acceleration = {velocity_matching_acceleration}")
        # print(f"flock_centering_acceleration = {flock_centering_acceleration}")

    def _collision_avoidance_acceleration(
        self, swarm: Swarm
    ) -> np.ndarray[float, float]:
        """Accelerate in the direction opposite of a boids neighbours.

        Args:
            swarm (Swarm): the entire swarm
            neighbours (list[Boid]): provided neighbours

        Returns:
            np.ndarray[float, float]: the collision avoidance acceleration
        """
        # TODO: Change the acceleration calculations into a class
        neighbours = self._calculate_neighbours(self._collision_avoidance_radius, swarm)

        total_normalised_distance = np.array([0, 0])
        for neighbour in neighbours:
            distance = self.position - neighbour.position
            normalised_distance = distance / (
                1 + (np.linalg.norm(neighbour.position) ** 2)
            )
            total_normalised_distance = np.add(
                total_normalised_distance,
                normalised_distance,
            )

        return self._collision_avoidance_weighting * total_normalised_distance

    def _velocity_matching_acceleration(self, swarm: Swarm) -> np.ndarray[float, float]:
        """Boids will try to match velocity with nearby boids.

        Args:
            swarm (Swarm): the entire swarm

        Returns:
            np.ndarray[float, float]: the change in velocity for velocity matching
        """
        neighbours = self._calculate_neighbours(self._velocity_matching_radius, swarm)

        total_velocity = np.array([0, 0])
        for neighbour in neighbours:
            total_velocity = np.add(total_velocity, neighbour.velocity)

        normalised_velocity = total_velocity / np.max([len(neighbours), 1])

        return self._velocity_matching_weighting * (normalised_velocity - self.velocity)

    def _flock_centering_acceleration(self, swarm: Swarm) -> np.ndarray[float, float]:
        """Boids will attempt to move towards nearby flockmates

        Args:
            swarm (Swarm): the entire swarm
            neighbours (list[Boid]): provided neighbours

        Returns:
            np.ndarray[float, float]: the change in velocity for flock centering
        """
        neighbours = self._calculate_neighbours(self._flock_centering_radius, swarm)

        total_distance = np.array([0, 0])
        for neighbour in neighbours:
            total_distance = np.add(
                total_distance,
                neighbour.position,
            )

        normalised_distance = total_distance / np.max([len(neighbours), 1])

        return (
            self._flock_centering_weighting * (normalised_distance - self.position),
            neighbours,
        )
