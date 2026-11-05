import json
from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct


class InventoryFile:
    """Loads and saves an Inventory to a JSON file.

    Each saved product has a "type" ("physical" or "digital") so the
    right subclass can be rebuilt when the file is loaded.
    """

    def __init__(self, file_name):
        self.__file_name = file_name

    def get_file_name(self):
        return self.__file_name

    def load(self):
        inventory = Inventory()

        # Missing file -> start with an empty inventory, no error
        if not Path(self.__file_name).exists():
            print(f"{self.__file_name} not found.")
            print("Starting with an empty inventory.")
            return inventory

        print(f"{self.__file_name} found.")
        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"{self.__file_name} is not valid JSON. Starting with an empty inventory.")
            return inventory

        for item in data:
            try:
                product = self.__create_product(item)
            except (KeyError, ValueError) as error:
                print(f"Skipping invalid product {item.get('id', '?')}: {error}")
                continue
            inventory.add_product(product)

        print("Inventory loaded successfully.")
        return inventory

    def __create_product(self, item):
        """Use the saved "type" to build the matching subclass."""
        product_type = item.get("type")
        if product_type == PhysicalProduct.TYPE:
            return PhysicalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                item["weight"], item.get("transaction_history"),
            )
        if product_type == DigitalProduct.TYPE:
            return DigitalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                item["download_size"], item.get("transaction_history"),
            )
        raise ValueError(f"unknown product type '{product_type}'")

    def save(self, inventory):
        # Each product knows how to turn itself into a dict
        data = [product.to_dict() for product in inventory.get_products()]
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
