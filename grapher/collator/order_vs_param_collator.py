from grapher.collator.data_collator import DataCollator
from grapher.data_point.contour_point import ContourPoint
from grapher.data_point.multi_line_point import MultiLinePoint
from grapher.data_point.data_point import DataPoint
import numpy as np


class OrderVsParamCollator(DataCollator):

    def __init__(self, data):
        # Data needs to be all of the data put together in one file.
        super().__init__(data)

    def get_2d_data_points(self, simulation_parameters) -> list[DataPoint]:
        for x in simulation_parameters:
            # x is the of
            print(f"Getting values for the simulation parameter: {x}")
            one_file_data = self.data[x]
            one_file_data.pop("simulation_parameter")

            ys = [float(y) for y in one_file_data.keys()]
            # ys.sort()
            for y in ys:
                # y is the oe values
                parameter_data = one_file_data[str(y)]
                total_average = []
                # will have n number of parameter_data runs
                for run in parameter_data.values():
                    # We want to get the average of the last 300 time steps of each of the runs
                    values = list(run.values())
                    last_300_runs = np.array(values[-300:])
                    total_average.append(np.mean(last_300_runs))

                # print(f"total average for y = {y}: {total_average}")

                self.data_points.append(
                    MultiLinePoint(
                        y,
                        np.mean(total_average),
                        np.std(total_average) / np.sqrt(len(total_average)),
                        x,
                    )
                )

        return self.data_points

    def get_3d_data_points(self, simulation_parameters) -> list[DataPoint]:
        # x - of, y - oe, z - dtg
        for x in simulation_parameters:
            # x is the of
            print(f"Getting values for the simulation parameter: {x}")
            one_file_data = self.data[x]
            one_file_data.pop("simulation_parameter")

            ys = [float(y) for y in one_file_data.keys()]
            # ys.sort()
            for y in ys:
                # y is the oe values
                parameter_data = one_file_data[str(y)]
                total_average = 0
                # will have n number of parameter_data runs
                for run in parameter_data.values():
                    # We want to get the average of the last 500 runs of each of the runs
                    values = list(run.values())
                    last_500_runs = np.array(values[-500:])
                    total_average += np.mean(last_500_runs)

                # print(f"total average for y = {y}: {total_average}")

                self.data_points.append(
                    ContourPoint(
                        float(x),
                        y,
                        total_average / len(parameter_data),
                    )
                )

        return self.data_points
