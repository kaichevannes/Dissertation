from grapher.data_point.data_point import DataPoint


class MultiLinePoint(DataPoint):

    def __init__(self, x: float, y: float, yerr: float, simulation_parameter: float):
        super().__init__(x, y)
        self.yerr = yerr
        self.simulation_parameter = simulation_parameter
