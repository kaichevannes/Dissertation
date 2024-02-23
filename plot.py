from grapher.grapher import Grapher
import argparse


def plot(args):
    with open(f"./data/{args.filename}") as f:
        grapher = Grapher(f)
        grapher.generate_graph()
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
    plot(parser.parse_args())
