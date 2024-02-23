from grapher.collator.order_vs_time_collator import OrderVsTimeGenerator
from grapher.collator.order_vs_param_collator import OrderVsParamCollator
import matplotlib.pyplot as plt
import json


class Grapher:
    """Graph the results from our simulations."""

    def __init__(self, filename: str):
        self.filename = filename
        self.fig = None
        self.ax = None

    def generate_graph(self):
        with open(f"./data/{self.filename}") as f:
            data = json.load(f)

        if data["simulation_parameter"]:
            collator = OrderVsTimeGenerator(data)
        else:
            collator = OrderVsParamCollator(data)

        plot_data = collator.get_data_points()
        xs, ys, yerrs = [
            (data_point.x, data_point.y, data_point.yerr) for data_point in plot_data
        ]
        self.fig, self.ax = plt.subplots()
        self.ax.errorbar(xs, ys, yerr=yerrs)

    def save(self):
        self.fig.savefig(f"./zfigures/{self.filename.split(".")[0]}.png")

    def show(self):
        self.fig.show()
