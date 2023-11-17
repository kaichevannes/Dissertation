import unittest
from entity.entity import Entity
from swarm.swarm import Swarm
import numpy as np


class TestEntity(unittest.TestCase):
    """Test the base Entity abstract class."""

    swarm = None
    GRID_SIZE = 20
    INITIAL_POSITION = np.array([0, 0])

    def test_update_position_is_abstract(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.entity1.update_position(self.swarm)

    def test_values_correctly_set(self) -> None:
        grid_size = 1
        position = np.array([2, 3])
        velocity = np.array([4, 5])
        acceleration = np.array([6, 7])
        time_step = 8
        full_entity = Entity(
            grid_size=grid_size,
            initial_position=position,
            initial_velocity=velocity,
            initial_acceleration=acceleration,
            initial_time_step=time_step,
        )

        self.assertEqual(full_entity._grid_size, grid_size)
        np.testing.assert_equal(full_entity.position, position)
        np.testing.assert_equal(full_entity.velocity, velocity)
        np.testing.assert_equal(full_entity.acceleration, acceleration)
        self.assertEqual(full_entity.positions, [])

    def test_str_special_method(self) -> None:
        self.assertEqual(
            self.entity1.__str__().replace(" ", ""),
            "[ENTITY]|p(3,2)|v(0,0)|a(0,0)|t0|",
        )

    def setUp(self) -> None:
        self.entity1 = Entity(self.GRID_SIZE, np.array([3, 2]))
        self.entity2 = Entity(self.GRID_SIZE, np.array([9, 16]))
        self.entity3 = Entity(self.GRID_SIZE, np.array([18, 6]))
        entities = [self.entity1, self.entity2, self.entity3]
        self.swarm = Swarm(None, None, entities=entities)
