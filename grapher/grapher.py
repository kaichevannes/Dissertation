from grapher.collator.order_vs_time_collator import OrderVsTimeCollator
from grapher.collator.order_vs_param_collator import OrderVsParamCollator
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import json
import numpy as np

plt.rcParams.update({"font.size": 16})
SIZE = 20

class Grapher:
    """Graph the results from the simulations."""

    def __init__(self, filename: str, xlabel: str = None, ylabel: str = None):
        self.filename = filename
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.fig = None
        self.ax = None

    def generate_errorbar(self) -> None:
        data = self._get_data()

        if data["simulation_parameter"]:
            collator = OrderVsParamCollator(data)
        else:
            collator = OrderVsTimeCollator(data)

        plot_data = collator.get_2d_data_points()
        # TODO: Make more efficient, brain isn't working at the moment
        xs = [data_point.x for data_point in plot_data]
        ys = [data_point.y for data_point in plot_data]
        yerrs = [data_point.yerr for data_point in plot_data]
        self.fig, self.ax = plt.subplots()
        self.ax.errorbar(xs, ys, yerr=yerrs)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

    def generate_3d_contour(self) -> None:
        data = self._get_data()

        # Always should be order vs param
        if data["simulation_parameter"]:
            collator = OrderVsParamCollator(data)
        else:
            raise ValueError("Can only plot 3d contours when simulation_parameter is true in the data.")
        
        plot_data = collator.get_3d_data_points()
        X = [data_point.x for data_point in plot_data]
        Y = [data_point.y for data_point in plot_data]
        Z = [data_point.z for data_point in plot_data]

        X, Y = np.meshgrid(X, Y)
        self.fig, self.ax = plt.subplots()

        surf = self.ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

        # Customize the z axis.
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        self.ax.zaxis.set_major_formatter('{x:.02f}')

        # Add a color bar which maps values to colors.
        self.fig.colorbar(surf, shrink=0.5, aspect=5)
                

    def _get_data(self):
        with open(f"./data/{self.filename}", "r") as f:
            data = json.load(f)

        return data

    def save(self):
        self.fig.savefig(f"./zfigures/{self.filename.split(".")[0]}.png")

    def show(self):
        plt.show()
