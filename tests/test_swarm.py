import unittest
from tests.mock_classes import MockEntity, MockEntityFactory
from swarm.swarm import Swarm
import numpy as np


class TestSwarm(unittest.TestCase):
    """Test a swarm of base Entities."""

    swarm = None
    GRID_SIZE = 20
    INITIAL_POSITION = np.array([0, 0])

    def test_manual_entities(self) -> None:
        """Check that the entities we provide a swarm with are the same ones that it stores when manually instantiating."""
        self.assertCountEqual(self.entities, self.swarm.entities)

    def test_pre_step(self) -> None:
        """Test that the positions of the entities before we step are the positions we expect."""
        np.testing.assert_equal(self.entity1.position, np.array([3, 2]))
        np.testing.assert_equal(self.entity2.position, np.array([9, 16]))
        np.testing.assert_equal(self.entity3.position, np.array([18, 6]))

    def test_step(self) -> None:
        """Check that stepping updates the position of each entity."""
        self.swarm.step()
        np.testing.assert_equal(self.entity1.position, np.array([4, 3]))
        np.testing.assert_equal(self.entity2.position, np.array([10, 17]))
        np.testing.assert_equal(self.entity3.position, np.array([19, 7]))

    def test_generate_entities_lbv(self) -> None:
        """Check the lower valid boundary on generating entities through a swarm object."""
        mock_entity_factory = MockEntityFactory(20)
        swarm = Swarm(0, mock_entity_factory)
        swarm.generate_entities()
        self.assertEqual(len(swarm.entities), 0)

    def test_generate_entities_lbi(self) -> None:
        """Check the lower invalid boundary on generating entities through a swarm object."""
        mock_entity_factory = MockEntityFactory(20)
        swarm = Swarm(-1, mock_entity_factory)
        with self.assertRaises(ValueError):
            swarm.generate_entities()

    def test_generate_entities_v(self) -> None:
        """Check the valid interval on generating entities through a swarm object."""
        mock_entity_factory = MockEntityFactory(20)
        swarm = Swarm(5, mock_entity_factory)
        swarm.generate_entities()
        self.assertEqual(len(swarm.entities), 5)
        for entity in swarm.entities:
            self.assertEqual(type(entity), MockEntity)

    def test_str_special_method(self) -> None:
        """Test the string special method."""
        lines = self.swarm.__str__().replace(" ", "").split("\n")
        self.assertEqual(lines[0], "Entity#1:[MOCKENTITY]|p(3,2)|v(0,0)|a(0,0)|t0|")
        self.assertEqual(lines[1], "Entity#2:[MOCKENTITY]|p(9,16)|v(0,0)|a(0,0)|t0|")
        self.assertEqual(lines[2], "Entity#3:[MOCKENTITY]|p(18,6)|v(0,0)|a(0,0)|t0|")

    def setUp(self) -> None:
        self.entity1 = MockEntity(self.GRID_SIZE, np.array([3, 2]))
        self.entity2 = MockEntity(self.GRID_SIZE, np.array([9, 16]))
        self.entity3 = MockEntity(self.GRID_SIZE, np.array([18, 6]))
        self.entities = [self.entity1, self.entity2, self.entity3]
        self.swarm = Swarm(None, None, entities=self.entities)
