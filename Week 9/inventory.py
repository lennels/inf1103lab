LINE = "-" * 48


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if its ID is already used."""
        if self.search_product(product.get_product_id()):
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def get_products(self):
        # Return a copy so callers can't add/remove products directly
        return list(self.__products)

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            print(product)
        print(LINE)
