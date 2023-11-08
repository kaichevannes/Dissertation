from entity_factory.entity_factory import EntityFactory
from entity.boid import Boid


class BoidFactory(EntityFactory):
    """A factory for boids, instantiated with a constant velocity with the start time starting at zero."""

    def __init__(self, grid_size: int, neighbour_radius: int):
        """
        Args:
            grid_size (int): The size of the simulation grid
            neighbour_radius (int): The radius where a boid recognises neighbours
        """
        super().__init__(grid_size=grid_size)
        self.neighbour_radius = neighbour_radius

    def create_entity(self) -> Boid:
        return Boid(
            neighbour_radius=self.neighbour_radius,
            grid_size=self.grid_size,
            initial_position=self.generate_random_coordinates(),
        )
