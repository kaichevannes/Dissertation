from entity.factory.entity_factory import EntityFactory
from entity.entity import Entity
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
import numpy as np
import networkx as nx
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

    # TODO: Refactor disgusting constructor with this factory method instead
    @classmethod
    def from_entities(cls, entities: list[Entity]):
        swarm = Swarm(None, None)
        swarm.entities = entities
        return swarm

    def generate_entities(self) -> None:
        """Generate a new swarm based on the initialisation parameters."""
        if self.swarm_size < 0:
            raise ValueError("Swarm size must be non-negative.")
        self.entities = [
            self.entity_factory.create_entity() for _ in range(self.swarm_size)
        ]

    # TODO: Remove below code once refactored

    # def calculate_visceks_order_parameter(self) -> float:
    #     """Calculate the Visceks order parameter at this time step.

    #     Returns:
    #         float: the Visceks order parameter at this time step
    #     """
    #     # from viscek, quoted from Harvey et al
    #     total_normalised_velocity = np.array([0, 0])
    #     for entity in self.entities:
    #         if np.linalg.norm(entity.velocity) == 0:
    #             continue
    #         normalised_velocity = entity.velocity / np.linalg.norm(entity.velocity)
    #         total_normalised_velocity = np.add(
    #             total_normalised_velocity,
    #             normalised_velocity,
    #         )

    #     return np.linalg.norm(total_normalised_velocity) / len(self.entities)

    # def calculate_lanchesters_index(self) -> float:
    #     # From Zhang
    #     # if self.graph is None:
    #     graph = nx.Graph()
    #     graph.add_nodes_from(self.entities)

    #     for entity in self.entities:
    #         for possible_neighbour in self.entities:
    #             if entity == possible_neighbour:
    #                 continue
    #             dist = np.linalg.norm(possible_neighbour.position - entity.position)
    #             if min(dist, entity._grid_size - dist) < (
    #                 entity._collision_avoidance_radius
    #             ):  # multiplied by the swarm density
    #                 graph.add_edge(entity, possible_neighbour)

    #     # print(graph)
    #     # now we have a graph of boids and edges.
    #     groups = nx.connected_components(graph)

    #     group_sizes_squared = 0
    #     for group in groups:
    #         group_sizes_squared += len(group) ** 2

    #     lanchesters_index = (1 / len(self.entities) ** 2) * group_sizes_squared
    #     return lanchesters_index

    # def calculate_number_of_groups(self) -> int:
    #     # Used by Harvey et al. in Application of chaos measures to a simplified boids flocking model
    #     graph = nx.Graph()
    #     graph.add_nodes_from(self.entities)

    #     for entity in self.entities:
    #         for possible_neighbour in self.entities:
    #             if entity == possible_neighbour:
    #                 continue
    #             dist = np.linalg.norm(possible_neighbour.position - entity.position)
    #             average_radius = (
    #                 entity._flock_centering_radius
    #                 + entity._collision_avoidance_radius
    #                 + entity._velocity_matching_radius
    #             ) / 3
    #             if (
    #                 min(dist, entity._grid_size - dist)
    #                 < entity._collision_avoidance_radius
    #             ):
    #                 graph.add_edge(entity, possible_neighbour)

    #     # print(graph)
    #     # now we have a graph of boids and edges.
    #     self.graph = graph
    #     groups = nx.connected_components(graph)
    #     num_groups = 0
    #     for _ in groups:
    #         num_groups += 1
    #     return num_groups

    def calculate_rotation_order_parameter(self, t):
        z = 10
        if t == 0:
            self.velocities = []
            return None
        # if t % z != 0:
        #     time_step_velocities = []
        #     for entity in self.entities:
        #         time_step_velocities.append(entity.velocity)
        #     self.velocities.append(time_step_velocities)
        #     return None
        time_step_velocities = []
        for entity in self.entities:
            time_step_velocities.append(entity.velocity)
        self.velocities.append(time_step_velocities)

        if t < z:
            return None

        # print(self.velocities)
        total_global_velocity_difference = 0
        for entity_index in range(len(self.entities)):
            total_velocity_difference = 0
            # print("start")
            # for velocity_index in range(z - 2):
            #     velocity_k = self.velocities[velocity_index][entity_index]
            #     velocity_k_plus_1 = self.velocities[velocity_index + 1][entity_index]
            #     # print("k", velocity_k)
            #     # print("k+1", velocity_k_plus_1)
            #     total_velocity_difference += np.abs(
            #         (
            #             np.cross(velocity_k, velocity_k_plus_1)
            #             - np.cross(velocity_k_plus_1, velocity_k)
            #         )
            #         / (np.linalg.norm(velocity_k) * np.linalg.norm(velocity_k_plus_1))
            #     )
            # print("end")
            for velocity_index in range(z - 2):
                velocity_k = self.velocities[velocity_index][entity_index]
                velocity_k_plus_1 = self.velocities[velocity_index + 1][entity_index]
                # print("k", velocity_k)
                # print("k+1", velocity_k_plus_1)
                total_velocity_difference += (
                    np.cross(velocity_k, velocity_k_plus_1)
                    - np.cross(velocity_k_plus_1, velocity_k)
                ) / (np.linalg.norm(velocity_k) * np.linalg.norm(velocity_k_plus_1))
            total_global_velocity_difference += np.abs(total_velocity_difference) / z

        self.velocities = self.velocities[1:]
        return total_global_velocity_difference / len(self.entities)

    def step(self) -> None:
        """Update by one time step."""
        for entity in self.entities:
            entity.update_position(self)

    def initialise_plot(self, ax: plt.Axes) -> None:
        """Initialise the plot when visualising.

        Args:
            ax (plt.Axes): the axes to plot on
        """
        self.graph = None
        plt.rcParams.update({"font.size": 22})
        self.step()
        # print(self)
        self.velocities = []
        positions = np.array([entity.position for entity in self.entities])

        self.sc = ax.scatter(positions[:, 0], positions[:, 1], c="black", s=250)
        self.ax = ax
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_title(f"t = 0")

        # self.update_colours()

        self.update_markers()

    def update_plot(self, frame: int) -> None:
        """Update the plot

        Args:
            frame (int): the number of the frame this plot is currently on
        """
        self.step()
        # print(self)
        # print(f"Alignment = {self.calculate_visceks_order_parameter()}")
        # print(f" Num Groups = {self.calculate_number_of_groups()}")
        # print(f"Lanchesters = {self.calculate_lanchesters_index()}")
        # print(f"Rotation = {self.calculate_rotation_order_parameter(frame)}")
        positions = np.array([entity.position for entity in self.entities])

        self.sc.set_offsets(np.c_[positions[:, 0], positions[:, 1]])
        self.ax.set_title(f"t = {frame}")
        # if frame % 250 == 0:
        #     input()

        # self.update_colours()

        # print(f"boid_colours = {boid_colours}")
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

    def update_colours(self):
        if self.graph is None:
            graph = nx.Graph()
            graph.add_nodes_from(self.entities)

            for entity in self.entities:
                for possible_neighbour in self.entities:
                    if entity == possible_neighbour:
                        continue
                    dist = np.linalg.norm(possible_neighbour.position - entity.position)
                    if (
                        min(dist, entity._grid_size - dist)
                        < entity._collision_avoidance_radius
                    ):
                        graph.add_edge(entity, possible_neighbour)

            self.graph = graph

        colors = [
            "blue",
            "lightcoral",
            "orange",
            "khaki",
            "yellowgreen",
            "lime",
            "turquoise",
            "skyblue",
            "cornflowerblue",
            "mediumpurple",
            "mediumorchid",
            "violet",
            "deeppink",
            "gainsboro",
            "brown",
            "sandybrown",
            "tan",
            "beige",
            "peru",
            "lightgrey",
            "black",
            "orangered",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
        ]

        groups = [
            self.graph.subgraph(c).copy() for c in nx.connected_components(self.graph)
        ]

        boid_colours = []
        for entity in self.entities:
            # print("looking for entity")
            for i in range(len(groups)):
                # print("incrementing i")
                # print(groups[i])
                if entity in groups[i]:
                    # print("in this group")
                    boid_colours.append(colors[i])
                    break
                    # print("not in this group")

        self.sc.set_color(boid_colours)
