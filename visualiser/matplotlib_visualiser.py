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

    def visualise(self):
        # TODO: Decouple this visualuser from the swarm function somehow.
        if self.steps is None:
            raise LookupError("No max time step is assigned to this visualiser.")
        _ = animation.FuncAnimation(
            self.fig, self.swarm.update_plot, frames=self.steps
        )
        plt.show()
