from visualiser.visualiser import Visualiser
from matplotlib import animation
import matplotlib.pyplot as plt


class MatplotlibVisualiser(Visualiser):

    def initialise_visualisation(self):
        if self.swarm is None:
            raise LookupError("No swarm is assigned to this visualiser.")
        self.fig, self.ax = plt.subplots()
        self.swarm.initialise_plot(self.ax)
        plt.xlim(0, self.grid_size)
        plt.ylim(0, self.grid_size)

    def set_end_frame(self, end_frame):
        self.swarm.set_end_frame(end_frame)

    def visualise(self):
        # TODO: Decouple this visualuser from the swarm function somehow.
        if self.steps is None:
            raise LookupError("No max time step is assigned to this visualiser.")
        if self.save_interval is not None:
            self.swarm.initialise_saving(self.save_interval, self.savefolder)
        if self.adjuster is not None:
            self.swarm.initialise_continuous_adjustment(self.adjuster)
        _ = animation.FuncAnimation(
            self.fig,
            self.swarm.update_plot,
            frames=self.steps,
            repeat=False,
            interval=self.interval,
        )
        plt.show()

    def stop(self):
        plt.close()
