import unittest
from entity.boid.boid import Boid
from entity.boid.boid_neighbour import BoidNeighbour
import numpy as np


class TestBoidNeighbour(unittest.TestCase):
    """Test a boid neighbour."""

    GRID_SIZE = 20

    def test_adjustment_up_down(self):
        """Test an up down adjustment."""
        y_position = 10

        boid1 = Boid(5, self.GRID_SIZE, np.array([19, y_position]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([1, y_position]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([21, y_position]))

    def test_adjustment_down_up(self):
        """Test a down up adjustment."""
        y_position = 10

        boid1 = Boid(5, self.GRID_SIZE, np.array([1, y_position]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([19, y_position]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([-1, y_position]))

    def test_adjustment_left_right(self):
        """Test a left right adjustment."""
        x_position = 10

        boid1 = Boid(5, self.GRID_SIZE, np.array([x_position, 19]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([x_position, 1]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([x_position, 21]))

    def test_adjustment_right_left(self):
        """Test a right left adjustment."""
        x_position = 10

        boid1 = Boid(5, self.GRID_SIZE, np.array([x_position, 1]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([x_position, 19]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([x_position, -1]))

    def test_adjustment_upper_left_corner(self):
        """Test an adjustment from the upper left corner."""
        boid1 = Boid(5, self.GRID_SIZE, np.array([2, 18]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([18, 2]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([-2, 22]))

    def test_adjustment_lower_right_corner(self):
        """Test an adjustment from the upper left corner."""
        boid1 = Boid(5, self.GRID_SIZE, np.array([18, 2]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([2, 18]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([22, -2]))

    def test_no_adjustment(self):
        """Test a position where there should be no adjustment."""
        boid1 = Boid(5, self.GRID_SIZE, np.array([12, 8]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([8, 12]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(adjusted_boid2.position, np.array([8, 12]))

    def test_original_boid_not_modified(self):
        """Test original boid not modified after adjustment."""
        y_position = 10

        boid1 = Boid(5, self.GRID_SIZE, np.array([19, y_position]))
        boid2 = Boid(5, self.GRID_SIZE, np.array([1, y_position]))
        boid_neighbour = BoidNeighbour(boid2, boid1)
        adjusted_boid2 = boid_neighbour.neighbour_boid

        np.testing.assert_equal(boid2.position, np.array([1, y_position]))
