from simulation.simulation import Simulation
import numpy as np

# Radii
COLLISION_AVOIDANCE_RADIUS_SCALAR = 0.01
VELOCITY_MATCHING_RADIUS_SCALAR = 0.05
FLOCK_CENTERING_RADIUS_SCALAR = 0.05

# Weighting
COLLISION_AVOIDANCE_WEIGHTING = 0.002
VELOCITY_MATCHING_WEIGHTING = 0.06
FLOCK_CENTERING_WEIGHTING = 0.008


class BoidSimulation(Simulation):
    """The boid simulation class will be used to run simulations for specifically the boid model."""

    def __init__(
        self,
        swarm_size: int = 100,
        swarm_density: float = 0.25,
        radius_multiplier: float = 5,
        noise_fraction: float = 0.05,
        visualise: bool = False,
    ):
        """Simulation constructor, we assume that the Maruyama model is used with a radius multiplier k applied to it.

        Args:
            swarm_size (int, optional): the number of entities in a swarm. Defaults to 100.
            swarm_density (float, optional): the number of entities per unit area. Defaults to 0.25.
            radius_multiplier (float, optional): the multiplier applied to the maruyama radius values. Defaults to 5.
            noise_fraction (float, optional): the amount of noise in the simulation, how random the boids move on average. Defaults to 0.05.
            visualise (bool, optional): whether or not to visualise this simulation. Defaults to False.
        """
        super().__init__(swarm_size, swarm_density, visualise)
        self.noise_fraction = noise_fraction

        # Construct the radii for rules
        self.collision_avoidance_radius = (
            COLLISION_AVOIDANCE_RADIUS_SCALAR * self.grid_size * radius_multiplier
        )
        self.velocity_matching_radius = (
            VELOCITY_MATCHING_RADIUS_SCALAR * self.grid_size * radius_multiplier
        )
        self.flock_centering_radius = (
            FLOCK_CENTERING_RADIUS_SCALAR * self.grid_size * radius_multiplier
        )
