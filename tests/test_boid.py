import unittest
from entity.boid.boid import Boid
from swarm.swarm import Swarm
import numpy as np
import copy


class TestBoid(unittest.TestCase):
    """Test the implementation of a boid."""

    def test_constructor_logic(self) -> None:
        """Test the constructor correctly assigns values and weights add up to 1."""
        boid = Boid(25, 100, np.array([50, 50]))
        self.assertEqual(boid._grid_size, 100)
        np.testing.assert_equal(boid.position, np.array([50, 50]))
        np.testing.assert_equal(boid.velocity, np.array([0, 0]))
        np.testing.assert_equal(boid.acceleration, np.array([0, 0]))
        self.assertEqual(boid.time_step, 0)
        self.assertEqual(boid._neighbour_radius, 25)
        self.assertEqual(
            boid._collision_avoidance_weighting
            + boid._flock_centering_weighting
            + boid._velocity_matching_weighting,
            1,
        )

    def test_copy_special_method(self) -> None:
        """Test that a copy of the boid has the same properties as the original."""
        boid = Boid(
            25,
            100,
            np.array([50, 50]),
            np.array([5, 5]),
            np.array([-2, -3]),
            10,
            128,
            17,
            91,
        )
        copy_boid = copy.copy(boid)

        self.assertEqual(boid._neighbour_radius, copy_boid._neighbour_radius)
        self.assertEqual(boid._grid_size, copy_boid._grid_size)
        np.testing.assert_equal(boid.position, copy_boid.position)
        np.testing.assert_equal(boid.velocity, copy_boid.velocity)
        np.testing.assert_equal(boid.acceleration, copy_boid.acceleration)
        self.assertEqual(boid.time_step, copy_boid.time_step)
        self.assertEqual(
            boid._collision_avoidance_weighting,
            copy_boid._collision_avoidance_weighting,
        )
        self.assertEqual(
            boid._flock_centering_weighting, copy_boid._flock_centering_weighting
        )
        self.assertEqual(
            boid._velocity_matching_weighting, copy_boid._velocity_matching_weighting
        )

    def test_calculate_neighbours_lbv(self) -> None:
        """Test the lower valid boundary on calculating the neighbours given a swarm."""
        boid = Boid(5, 20, np.array([50, 50]))
        swarm = Swarm(None, None, [boid])

        neighbours = boid._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours, [])

    def test_calculate_neighbour_x_axis(self) -> None:
        """Test the calculate neighbour function for boids on the same y coordinate."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid1 = Boid(neighbour_radius, grid_size, np.array([5, y_position]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([10, y_position]))
        boid3 = Boid(neighbour_radius, grid_size, np.array([19, y_position]))

        swarm = Swarm(None, None, [boid1, boid2, boid3])
        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1])

        neighbours3 = boid3._calculate_neighbours(swarm)
        self.assertEqual(neighbours3, [])

    def test_calculate_neighbour_y_axis(self) -> None:
        """Test the calculate neighbour function for boids on the same x coordinate."""
        neighbour_radius = 5
        grid_size = 20
        x_position = 10
        boid1 = Boid(neighbour_radius, grid_size, np.array([x_position, 5]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([x_position, 10]))
        boid3 = Boid(neighbour_radius, grid_size, np.array([x_position, 19]))

        swarm = Swarm(None, None, [boid1, boid2, boid3])
        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1])

        neighbours3 = boid3._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours3, [])

    def test_calculate_neighbour_v(self) -> None:
        """Test the valid interval"""
        neighbour_radius = 6
        grid_size = 20
        boid1 = Boid(neighbour_radius, grid_size, np.array([5, 7]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([9, 11]))
        boid3 = Boid(neighbour_radius, grid_size, np.array([11, 6]))
        boid4 = Boid(neighbour_radius, grid_size, np.array([19, 19]))
        swarm = Swarm(None, None, [boid1, boid2, boid3, boid4])

        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1, boid3])

        neighbours3 = boid3._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours3, [boid2])

        neighbours4 = boid4._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours4, [])

    def test_calculate_neighbour_wrap_x(self):
        """Test boids being neighbours that wrap around the x axis."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10

        boid1 = Boid(neighbour_radius, grid_size, np.array([1, y_position]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([19, y_position]))
        swarm = Swarm(None, None, [boid1, boid2])

        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1])

    def test_calculate_neighbour_wrap_y(self):
        """Test boids being neighbours that wrap around the y axis."""
        neighbour_radius = 5
        grid_size = 20
        x_position = 10

        boid1 = Boid(neighbour_radius, grid_size, np.array([x_position, 1]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([x_position, 19]))
        swarm = Swarm(None, None, [boid1, boid2])

        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1])

    def test_calculate_neighbour_wrap_xy(self):
        """Test boids being neighbours that wrap around the x an y axis at the same time."""
        neighbour_radius = 5
        grid_size = 20
        boid1 = Boid(neighbour_radius, grid_size, np.array([1, 19]))
        boid2 = Boid(neighbour_radius, grid_size, np.array([19, 1]))
        swarm = Swarm(None, None, [boid1, boid2])

        neighbours1 = boid1._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours1, [boid2])

        neighbours2 = boid2._calculate_neighbours(swarm)
        self.assertNeighboursEqual(neighbours2, [boid1])

    def test_collision_avoidance_acceleration_x_axis(self):
        """Test the collision avoidance is in the opposing direction to a neighbour on the x-axis."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(neighbour_radius, grid_size, np.array([5, y_position]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([10, y_position]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        self.assertLess(updated_position[0], boid.position[0])
        self.assertEqual(updated_position[1], boid.position[1])

    def test_collision_avoidance_acceleration_x_axis_negative(self):
        """Test the collision avoidance is in the opposing direction to a neighbour that has been transposed and have a negative x value."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(neighbour_radius, grid_size, np.array([4, y_position]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([-1, y_position]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        self.assertGreater(updated_position[0], boid.position[0])
        self.assertEqual(updated_position[1], boid.position[1])

    def test_collision_avoidance_acceleration_y_axis(self):
        """Test the collision avoidance is in the opposing direction to a neighbour on the y-axis."""
        neighbour_radius = 5
        grid_size = 20
        x_position = 10
        boid = Boid(neighbour_radius, grid_size, np.array([x_position, 5]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([x_position, 10]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        self.assertEqual(updated_position[0], boid.position[0])
        self.assertLess(updated_position[1], boid.position[1])

    def test_collision_avoidance_acceleration_y_axis_negative(self):
        """Test the collision avoidance is in the opposing direction to a neighbour on the other side of the y-axis."""
        neighbour_radius = 5
        grid_size = 20
        x_position = 10
        boid = Boid(neighbour_radius, grid_size, np.array([x_position, 4]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([x_position, -1]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        self.assertEqual(updated_position[0], boid.position[0])
        self.assertGreater(updated_position[1], boid.position[1])

    def test_collision_avoidance_acceleration_xy(self):
        """Test the collision avoidance is in the opposing direction to a neighbour."""
        neighbour_radius = 6
        grid_size = 20
        boid = Boid(neighbour_radius, grid_size, np.array([8, 12]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([12, 8]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        original_distance_to_neighbour = np.linalg.norm(
            neighbour.position - boid.position
        )
        updated_distance_to_neighbour = np.linalg.norm(
            neighbour.position - updated_position
        )
        self.assertGreater(
            updated_distance_to_neighbour, original_distance_to_neighbour
        )

    def test_collision_avoidance_acceleration_xy_negative(self):
        """Test the collision avoidance is in the opposing direction to a neighbour wrapping around the edge."""
        neighbour_radius = 6
        grid_size = 20
        boid = Boid(neighbour_radius, grid_size, np.array([2, 18]))
        neighbour = Boid(neighbour_radius, grid_size, np.array([-2, 22]))

        collision_avoidance_acceleration = boid._collision_avoidance_acceleration(
            [neighbour]
        )
        updated_position = boid.position + collision_avoidance_acceleration
        original_distance_to_neighbour = np.linalg.norm(
            neighbour.position - boid.position
        )
        updated_distance_to_neighbour = np.linalg.norm(
            neighbour.position - updated_position
        )
        self.assertGreater(
            updated_distance_to_neighbour, original_distance_to_neighbour
        )

    def test_velocity_matching_acceleration_x_axis(self):
        """Test the velocity matching makes the velocity of this boid closer to a neighbour."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([5, y_position]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([10, y_position]),
            initial_velocity=np.array([2, 2]),
        )

        velocity_matching_acceleration = boid._velocity_matching_acceleration(
            [neighbour]
        )

        starting_velocity_difference = neighbour.velocity - boid.velocity
        updated_velocity_difference = neighbour.velocity - (
            boid.velocity + velocity_matching_acceleration
        )
        np.testing.assert_array_less(
            updated_velocity_difference, starting_velocity_difference
        )

    def test_velocity_matching_acceleration_y_axis(self):
        """Test the velocity matching makes the velocity of this boid closer to a neighbour."""
        neighbour_radius = 5
        grid_size = 20
        x_position = 10
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([x_position, 5]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([x_position, 10]),
            initial_velocity=np.array([2, 2]),
        )

        velocity_matching_acceleration = boid._velocity_matching_acceleration(
            [neighbour]
        )

        starting_velocity_difference = neighbour.velocity - boid.velocity
        updated_velocity_difference = neighbour.velocity - (
            boid.velocity + velocity_matching_acceleration
        )
        np.testing.assert_array_less(
            updated_velocity_difference, starting_velocity_difference
        )

    def test_velocity_matching_acceleration_xy(self):
        """Test the velocity matching makes the velocity of this boid closer to a neighbour."""
        neighbour_radius = 6
        grid_size = 20
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([8, 12]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([12, 8]),
            initial_velocity=np.array([2, 2]),
        )

        velocity_matching_acceleration = boid._velocity_matching_acceleration(
            [neighbour]
        )

        starting_velocity_difference = neighbour.velocity - boid.velocity
        updated_velocity_difference = neighbour.velocity - (
            boid.velocity + velocity_matching_acceleration
        )
        np.testing.assert_array_less(
            updated_velocity_difference, starting_velocity_difference
        )

    def test_flock_centering_acceleration_x_axis(self):
        """Test the flock centering moves towards a neighbour on the x-axis."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([5, y_position]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([10, y_position]),
            initial_velocity=np.array([2, 2]),
        )

        flock_centering_acceleration = boid._flock_centering_acceleration([neighbour])
        updated_position = boid.position + flock_centering_acceleration

        self.assertGreater(updated_position[0], boid.position[0])
        self.assertEqual(updated_position[1], boid.position[1])

    def test_flock_centering_acceleration_x_axis(self):
        """Test the flock centering moves towards a neighbour on the x-axis."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([5, y_position]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([10, y_position]),
            initial_velocity=np.array([2, 2]),
        )

        flock_centering_acceleration = boid._flock_centering_acceleration([neighbour])
        updated_position = boid.position + flock_centering_acceleration

        self.assertGreater(updated_position[0], boid.position[0])
        self.assertEqual(updated_position[1], boid.position[1])

    def test_flock_centering_x_axis_negative(self):
        """Test the flock centering moves towards a neighbour on the x-axis."""
        neighbour_radius = 5
        grid_size = 20
        y_position = 10
        boid = Boid(
            neighbour_radius,
            grid_size,
            np.array([4, y_position]),
            initial_velocity=np.array([1, 1]),
        )
        neighbour = Boid(
            neighbour_radius,
            grid_size,
            np.array([-1, y_position]),
            initial_velocity=np.array([2, 2]),
        )

        flock_centering_acceleration = boid._flock_centering_acceleration([neighbour])
        updated_position = boid.position + flock_centering_acceleration

        self.assertLess(updated_position[0], boid.position[0])
        self.assertEqual(updated_position[1], boid.position[1])

    def assertNeighboursEqual(self, neighbours, boids):
        neighbours_positions = list(
            map(lambda neighbour: neighbour.position, neighbours)
        )
        boids_positions = list(map(lambda boid: boid.position, boids))
        np.testing.assert_equal(neighbours_positions, boids_positions)
