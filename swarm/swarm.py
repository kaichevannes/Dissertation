from entity_factory.entity_factory import EntityFactory
from entity.entity import Entity
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
import numpy as np
import math


class Swarm:
    """A swarm of entities."""

    def __init__(
        self,
        swarm_size: int,
        entity_factory: EntityFactory,
        entities: list[Entity] = None,
    ) -> None:
        """
        Args:
            swarm_size (int): the number of entities in the swarm
            entity_factory (EntityFactory): the factory used to create the swarm entities
            entities (Entity): a pre-instantiated list of entities to start the swarm with
        """
        if entities is None:
            self.swarm_size = swarm_size
            self.entity_factory = entity_factory
        self.entities = entities

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

    def generate_entities(self) -> None:
        """Generate a new swarm based on the initialisation parameters."""
        if self.swarm_size < 0:
            raise ValueError("Swarm size must be non-negative.")
        self.entities = [
            self.entity_factory.create_entity() for _ in range(self.swarm_size)
        ]

    def calculate_visceks_order_parameter(self) -> float:
        """Calculate the Visceks order parameter at this time step.

        Returns:
            float: the Visceks order parameter at this time step
        """
        total_normalised_velocity = np.array([0, 0])
        for entity in self.entities:
            normalised_velocity = entity.velocity / np.linalg.norm(entity.velocity)
            total_normalised_velocity = np.add(
                total_normalised_velocity,
                normalised_velocity,
            )

        return np.linalg.norm(total_normalised_velocity) / len(self.entities)

    def step(self) -> None:
        """Update by one time step."""
        for entity in self.entities:
            entity.update_position(self)

    def initialise_plot(self, ax: plt.Axes) -> None:
        """Initialise the plot when visualising.

        Args:
            ax (plt.Axes): the axes to plot on
        """
        self.step()
        print(self)
        positions = np.array([entity.position for entity in self.entities])

        self.sc = ax.scatter(positions[:, 0], positions[:, 1], c="black", s=250)
        self.ax = ax

        self.update_markers()

    def update_plot(self, frame: int) -> None:
        """Update the plot

        Args:
            frame (int): the number of the frame this plot is currently on
        """
        self.step()
        print(self)
        positions = np.array([entity.position for entity in self.entities])

        self.sc.set_offsets(np.c_[positions[:, 0], positions[:, 1]])
        self.ax.set_title(f"t = {frame}")

        self.update_markers()

    def update_markers(self):
        """Update the markers for the graph at this time step."""
        markers = [self.generate_arrow_marker(entity) for entity in self.entities]

        # Update markers
        paths = []

        for marker in markers:
            marker_obj = MarkerStyle(marker)
            path = marker_obj.get_path().transformed(marker_obj.get_transform())
            paths.append(path)

        self.sc.set_paths(paths)

    def generate_arrow_marker(self, entity: Entity) -> Path:
        """Generate an arrow marker for an entity, pointing in the same direction as that entity. Adapted from https://stackoverflow.com/a/66973317

        Args:
            entity (Entity): the entity to generate the marker for

        Returns:
            Path: the path representation of the marker
        """
        velocity = entity.velocity
        theta = math.atan2(velocity[1], velocity[0])

        arrow_shape = np.array(
            [[0.1, 0.3], [0.1, -0.3], [1, 0], [0.1, 0.3]]
        )  # arrow shape
        # arrow_shape = np.array([[0.3, 0.3], [0.3, -0.3], [1, 0], [0.3, 0.3]])

        rotation_matrix = np.array(
            [[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]]
        )
        arrow_shape = np.matmul(arrow_shape, rotation_matrix)  # rotates the arrow
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
        arrow_head_marker = Path(arrow_shape, codes)

        return arrow_head_marker
