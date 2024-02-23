from grapher.collator.data_collator import DataCollator
from grapher.data_point import DataPoint


class OrderVsTimeGenerator(DataCollator):

    def get_data_points(self):
        for i in range(len(self.data)):
            print(i)
