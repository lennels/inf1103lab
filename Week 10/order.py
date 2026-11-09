from order_line import OrderLine
from product import Product

LINE = "-" * 48


class Order:
    """Composition: an Order creates and owns its OrderLine objects.

    Order lines are only made inside add_order_line(), are never passed
    in from outside, and are never handed to another Order. When an
    Order is discarded, its order lines go with it.
    """

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        # A tuple so callers can read the lines but not add or remove them
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and keep it."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Delete the line for this product. Returns False if not found."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        """Add up the subtotal of every order line."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(LINE)
        if not self.__order_lines:
            print("No order lines.")
        for order_line in self.__order_lines:
            print(order_line)
        print(LINE)
        print(f"Total: ${self.calculate_total():.2f}")
