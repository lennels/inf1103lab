from product import Product


class DigitalProduct(Product):
    """A product that is delivered through a download link.

    It does NOT implement CanBeShipped, because nothing is shipped.
    """

    TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size,
                 transaction_history=None):
        super().__init__(product_id, name, price, stock, transaction_history)
        if float(download_size) < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "This product is delivered digitally via a download link."

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    def __str__(self):
        return f"{super().__str__()} | Download: {self.__download_size:.2f} MB"
