from grapher.collator.order_vs_time_collator import OrderVsTimeCollator
from grapher.collator.order_vs_param_collator import OrderVsParamCollator
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy.interpolate import griddata
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import median_filter
import numpy as np
from scipy.interpolate import griddata

import seaborn as sns
import pandas as pd

# Normal
plt.rcParams.update({"font.size": 16})

# Heatmap quad
# plt.rcParams.update({"font.size": 22})

# Distance to goal subplot
# plt.rcParams.update({"font.size": 28})
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
        range: int = None,
    ):
        self.data = data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.fig = None
        self.ax = None
        self.savefile = savefile
        self.range = range

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
        if self.range is None:
            ts = len(list(self.data.values())[0])
        else:
            ts = self.range
            xs = xs[: self.range]
            ys = ys[: self.range]
            yerrs = yerrs[: self.range]

        # self.ax.set_xscale("log")
        # self.ax.set_xlim(1, 100000)
        # self.ax.set_ylim(0, 10)
        self.ax.errorbar(
            xs,
            ys,
            yerr=yerrs,
            errorevery=max(int(ts * 0.01), 1),
            capsize=2,
            elinewidth=1,
        )
        self.ax.set_xlabel(self.xlabel, rotation=0)
        self.ax.set_ylabel(self.ylabel, rotation=0)

    def generate_3d_contour(self, simulation_parameters) -> None:
        collator = OrderVsParamCollator(self.data)

        plot_data = collator.get_3d_data_points(simulation_parameters)
        # self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.fig, self.ax = plt.subplots()

        xs = np.array([data_point.x for data_point in plot_data])
        ys = np.array([int(data_point.y) for data_point in plot_data])
        zs = np.array([data_point.z for data_point in plot_data])
        # zs = gaussian_filter1d(zs, sigma=1)
        # zs = median_filter(zs)
        # zs = gaussian_filter(zs, sigma=2)

        data = pd.DataFrame({self.xlabel: xs, self.ylabel: ys, self.zlabel: zs})

        data_pivoted = data.pivot(
            index=self.xlabel, columns=self.ylabel, values=self.zlabel
        )
        sns.heatmap(
            data_pivoted,
            vmin=np.min(zs),
            vmax=np.max(zs),
            ax=self.ax,
            # cmap="binary",
            cmap="pink_r",
            # cmap="Oranges_r",
            # cmap="Purples",
            # cmap="Greens",
            cbar_kws={"label": self.zlabel},
        )

    def generate_time_to_goal_heatmap(self, simulation_parameters) -> None:
        collator = OrderVsParamCollator(self.data)

        plot_data = collator.get_3d_time_to_data_points(simulation_parameters)
        # self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.fig, self.ax = plt.subplots()

        xs = np.array([data_point.x for data_point in plot_data])
        ys = np.array([int(data_point.y) for data_point in plot_data])
        zs = np.array([data_point.z for data_point in plot_data])
        # zs = gaussian_filter1d(zs, sigma=1)
        # zs = median_filter(zs)
        # zs = gaussian_filter(zs, sigma=2)

        data = pd.DataFrame({self.xlabel: xs, self.ylabel: ys, self.zlabel: zs})

        data_pivoted = data.pivot(
            index=self.xlabel, columns=self.ylabel, values=self.zlabel
        )
        sns.heatmap(
            data_pivoted,
            vmin=np.min(zs),
            vmax=np.max(zs),
            ax=self.ax,
            cmap="binary",
            # cmap="Purples",
            cbar_kws={"label": self.zlabel},
        )

    def save(self):
        self.fig.savefig(f"./zfigures/{self.savefile}", bbox_inches="tight")

    def show(self):
        plt.show()
