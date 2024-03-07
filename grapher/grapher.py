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

    def __init__(
        self,
        data: str,
        xlabel: str = None,
        ylabel: str = None,
        zlabel: str = None,
        savefile: str = None,
    ):
        self.data = data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.fig = None
        self.ax = None
        self.savefile = savefile

    def generate_errorbar(self) -> None:
        if self.data["simulation_parameter"]:
            collator = OrderVsParamCollator(self.data)
        else:
            collator = OrderVsTimeCollator(self.data)

        plot_data = collator.get_2d_data_points()
        # TODO: Make more efficient, brain isn't working at the moment
        xs = [data_point.x for data_point in plot_data]
        ys = [data_point.y for data_point in plot_data]
        yerrs = [data_point.yerr for data_point in plot_data]
        self.fig, self.ax = plt.subplots()
        self.ax.errorbar(xs, ys, yerr=yerrs)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

    def generate_3d_contour(self, simulation_parameters) -> None:
        # Always should be order vs param
        # if self.data["simulation_parameter"]:
        #     collator = OrderVsParamCollator(self.data)
        # else:
        #     raise ValueError("Can only plot 3d contours when simulation_parameter is true in the data.")
        collator = OrderVsParamCollator(self.data)

        plot_data = collator.get_3d_data_points(simulation_parameters)
        # xs = [data_point.x for data_point in plot_data]
        # ys = [data_point.y for data_point in plot_data]
        # zs = [data_point.z for data_point in plot_data]

        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})

        xs = [data_point.x for data_point in plot_data]
        ys = [data_point.y for data_point in plot_data]
        zs = [data_point.z for data_point in plot_data]
        # X, Y = np.meshgrid(xs, ys)
        zs = np.array(zs)

        # surf = self.ax.plot_trisurf(
        #     xs, ys, zs, cmap=cm.coolwarm, linewidth=0.2, antialiased=True
        # )
        surf = self.ax.scatter(xs, ys, zs)

        # Customize the z axis.
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        self.ax.zaxis.set_major_formatter("{x:.02f}")

        # Add a color bar which maps values to colors.
        self.fig.colorbar(surf, shrink=0.5, aspect=5)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_zlabel(self.zlabel)

    def save(self):
        self.fig.savefig(f"./zfigures/{self.savefile}")

    def show(self):
        plt.show()
