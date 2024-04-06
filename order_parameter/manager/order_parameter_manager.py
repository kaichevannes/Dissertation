from order_parameter.order_parameter import OrderParameter
from swarm.swarm import Swarm


class OrderParameterManager:
    """The order parameter manager class is used to organise multiple order parameters to be measured during a simulation."""

    def __init__(self):
        self.order_parameters = []

    def add_order_parameter(self, order_parameter_to_add: OrderParameter):
        """Add an order parameter to this manager.

        Args:
            order_parameter (OrderParameter): an order parameter

        Raises:
            ValueError: if this order parameter has already been added
        """
        # for existing_order_parameter in self.order_parameters:
        #     if isinstance(existing_order_parameter, order_parameter_to_add):
        #         raise ValueError(
        #             f"Cannot add another order parameter of type {type(order_parameter_to_add)}"
        #         )
        #     else:
        self.order_parameters.append(order_parameter_to_add)

    def set_swarm(self, swarm: Swarm):
        """Set the swarm for this order parameter manager.

        Args:
            swarm (Swarm): the swarm that will be evaluated
        """
        for order_parameter in self.order_parameters:
            order_parameter.set_swarm(swarm)
