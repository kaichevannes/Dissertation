from grapher.grapher import Grapher
import argparse
import json


def plot(args):
    if args.threedimensions:
        data = {}
        filenames = [args.filename] + args.additionalfiles
        for i in range(len(filenames)):
            if args.folder is None:
                with open(f"./data/{filenames[i]}", "r") as f:
                    print(f"opening ./data/{filenames[i]}")
                    data[args.simulationparameters[i]] = json.load(f)
            else:
                with open(f"./data/{args.folder}/{filenames[i]}", "r") as f:
                    print(f"opening ./data/{args.folder}/{filenames[i]}")
                    data[args.simulationparameters[i]] = json.load(f)
        grapher = Grapher(
            data, args.xlabel, args.ylabel, args.zlabel, args.savefile, args.range
        )
        if args.multiline:
            grapher.generate_multiline_plot(args.simulationparameters)
        else:
            if args.timetogoal:
                grapher.generate_time_to_goal_heatmap(args.simulationparameters)
            else:
                grapher.generate_3d_contour(args.simulationparameters)
    else:
        if args.folder is None:
            with open(f"./data/{args.filename}", "r") as f:
                data = json.load(f)
        else:
            with open(f"./data/{args.folder}/{args.filename}", "r") as f:
                data = json.load(f)
        grapher = Grapher(
            data, args.xlabel, args.ylabel, args.zlabel, args.savefile, args.range
        )
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
    parser.add_argument("-3d", "--threedimensions", action="store_true", default=False)
    parser.add_argument("-x", "--xlabel")
    parser.add_argument("-y", "--ylabel")
    parser.add_argument("-z", "--zlabel")
    parser.add_argument("-af", "--additionalfiles", nargs="*")
    parser.add_argument("-sps", "--simulationparameters", nargs="*")
    parser.add_argument("-sf", "--savefile")
    parser.add_argument("-ml", "--multiline", action="store_true")
    parser.add_argument("-r", "--range", type=int)
    parser.add_argument("-ttg", "--timetogoal", action="store_true")
    parser.add_argument("-fo", "--folder")
    plot(parser.parse_args())

    # Example: python plot.py -f of0p0oe0to100.json -d -3d -af of0p1oe0to100.json of0p2oe0to100.json of0p3oe0to100.json of0p4oe0to100.json of0p5oe0to100.json of0p6oe0to100.json of0p7oe0to100.json of0p8oe0to100.json of0p9oe0to100.json of1p0oe0to100.json -sps 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 -y "number of entities overriden" -z "distance to goal" -x lambda -sf heatmap-magma-contour.png -s
