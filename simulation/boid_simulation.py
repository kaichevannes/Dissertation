from swarm.swarm import Swarm
from simulation.options.boid_simulation_options import BoidSimulationOptions
from simulation.simulation import Simulation
from simulation.simulation_result import SimulationResult
from entity.factory.boid_factory import BoidFactory

# from order_parameter.order_parameter import OrderParameter
from order_parameter.manager.order_parameter_manager import OrderParameterManager
from swarm.adjuster.boid_swarm_adjuster import BoidSwarmAdjuster
import numpy as np
import threading


class BoidSimulation(Simulation):
    """The boid simulation class will be used to run simulations for specifically the boid model."""

    def __init__(
        self,
        boid_simulation_options: BoidSimulationOptions = BoidSimulationOptions(),
        # order_parameter: OrderParameter = None,
        order_parameter_manager: OrderParameterManager = None,
    ):
        """Simulation constructor, we assume that the Maruyama model is used with a radius multiplier k applied to it.

        Args:
            boid_simulation_options (BoidSimulationOptions, optional): the boid simulation options for this simulation. Defaults to BoidSimulationOptions()
            order_parameter (OrderParameter, optional): the order parameter for this simulation. Defaults to None
        """
        self.boid_factory = BoidFactory(
            grid_size=boid_simulation_options.grid_size,
            collision_avoidance_radius=boid_simulation_options.collision_avoidance_radius,
            velocity_matching_radius=boid_simulation_options.velocity_matching_radius,
            flock_centering_radius=boid_simulation_options.flock_centering_radius,
            collision_avoidance_weighting=boid_simulation_options.collision_avoidance_weighting,
            velocity_matching_weighting=boid_simulation_options.velocity_matching_weighting,
            flock_centering_weighting=boid_simulation_options.flock_centering_weighting,
            noise_fraction=boid_simulation_options.noise_fraction,
        )
        # TODO: Look at builder pattern to make this less disgusting?
        self.swarm_size = boid_simulation_options.swarm_size
        self.swarm_density = boid_simulation_options.swarm_density
        self.visualiser = boid_simulation_options.visualiser
        self.grid_size = np.sqrt(self.swarm_size / self.swarm_density) - 1
        # self.order_parameter = order_parameter
        self.order_parameter_manager = order_parameter_manager
        self.swarm = Swarm(self.swarm_size, self.boid_factory)
        self.swarm.generate_entities()
        if self.order_parameter_manager is not None:
            self.order_parameter_manager.set_swarm(self.swarm)
        self.simulation_results = []
        if self.order_parameter_manager is not None:
            for order_parameter in self.order_parameter_manager.order_parameters:
                self.simulation_results.append(
                    SimulationResult(
                        order_parameter.get_name(),
                        boid_simulation_options.simulation_parameter,
                    )
                )
        self.swarm_adjuster = boid_simulation_options.swarm_adjuster
        self.pre_simulation_steps = boid_simulation_options.pre_simulation_steps
        self.max_time_step = boid_simulation_options.max_time_step

        # TODO: Make this a parameter
        self.swarm.set_goal_position(np.array([self.grid_size / 2, self.grid_size / 2]))

    def run(self) -> list[SimulationResult]:
        """Run this simulation from start to finish."""
        if self.visualiser is None:
            # print(f"Starting {type(self.order_parameter)} simulation.")
            for t in range(self.pre_simulation_steps):
                if t % 100 == 0:
                    print(f"{threading.current_thread()}: pre-t = {t}")
                self.swarm.step()
            if self.swarm_adjuster is not None:
                self.swarm_adjuster.adjust_swarm(self.swarm)
            for entity in self.swarm.entities:
                entity.time_step = 0
            for t in range(self.max_time_step):
                if t % 100 == 0:
                    print(f"{threading.current_thread()}: t = {t}")
                self.swarm.step()
                for order_parameter_i in range(
                    len(self.order_parameter_manager.order_parameters)
                ):
                    current_result = self.order_parameter_manager.order_parameters[
                        order_parameter_i
                    ].calculate()
                    self.simulation_results[order_parameter_i].add_result(
                        t, current_result
                    )
                if self.swarm_adjuster.continuous:
                    self.swarm_adjuster.adjust_swarm(self.swarm)
            return self.simulation_results
        else:
            # TODO: Make not horrendous, this is so bad but I ran out of time to fix it
            # Visualiser cannot get results for now.
            self.visualiser.set_swarm(self.swarm)
            self.visualiser.set_steps(self.pre_simulation_steps)
            self.visualiser.set_grid_size(self.grid_size)
            self.visualiser.initialise_visualisation()
            self.visualiser.set_end_frame(self.visualiser.steps - 1)
            self.visualiser.visualise()

            if self.swarm_adjuster is not None:
                self.swarm_adjuster.adjust_swarm(self.swarm)
                print("Adjusted swarm")
                print("Current swarm:")
                print(self.swarm)

            if self.swarm_adjuster.continuous:
                self.visualiser.set_continuous_adjuster(self.swarm_adjuster)

            self.visualiser.set_steps(self.max_time_step - self.pre_simulation_steps)
            # Adjust swarm here
            self.visualiser.initialise_visualisation()
            self.visualiser.set_end_frame(self.visualiser.steps)
            self.visualiser.visualise()
            return None
