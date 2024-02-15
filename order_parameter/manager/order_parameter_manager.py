from order_parameter.order_parameter import OrderParameter


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
        for existing_order_parameter in self.order_parameters:
            if isinstance(existing_order_parameter, order_parameter_to_add):
                raise ValueError(
                    f"Cannot add another order parameter of type {type(order_parameter_to_add)}"
                )

        self.order_parameters.append(order_parameter_to_add)

    def evaluate_all(self) -> dict[str, float]:
        """Evaluate all of the order parameters that this class is managing.

        Returns:
            dict[str, float]: a dictionary of type to evaluation value
        """
        result = {}
        for order_parameter in self.order_parameters:
            result[type(order_parameter)] = order_parameter.evaluate()
        return result
