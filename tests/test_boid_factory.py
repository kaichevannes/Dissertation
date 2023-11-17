import unittest
from entity_factory.boid_factory import BoidFactory
from entity.boid.boid import Boid
import numpy as np


class TestBoidFactory(unittest.TestCase):
    """Test a concrete boid factory."""

    def test_constructor(self) -> None:
        """Test that the constructor properly assigns values."""
        boid_factory = BoidFactory(20, 5)
        self.assertEqual(boid_factory.grid_size, 20)
        self.assertEqual(boid_factory.neighbour_radius, 5)

    def test_create_entity(self) -> None:
        """Test that a boid factory creates boids."""
        boid_factory = BoidFactory(20, 5)
        boid = boid_factory.create_entity()
        self.assertEqual(type(boid), Boid)

    def test_boid_attributes(self) -> None:
        """Test that the boid is assigned the correct values."""
        boid_factory = BoidFactory(1, 5)
        boid = boid_factory.create_entity()
        self.assertEqual(boid._grid_size, 1)
        self.assertEqual(boid._neighbour_radius, 5)
        np.testing.assert_equal(boid.position, np.array([0, 0]))
