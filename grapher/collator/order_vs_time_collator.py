from grapher.collator.data_collator import DataCollator
from grapher.data_point.error_bar_point import ErrorBarPoint
import numpy as np


class OrderVsTimeCollator(DataCollator):

    def get_2d_data_points(self):
        self.data.pop("simulation_parameter")

        # Average the value at timestep t for every run of our data.
        for t in range(len(list(self.data.values())[0])):
            try:
                t_values = np.array(
                    [
                        order_parameter_values[str(t)]
                        for order_parameter_values in self.data.values()
                    ]
                )
            except:
                # Index doesnt exist, rotation case, bleh
                continue
            self.data_points.append(
                # append the time step, average values, and standard error of that value
                ErrorBarPoint(
                    t, np.mean(t_values), np.std(t_values) / np.sqrt(len(t_values))
                )
            )

        return self.data_points
