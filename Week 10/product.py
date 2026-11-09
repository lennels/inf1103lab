from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product.

    A product must be either physical or digital, so Product itself
    cannot be created directly. Subclasses must implement
    get_fulfilment_info().

    Every product keeps a reference to the Supplier that supplies it
    (association). The Supplier is created elsewhere and passed in.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier,
                 transaction_history: list[int] | None = None):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier
        if transaction_history is None:
            transaction_history = [self.__stock]
        self.__transaction_history: list[int] = list(transaction_history)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_transaction_history(self) -> list[int]:
        return list(self.__transaction_history)

    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new quantity and record the change.

        Contract every subclass must keep (LSP): any quantity >= 0 is
        accepted, get_stock() returns it afterwards, the change is
        recorded, and negative quantities raise ValueError.
        """
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__transaction_history.append(quantity - self.__stock)
        self.__stock = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return how this product reaches the customer."""

    def display_information(self) -> None:
        """Print the information every product has.

        Subclasses override this, call super().display_information()
        and then print their own extra details.
        """
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.get_name()} "
              f"({self.__supplier.get_contact_email()})")

    def to_dict(self) -> dict:
        """Return the common fields as a dict for saving to JSON.

        The supplier is saved by ID only; the supplier's own details
        are saved once in the file's supplier list.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
            "transaction_history": self.get_transaction_history(),
        }

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
                f"Supplier: {self.__supplier.get_name()}")
