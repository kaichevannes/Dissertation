import unittest
from entity_factory.entity_factory import EntityFactory
from mock_classes import MockEntityFactory, MockEntity
import numpy as np


class TestEntityFactory(unittest.TestCase):
    """Test class to test the base entity factory."""

    def test_generate_random_coordinates_lbi(self) -> None:
        """Test the lower invalid boundary on generating random coordinates (<1)"""
        entity_factory = EntityFactory(0)
        with self.assertRaises(ValueError):
            entity_factory._generate_random_coordinates()

    def test_generate_random_coordinates_lbv(self) -> None:
        """Test the lower valid boundary on generating random coordinates (1)"""
        entity_factory = EntityFactory(1)
        coords = entity_factory._generate_random_coordinates()
        np.testing.assert_equal(coords, np.array([0, 0]))

    def test_generate_random_coordaintes_v(self) -> None:
        """Test the valid interval on generating random coordiantes (>1)."""
        entity_factory = EntityFactory(5)
        coords = entity_factory._generate_random_coordinates()
        self.assertGreaterEqual(coords[0], 0)
        self.assertLessEqual(coords[0], 5)
        self.assertGreaterEqual(coords[1], 0)
        self.assertLessEqual(coords[1], 5)

    def test_generate_entity(self) -> None:
        """Test that the base entity class required implementation."""
        entity_factory = EntityFactory(5)
        with self.assertRaises(NotImplementedError):
            entity_factory.create_entity()

    def test_mock_generate_entity(self) -> None:
        """Test the the mock entity class creates a mock entity."""
        mock_entity_factory = MockEntityFactory(5)
        mock_entity = mock_entity_factory.create_entity()
        self.assertEqual(type(mock_entity), MockEntity)
