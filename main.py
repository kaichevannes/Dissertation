from simulation.boid_simulation import BoidSimulation
from visualiser.matplotlib_visualiser import MatplotlibVisualiser
from simulation.options.boid_simulation_options import BoidSimulationOptions
from order_parameter.visceks import Visceks
from order_parameter.lanchesters import Lanchesters
from order_parameter.number_of_groups import NumberOfGroups
from order_parameter.rotation import Rotation
import argparse


def main(args):
    if args.slow:
        visualiser = MatplotlibVisualiser(slow=True)
    else:
        visualiser = MatplotlibVisualiser(slow=False)

    if args.visualise:
        simulation_options = BoidSimulationOptions(visualiser=visualiser)
    else:
        simulation_options = BoidSimulationOptions(visualiser=None)

    # Set order parameter here.
    visceks = Visceks()
    lanchesters = Lanchesters()
    number_of_groups = NumberOfGroups()
    rotation = Rotation()

    simulation = BoidSimulation(simulation_options, rotation, debug=True)
    simulation_result = simulation.run()
    # simulation_result.average_after_t0(500)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Disseration",
        description="Simulates a swarm",
    )
    parser.add_argument("-v", "--visualise", action="store_true")
    parser.add_argument("-s", "--slow", action="store_true")
    main(parser.parse_args())
