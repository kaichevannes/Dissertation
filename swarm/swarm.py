from entity_factory.entity_factory import EntityFactory
import matplotlib.pyplot as plt
import numpy as np


class Swarm:
    """A swarm of entities."""

    def __str__(self) -> str:
        """Convert this swarm into a human-readable string.

        Returns:
            str: a string representation of this swarm
        """
        if self.entities is None:
            return "This swarm has no entities, generate them with swarm.generate_entities()."

        full_string = ""
        num_entities = len(self.entities)
        for i in range(num_entities):
            full_string += "Entity #{:{width}}: {}\n".format(
                i + 1,
                self.entities[i],
                width=len(str(num_entities)),
            )

        return full_string

    def __init__(self, swarm_size: int, entity_factory: EntityFactory) -> None:
        """
        Args:
            swarm_size (int): the number of entities in the swarm
            entity_factory (EntityFactory): the factory used to create the swarm entities
        """
        self.swarm_size = swarm_size
        self.entity_factory = entity_factory
        self.entities = None

    # def __init__(
    #     self, swarm_size: int, entity_factory: EntityFactory, axes: plt.axes
    # ) -> None:
    #     """
    #     Args:
    #         swarm_size (int): the number of entities in the swarm
    #         entity_factory (EntityFactory): the factory used to create the swarm entities
    #         axis (plt.axes): the plot to show the simulation on
    #     """
    #     self.swarm_size = swarm_size
    #     self.entity_factory = entity_factory
    #     self.entities = None
    #     self.axes = axes

    def generate_entities(self) -> None:
        """Generate a new swarm based on the initialisation parameters."""
        self.entities = [
            self.entity_factory.create_entity() for _ in range(self.swarm_size)
        ]

    def step(self) -> None:
        """Update by one time step."""
        for entity in self.entities:
            entity.update_position(self)

    def initialise_plot(self, ax: plt.Axes) -> None:
        self.step()
        x_positions = [entity.position[0] for entity in self.entities]
        y_positions = [entity.position[1] for entity in self.entities]
        self.sc = ax.scatter(x_positions, y_positions)

    def plot(self, ax: plt.Axes) -> None:
        self.step()
        print(self)
        x_positions = [entity.position[0] for entity in self.entities]
        y_positions = [entity.position[1] for entity in self.entities]
        self.sc.set_offsets(np.c_[x_positions, y_positions])
