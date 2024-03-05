from grapher.grapher import Grapher
import argparse


def plot(args):
    grapher = Grapher(args.filename, args.xlabel, args.ylabel)
    grapher.generate_errorbar()
    if args.display:
        grapher.show()
    if args.save:
        grapher.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Swarm Dissertation Plotting",
        description="Plot data from the swarm.",
    )
    parser.add_argument("-f", "--filename", required=True)
    parser.add_argument("-d", "--display", action="store_true")
    parser.add_argument("-s", "--save", action="store_true")
    parser.add_argument("-x", "--xlabel")
    parser.add_argument("-y", "--ylabel")
    plot(parser.parse_args())
