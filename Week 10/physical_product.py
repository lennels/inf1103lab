from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that has weight and is shipped to the customer.

    Inherits from one class (Product) and implements one
    interface (CanBeShipped).
    """

    TYPE = "physical"
    BASE_SHIPPING_FEE = 5.00
    RATE_PER_KG = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float,
                 transaction_history: list[int] | None = None):
        super().__init__(product_id, name, price, stock, supplier,
                         transaction_history)
        if float(weight) < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Flat fee plus a charge for every kilogram."""
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    def __str__(self) -> str:
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"
