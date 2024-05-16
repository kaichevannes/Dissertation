from swarm.swarm import Swarm
from entity.entity import Entity


class OrderParameter:
    """The order parameter class is a base class for implementing order parameters.
    Each order parameter class will represent a specific order parameter and will
    be constructed using a swarm. It will then have some kind of calculate method
    and will return the order parameters value at that time step. Perhaps some
    kind of history mechanism could also be implemented."""

    def set_swarm(self, swarm: Swarm) -> None:
        """Set this order parameters swarm.

        Args:
            swarm (Swarm): the swarm that this order parameter will measure
        """
        self.swarm = swarm

    def get_name(self) -> str:
        """Get the name of this order parameter

        Raises:
            NotImplementedError: if not implemented
        """
        raise NotImplementedError

    def calculate(self, entities: list[Entity]) -> float:
        """Calculate this order parameter on the current state of the swarm.

        Raises:
            NotImplementedError: if not implemented, must be implemented in all subclasses

        Returns:
            float: a value between 0 and 1 for this order parameter
        """
        raise NotImplementedError

    def calculate_normal(self) -> float:
        """Calculate this order parameter for the unoverriden swarm members only.

        Returns:
            float: a value between 0 and 1 for this order parameter
        """
        from order_parameter.rotation import Rotation

        non_override_entities = []
        for entity in self.swarm.entities:
            if entity.override_fraction == 0:
                non_override_entities.append(entity)

        if isinstance(self, Rotation):
            if len(non_override_entities) == len(self.swarm.entities):
                return None

        if len(non_override_entities) > 0:
            return self.calculate(non_override_entities)
        else:
            return None

    def calculate_overriden(self) -> float:
        """Calculate this order parameter for the overriden swarm members only.

        Returns:
            float: a value between 0 and 1 for this order parameter
        """
        overriden_entities = []
        for entity in self.swarm.entities:
            if entity.override_fraction > 0:
                overriden_entities.append(entity)

        if len(overriden_entities) > 0:
            return self.calculate(overriden_entities)
        else:
            return None

    def calculate_combined(self) -> float:
        """Calculate this order parameter for both overriden and normal swarm members.

        Returns:
            float: a value between 0 and 1 for this order parameter
        """
        return self.calculate(self.swarm.entities)
