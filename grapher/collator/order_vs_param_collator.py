from grapher.collator.data_collator import DataCollator
from grapher.data_point.contour_point import ContourPoint
from grapher.data_point.multi_line_point import MultiLinePoint
from grapher.data_point.data_point import DataPoint
from grapher.data_point.error_bar_point import ErrorBarPoint
import numpy as np


class OrderVsParamCollator(DataCollator):

    def __init__(self, data):
        # Data needs to be all of the data put together in one file.
        super().__init__(data)

    def get_2d_data_points(self) -> list[DataPoint]:
        self.data.pop("simulation_parameter")

        ys = [float(y) for y in self.data.keys()]
        ys.sort()
        for y in ys:
            # y is the oe values
            parameter_data = self.data[str(y)]
            total_average = []
            # will have n number of parameter_data runs
            for run in parameter_data.values():
                # We want to get the average of the last 300 time steps of each of the runs
                values = list(run.values())
                last_300_runs = np.array(values[-300:])
                total_average.append(np.mean(last_300_runs))

            # print(f"total average for y = {y}: {total_average}")

            self.data_points.append(
                ErrorBarPoint(
                    y,
                    np.mean(total_average),
                    np.std(total_average) / np.sqrt(len(total_average)),
                )
            )

        return self.data_points

    def get_multi_data_points(self, simulation_parameters) -> list[DataPoint]:
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
                try:
                    # y is the oe values
                    parameter_data = one_file_data[str(y)]
                    total_average = 0
                    # will have n number of parameter_data runs
                    for run in parameter_data.values():
                        # We want to get the average of the last 300 runs of each of the runs
                        values = list(run.values())
                        if len(values) < 300:
                            continue
                        last_300_runs = np.array(values[-300:])
                        total_average += np.mean(last_300_runs)

                    # print(f"total average for y = {y}: {total_average}")

                    self.data_points.append(
                        ContourPoint(
                            float(x),
                            y,
                            total_average / len(parameter_data),
                        )
                    )
                except:
                    print(f"y = {y}")
                    print(f"last_300_runs = {last_300_runs}")
                    print(f"run = {run}")

        return self.data_points

    def get_3d_time_to_data_points(self, simulation_parameters) -> list[DataPoint]:
        # x - of, y - oe, z - dtg
        for x in simulation_parameters:
            # x is the of
            print(f"Getting time to values for the simulation parameter: {x}")
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
                    # We want to find where the average of the last 300 runs first occurs within 5%
                    values = list(run.values())
                    last_300_runs = np.array(values[-300:])
                    final_average = np.mean(last_300_runs)

                    starting_t = 0
                    current_average_runs = np.array(values[300:])
                    while (
                        abs(np.mean(current_average_runs) - final_average)
                        / final_average
                        > 0.05
                    ):
                        starting_t += 1
                        if starting_t >= len(values) - 300:
                            break
                        np.delete(current_average_runs, 1, 0)
                        np.append(current_average_runs, values[300 + starting_t])

                    # print(f"run {run} reached average in {starting_t} time steps.")
                    total_average += starting_t

                self.data_points.append(
                    ContourPoint(
                        float(x),
                        y,
                        total_average / len(parameter_data),
                    )
                )

        return self.data_points
