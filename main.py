from simulation.manager.boid_simulation_manager import BoidSimulationManager
from visualiser.matplotlib_visualiser import MatplotlibVisualiser
from simulation.options.boid_simulation_options import BoidSimulationOptions
from swarm.adjuster.boid_swarm_adjuster import BoidSwarmAdjuster
from order_parameter.visceks import Visceks
from order_parameter.lanchesters import Lanchesters
from order_parameter.number_of_groups import NumberOfGroups
from order_parameter.rotation import Rotation
from order_parameter.distance_to_goal import DistanceToGoal
from order_parameter.manager.order_parameter_manager import OrderParameterManager
import argparse
from mpi4py import MPI


def main(args):
    # BoidSwarmAdjuster
    boid_swarm_adjuster = BoidSwarmAdjuster()

    if args.overridefraction is not None:
        boid_swarm_adjuster.set_override_fraction(args.overridefraction)
    else:
        boid_swarm_adjuster.set_override_fraction(0.3)

    if args.overrideentities is not None:
        boid_swarm_adjuster.set_num_entities(args.overrideentities)
    else:
        boid_swarm_adjuster.set_num_entities(50)

    # Experiment 1:
    # boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n)

    # Experiment 2:
    # boid_swarm_adjuster.continuous = True
    # boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n_from_edge)

    # Experiment 3:
    boid_swarm_adjuster.set_k(5.5)
    boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n_plus_radius)

    # Experiment 4:
    # boid_swarm_adjuster.continuous = True
    # boid_swarm_adjuster.set_k(5.5)
    # boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n_from_edge_plus_radius)

    # boid_swarm_adjuster.set_velocity_multiplier(1.1)
    # boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n_plus_velocity)

    # BoidSimulationOptions
    if args.radiusmultiplier is not None:
        simulation_options = BoidSimulationOptions(
            boid_swarm_adjuster=boid_swarm_adjuster,
            radius_multiplier=args.radiusmultiplier,
        )
    else:
        simulation_options = BoidSimulationOptions(
            boid_swarm_adjuster=boid_swarm_adjuster
        )

    if args.overridefraction is None and args.overrideentities is None:
        simulation_options.boid_swarm_adjuster = None

    if args.simulationparameter is not None:
        simulation_options.simulation_parameter = args.simulationparameter
    else:
        simulation_options.simulation_parameter = None

    if args.presimulationsteps is not None:
        simulation_options.pre_simulation_steps = args.presimulationsteps

    if args.maxtimestep is not None:
        simulation_options.max_time_step = args.maxtimestep

    if args.noisefraction is not None:
        simulation_options.noise_fraction = args.noisefraction

    # Number of runs
    comm = MPI.COMM_WORLD
    num_runs = comm.Get_size()

    # Visualisation
    if args.visualise:
        simulation_options.visualiser = MatplotlibVisualiser(
            slow=args.slow, save_interval=args.saveinterval, savefolder=args.savefolder
        )
        num_runs = 1

    # Order parameter
    if args.order_parameter == "none":
        order_parameter_manager = None
    else:
        order_parameter_manager = OrderParameterManager()
        if args.additionalparameters is None:
            all_order_parameters = [args.order_parameter]
        else:
            all_order_parameters = [args.order_parameter] + args.additionalparameters
        for order_parameter in all_order_parameters:
            match order_parameter:
                case "visceks":
                    current_order_parameter = Visceks()
                case "lanchesters":
                    current_order_parameter = Lanchesters()
                case "groups":
                    current_order_parameter = NumberOfGroups()
                case "rotation":
                    current_order_parameter = Rotation()
                case "distancetogoal":
                    current_order_parameter = DistanceToGoal()
                case _:
                    current_order_parameter = None
            order_parameter_manager.add_order_parameter(current_order_parameter)

    # BoidSimulationManager
    simulation_manager = BoidSimulationManager(
        order_parameter_manager, simulation_options, num_runs=num_runs
    )
    simulation_manager.run_all()

    # Saving
    if args.filename is not None:
        simulation_manager.save_to_file(args.filename)


if __name__ == "__main__":
    # Current task
    # 1. Plot override fraction = 0.3 with swarm members = say 10 vs time to see how long it takes
    # 2. Find a way to automatically calculate when in the graph we are at the average
    # 3. Get data for override fraction at 0 changing swarm members from 0 to 100, and calculate this
    #    for override fraction 0.1, 0.2, ... 1 for the time being, plot as heatmap. This will be average
    #    distance to the goal in each case
    # Plot override fraction vs distance to goal (new order parameter)
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration Simulation",
        description="Simulates a swarm",
        usage="Usage: mpiexec -n [number_of_cpu_cores] python main.py -params",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    parser.add_argument("-f", "--filename")
    parser.add_argument("-p", "--presimulationsteps", type=int)
    parser.add_argument("-t", "--maxtimestep", type=int)
    parser.add_argument("-of", "--overridefraction", type=float)
    parser.add_argument("-oe", "--overrideentities", type=int)
    parser.add_argument(
        "-sp",
        "--simulationparameter",
        type=float,
        help="The value for the simulation parameter that is being used if any.",
    )
    parser.add_argument(
        "order_parameter",
        choices=[
            "visceks",
            "lanchesters",
            "groups",
            "rotation",
            "distancetogoal",
            "none",
        ],
    )
    parser.add_argument("-k", "--radiusmultiplier", type=float)
    parser.add_argument("-si", "--saveinterval", type=int)
    parser.add_argument("-sf", "--savefolder")
    parser.add_argument("-nf", "--noisefraction", type=float)
    parser.add_argument("-aps", "--additionalparameters", nargs="*")
    main(parser.parse_args())
