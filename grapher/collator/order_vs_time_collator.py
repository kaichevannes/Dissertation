from grapher.collator.data_collator import DataCollator
from grapher.data_point import DataPoint


class OrderVsTimeCollator(DataCollator):

    def get_data_points(self):
        self.data.pop("simulation_parameter")

        # Average the value at timestep t for every run of our data.
        for t in range(len(self.data)):
            t_values = [
                order_parameter_values[t]
                for order_parameter_values in self.data.values()
            ]
            self.data_points.append(
                DataPoint(
                    t,
                )
            )
