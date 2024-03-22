from grapher.collator.order_vs_time_collator import OrderVsTimeCollator
from grapher.collator.order_vs_param_collator import OrderVsParamCollator
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter1d
from scipy.ndimage import median_filter
import numpy as np
from scipy.interpolate import griddata

import seaborn as sns
import pandas as pd

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

        self.ax.errorbar(
            xs,
            ys,
            yerr=yerrs,
            errorevery=max(int(ts * 0.01), 1),
            capsize=2,
            elinewidth=1,
        )
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

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

        data = pd.DataFrame({self.xlabel: xs, self.ylabel: ys, self.zlabel: zs})
        data_pivoted = data.pivot(
            index=self.xlabel, columns=self.ylabel, values=self.zlabel
        )
        sns.heatmap(
            data_pivoted,
            ax=self.ax,
            cmap="binary",
            cbar_kws={"label": self.zlabel},
        )

        # sns.kdeplot(x=data[self.ylabel], y=data[self.zlabel])

        self.ax.tricontour(
            ys,
            (xs * 10) + 0.5,
            zs,
            colors="black",
            levels=2,
        )
        # self.ax.tricontour(ys, xs, zs)

        # X, Y = np.meshgrid(xs, ys)
        # Z = griddata((xs, ys), zs, (X, Y), method="nearest")
        # self.ax.contour(
        #     X,
        #     Y,
        #     Z,
        # )
        # df["Z_value"] = pd.to_numeric(df["Z_value"])
        # pivotted = df.pivot("Y_value", "X_value", "Z_value")
        # sns.heatmap(pivotted, ax=self.ax)
        # surf = self.ax.plot_trisurf(
        #     xs, ys, zs, cmap=cm.coolwarm, linewidth=0.2, antialiased=True
        # )
        # surf = self.ax.scatter(xs, ys, zs)

        # Customize the z axis.
        # self.ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        # self.ax.zaxis.set_major_formatter("{x:.02f}")

        # Add a color bar which maps values to colors.
        # self.fig.colorbar(surf, shrink=0.5, aspect=5)
        # self.ax.set_xlabel(self.xlabel)
        # self.ax.set_ylabel(self.ylabel)
        # self.ax.set_zlabel(self.zlabel)

    def generate_multiline_plot(self, simulation_parameters) -> None:
        collator = OrderVsParamCollator(self.data)

        plot_data = collator.get_2d_data_points(simulation_parameters)
        # xs = [data_point.x for data_point in plot_data]
        # ys = [data_point.y for data_point in plot_data]
        # zs = [data_point.z for data_point in plot_data]

        self.fig, self.ax = plt.subplots()

        for s in simulation_parameters:
            xs = []
            ys = []
            yerrs = []
            for data_point in plot_data:
                if data_point.simulation_parameter == s:
                    xs.append(data_point.x)
                    ys.append(data_point.y)
                    yerrs.append(data_point.yerr)
            self.ax.scatter(xs, ys, label=s, s=4)
            self.ax.errorbar(xs, ys, yerrs, fmt="none")

        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.legend(title=self.zlabel)

    def save(self):
        self.fig.savefig(f"./zfigures/{self.savefile}", bbox_inches="tight")

    def show(self):
        plt.show()
