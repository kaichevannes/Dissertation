from grapher.collator.data_collator import DataCollator
from grapher.data_point.data_point import DataPoint
import numpy as np


class OrderVsTimeCollator(DataCollator):

    def get_2d_data_points(self):
        self.data.pop("simulation_parameter")

        # Average the value at timestep t for every run of our data.
        for t in range(len(self.data)):
            t_values = np.array(
                [
                    order_parameter_values[str(t)]
                    for order_parameter_values in self.data.values()
                ]
            )
            self.data_points.append(
                # append the time step, average values, and standard error of that value
                DataPoint(
                    t, np.mean(t_values), np.std(t_values) / np.sqrt(len(t_values))
                )
            )

        return self.data_points
