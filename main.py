from simulation.manager.boid_simulation_manager import BoidSimulationManager
from visualiser.matplotlib_visualiser import MatplotlibVisualiser
from simulation.options.boid_simulation_options import BoidSimulationOptions
from swarm.adjuster.boid_swarm_adjuster import BoidSwarmAdjuster
from order_parameter.visceks import Visceks
from order_parameter.lanchesters import Lanchesters
from order_parameter.number_of_groups import NumberOfGroups
from order_parameter.rotation import Rotation
import argparse


def main(args):
    boid_swarm_adjuster = BoidSwarmAdjuster()
    boid_swarm_adjuster.set_override_fraction(0.3)
    boid_swarm_adjuster.set_num_entities(50)
    boid_swarm_adjuster.set_strategy(boid_swarm_adjuster.modify_n)

    simulation_options = BoidSimulationOptions(
        boid_swarm_adjuster=boid_swarm_adjuster,
        radius_multiplier=5.5,
        pre_simulation_steps=0,
        max_time_step=20,
    )

    if args.numruns is not None:
        num_runs = args.numruns
    else:
        num_runs = 10

    if args.visualise:
        simulation_options.visualiser = MatplotlibVisualiser(slow=args.slow)
        num_runs = 1

    # Set order parameter here.
    match args.order_parameter[0]:
        case "visceks":
            order_parameter = Visceks()
        case "lanchesters":
            order_parameter = Lanchesters()
        case "groups":
            order_parameter = NumberOfGroups()
        case "rotation":
            order_parameter = Rotation()
        case _:
            order_parameter = None

    simulation_manager = BoidSimulationManager(
        order_parameter, simulation_options, num_runs=num_runs
    )
    simulation_manager.run_all()

    if args.filename is not None:
        simulation_manager.save_to_file(args.filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration Simulation",
        description="Simulates a swarm",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    parser.add_argument("-n", "--numruns", type=int)
    parser.add_argument("-f", "--filename")
    parser.add_argument(
        "order_parameter",
        choices=["visceks", "lanchesters", "groups", "rotation"],
        nargs="*",
    )
    main(parser.parse_args())
