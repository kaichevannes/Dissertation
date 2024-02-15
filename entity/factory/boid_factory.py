from entity.factory.entity_factory import EntityFactory
from entity.boid import Boid


class BoidFactory(EntityFactory):
    """A factory for boids, instantiated with a constant velocity with the start time starting at zero."""

    def __init__(
        self,
        grid_size: float,
        collision_avoidance_radius: int,
        random_seed: int = None,
        velocity_matching_radius: int = None,
        flock_centering_radius: int = None,
        collision_avoidance_weighting: int = None,
        velocity_matching_weighting: int = None,
        flock_centering_weighting: int = None,
        noise_fraction: int = 0,
    ):
        """
        Args:
            grid_size (int): The size of the simulation grid
            neighbour_radius (int): The radius where a boid recognises neighbours
        """
        super().__init__(grid_size=grid_size, random_seed=random_seed)
        self.collision_avoidance_radius = collision_avoidance_radius
        self.velocity_matching_radius = velocity_matching_radius
        self.flock_centering_radius = flock_centering_radius
        self.collision_avoidance_weighting = collision_avoidance_weighting
        self.velocity_matching_weighting = velocity_matching_weighting
        self.flock_centering_weighting = flock_centering_weighting
        self.noise_fraction = noise_fraction

        if self.velocity_matching_radius is None:
            self.velocity_matching_radius = self.collision_avoidance_radius * 1.5
        if self.flock_centering_radius is None:
            self.flock_centering_radius = self.collision_avoidance_radius * 2

    def create_entity(self) -> Boid:
        position = self._generate_random_coordinates()
        velocity = self._generate_random_velocity()
        # velocity = self._generate_random_coordinates() / self.grid_size

        # TODO: Allow for changing just 1 at a time.
        if (
            self.collision_avoidance_weighting is not None
            and self.velocity_matching_weighting is not None
            and self.flock_centering_weighting is not None
        ):
            return Boid(
                collision_avoidance_radius=self.collision_avoidance_radius,
                velocity_matching_radius=self.velocity_matching_radius,
                flock_centering_radius=self.flock_centering_radius,
                grid_size=self.grid_size,
                initial_position=position,
                initial_velocity=velocity,
                collision_avoidance_weighting=self.collision_avoidance_weighting,
                velocity_matching_weighting=self.velocity_matching_weighting,
                flock_centering_weighting=self.flock_centering_weighting,
                noise_fraction=self.noise_fraction,
            )

        return Boid(
            collision_avoidance_radius=self.collision_avoidance_radius,
            velocity_matching_radius=self.velocity_matching_radius,
            flock_centering_radius=self.flock_centering_radius,
            grid_size=self.grid_size,
            initial_position=position,
            initial_velocity=velocity,
            noise_fraction=self.noise_fraction,
        )
