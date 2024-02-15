from simulation.options.simulation_options import SimulationOptions
from swarm.adjuster.boid_swarm_adjuster import BoidSwarmAdjuster
from visualiser.visualiser import Visualiser

# Radii
COLLISION_AVOIDANCE_RADIUS_SCALAR = 0.01
VELOCITY_MATCHING_RADIUS_SCALAR = 0.05
FLOCK_CENTERING_RADIUS_SCALAR = 0.05

# Weighting
COLLISION_AVOIDANCE_WEIGHTING = 0.002
VELOCITY_MATCHING_WEIGHTING = 0.06
FLOCK_CENTERING_WEIGHTING = 0.008


class BoidSimulationOptions(SimulationOptions):
    """The simulation options for the boids model."""

    def __init__(
        self,
        swarm_size: int = 100,
        swarm_density: float = 0.25,
        radius_multiplier: float = 5,
        noise_fraction: float = 0.05,
        visualiser: Visualiser = None,
        max_time_step: int = 1000,
        pre_simulation_steps: int = 500,
        boid_swarm_adjuster: BoidSwarmAdjuster = None,
    ):
        """Options constructor.

        Args:
            swarm_size (int, optional): the number of entities in the swarm
            swarm_density (float, optional): the number of entities per square unit
            radius_multiplier (float, optional): the multiplier on the Maruyama radius values
            noise_fraction (float, optional): the amount of noise for the boids movement
            visualiser (Visualiser, optional): the visualiser class which is used to visualiser this simulation. Defaults to None.
            max_time_step (int, optional): the maximum time step for the simulation. Defaults to 1000.
            pre_simulation_steps (int, optional): the number of simulation steps to run before recording any results. Defaults to 500
            boid_swarm_adjuster (BoidSwarmAdjuster, optional): the swarm adjust class used to manually override some members of the swarm. Defaults to None.
        """
        super().__init__(
            swarm_size,
            swarm_density,
            visualiser,
            max_time_step,
            pre_simulation_steps,
            boid_swarm_adjuster,
        )
        self.radius_multiplier = radius_multiplier
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

        self.collision_avoidance_weighting = COLLISION_AVOIDANCE_WEIGHTING
        self.velocity_matching_weighting = VELOCITY_MATCHING_WEIGHTING
        self.flock_centering_weighting = FLOCK_CENTERING_WEIGHTING
