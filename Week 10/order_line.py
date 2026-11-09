from product import Product


class OrderLine:
    """One product and the quantity of it requested in an Order.

    An OrderLine is only created by Order.add_order_line() and belongs
    to exactly one Order (composition). It refers to a Product but does
    not own it: the Product can also sit in an Inventory or other orders.
    """

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = int(quantity)

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def __str__(self) -> str:
        return (f"{self.__product.get_product_id()} {self.__product.get_name()} "
                f"x {self.__quantity} @ ${self.__product.get_price():.2f} "
                f"= ${self.calculate_subtotal():.2f}")
