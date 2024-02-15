import numpy as np
import networkx as nx
from order_parameter.order_parameter import OrderParameter


class NumberOfGroups(OrderParameter):
    """The number of groups order parameter simply tells us how many distinct clusters
    of boids there are at any given time."""

    def calculate(self) -> float:
        """Calculate the number of groups order parameter for the swarm at it's current state.

        Returns:
            float: how clustered the swarm is from 0 to 1
        """
        # Used by Harvey et al. in Application of chaos measures to a simplified boids flocking model
        entities = self.swarm.entities
        graph = nx.Graph()
        graph.add_nodes_from(entities)

        for entity in entities:
            for possible_neighbour in entities:
                if entity == possible_neighbour:
                    continue
                dist = np.linalg.norm(possible_neighbour.position - entity.position)
                if (
                    min(dist, entity._grid_size - dist)
                    < entity._collision_avoidance_radius
                ):
                    graph.add_edge(entity, possible_neighbour)

        # now we have a graph of boids and edges.
        self.graph = graph
        groups = nx.connected_components(graph)
        num_groups = 0
        for _ in groups:
            num_groups += 1
        return num_groups
