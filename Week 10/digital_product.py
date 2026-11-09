from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product that is delivered through a download link.

    It does NOT implement CanBeShipped, because nothing is shipped.
    Stock here means the number of licences available, so it keeps the
    same update_stock() behaviour as every other Product (LSP).
    """

    TYPE = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float,
                 transaction_history: list[int] | None = None):
        super().__init__(product_id, name, price, stock, supplier,
                         transaction_history)
        if float(download_size) < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via a download link."

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    def __str__(self) -> str:
        return f"{super().__str__()} | Download: {self.__download_size:.2f} MB"
