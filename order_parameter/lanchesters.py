import numpy as np
import networkx as nx
from order_parameter.order_parameter import OrderParameter


class Lanchesters(OrderParameter):
    """The Lanchesters index is a measure of how clustered a swarm is, this means
    how close to one another each swarm member is within a group."""

    def calculate(self) -> float:
        """Calculate the Lanchesters order parameter for the swarm at it's current state.

        Returns:
            float: how clustered the swarm is from 0 to 1
        """
        # From Zhang
        entities = self.swarm.entities
        graph = nx.Graph()
        graph.add_nodes_from(entities)

        for entity in entities:
            for possible_neighbour in entities:
                if entity == possible_neighbour:
                    continue
                dist = np.linalg.norm(possible_neighbour.position - entity.position)
                if min(dist, entity._grid_size - dist) < (
                    entity._collision_avoidance_radius
                ):  # multiplied by the swarm density
                    graph.add_edge(entity, possible_neighbour)

        # now we have a graph of boids and edges.
        groups = nx.connected_components(graph)

        group_sizes_squared = 0
        for group in groups:
            group_sizes_squared += len(group) ** 2

        lanchesters_index = (1 / len(entities) ** 2) * group_sizes_squared
        return lanchesters_index

    def get_name(self) -> str:
        return "lanchesters"
