from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style ABC: anything that can be shipped.

    It only states WHAT a shippable object must be able to do.
    It holds no attributes and no shipping logic of its own.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost in dollars."""
