from grapher.data_point.data_point import DataPoint


class ErrorBarPoint(DataPoint):

    def __init__(self, x: float, y: float, yerr: float):
        super().__init__(x, y)
        self.yerr = yerr
