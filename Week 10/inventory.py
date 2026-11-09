from product import Product

LINE = "-" * 48


class Inventory:
    """Aggregation: an Inventory groups Product objects it does not own.

    Products are created outside the inventory and passed in. Removing
    a product only drops the inventory's reference; the Product object
    itself keeps working and can be added to another inventory.

    Every method works with the Product type only, so any subclass
    (physical, digital or a future one) can be stored (LSP).
    """

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing product. Returns False if its ID is already used."""
        if self.find_product(product.get_product_id()):
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the product's reference and return the product, or None.

        The returned Product is not destroyed, so it can be reused.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def get_products(self) -> list[Product]:
        # Return a copy so callers can't add/remove products directly
        return list(self.__products)

    def display_all_products(self) -> None:
        """Ask every product to display itself (polymorphism).

        No isinstance() checks: each object runs its own version of
        display_information() and get_fulfilment_info().
        """
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print(LINE)
