from grapher.collator.order_vs_time_collator import OrderVsTimeCollator
from grapher.collator.order_vs_param_collator import OrderVsParamCollator
import matplotlib.pyplot as plt
import json


class Grapher:
    """Graph the results from the simulations."""

    def __init__(self, filename: str):
        self.filename = filename
        self.fig = None
        self.ax = None

    def generate_errorbar(self):
        with open(f"./data/{self.filename}", "r") as f:
            data = json.load(f)

        if data["simulation_parameter"]:
            collator = OrderVsParamCollator(data)
        else:
            collator = OrderVsTimeCollator(data)

        plot_data = collator.get_data_points()
        xs, ys, yerrs = [
            (data_point.x, data_point.y, data_point.yerr) for data_point in plot_data
        ]
        self.fig, self.ax = plt.subplots()
        self.ax.errorbar(xs, ys, yerr=yerrs)

    def generate_heatmap(self):
        pass

    def save(self):
        self.fig.savefig(f"./zfigures/{self.filename.split(".")[0]}.png")

    def show(self):
        self.fig.show()
