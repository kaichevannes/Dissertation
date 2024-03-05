from grapher.data_point.data_point import DataPoint


class ContourPoint(DataPoint):

    def __init__(self, x: float, y: float, z: float):
        super.__init__(x, y)
        self.z = z
