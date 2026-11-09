from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    """A product that has weight and is shipped to the customer.

    Inherits from one class (Product) and implements one
    interface (CanBeShipped).
    """

    TYPE = "physical"
    BASE_SHIPPING_FEE = 5.00 
    RATE_PER_KG = 2.00        

    def __init__(self, product_id, name, price, stock, weight,
                 transaction_history=None):
        super().__init__(product_id, name, price, stock, transaction_history)
        if float(weight) < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Flat fee plus a charge for every kilogram."""
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"
