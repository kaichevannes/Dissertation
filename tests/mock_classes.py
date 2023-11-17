from entity.entity import Entity
from entity_factory.entity_factory import EntityFactory
from swarm.swarm import Swarm
import numpy as np


class MockEntity(Entity):
    """A concrete mock entity for testing purposes."""

    def update_position(self, _: Swarm) -> None:
        """Update the position of this mock entity.

        Args:
            _ (Swarm): the test swarm, not used in calculation
        """
        self.position += 1


class MockEntityFactory(EntityFactory):
    """A concrete mock entity factory for testing purposes."""

    def create_entity(self) -> MockEntity:
        return MockEntity(self.grid_size, np.array([0, 0]))
