from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for every product.

    A product must be either physical or digital, so Product itself
    cannot be created directly. Subclasses must implement
    get_fulfilment_info().
    """

    def __init__(self, product_id, name, price, stock, transaction_history=None):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)
        if transaction_history is None:
            transaction_history = [self.__stock]
        self.__transaction_history = list(transaction_history)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_transaction_history(self):
        return list(self.__transaction_history)

    def update_stock(self, quantity):
        """Set the stock to a new quantity and record the change."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__transaction_history.append(quantity - self.__stock)
        self.__stock = quantity

    @abstractmethod
    def get_fulfilment_info(self):
        """Return how this product reaches the customer."""

    def display_information(self):
        """Print the information every product has.

        Subclasses override this, call super().display_information()
        and then print their own extra details.
        """
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def to_dict(self):
        """Return the common fields as a dict for saving to JSON.

        Subclasses override this to add their type and extra fields.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "transaction_history": self.get_transaction_history(),
        }

    def __str__(self):
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
