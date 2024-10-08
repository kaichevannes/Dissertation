from grapher.data_point.data_point import DataPoint


class DataCollator:
    """The DataCollator class is used to turn stored data into a plottable format."""

    def __init__(self, data):
        self.data = data
        self.data_points = []

    def get_2d_data_points(self) -> list[DataPoint]:
        raise NotImplementedError

    def get_3d_data_points(self) -> list[DataPoint]:
        raise NotImplementedError
