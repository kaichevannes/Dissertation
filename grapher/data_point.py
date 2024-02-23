class DataPoint:
    """Represent a data point to plot."""

    def __init__(self, x: float, y: float, yerr: float):
        self.x = x
        self.y = y
        self.yerr = yerr
