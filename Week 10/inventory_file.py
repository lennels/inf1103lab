import json
from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

# Used for products saved before suppliers existed (old list-only files)
UNKNOWN_SUPPLIER_ID = "SUP000"


class InventoryFile:
    """Loads and saves suppliers and an Inventory to a JSON file.

    File layout:
        {"suppliers": [...], "products": [...]}

    Each product stores its supplier's ID, so products from the same
    supplier share one Supplier object after loading. Each product also
    has a "type" ("physical" or "digital") so the right subclass is
    rebuilt.
    """

    def __init__(self, file_name: str | Path):
        self.__file_name: str | Path = file_name

    def get_file_name(self) -> str | Path:
        return self.__file_name

    def load(self) -> tuple[Inventory, list[Supplier]]:
        inventory = Inventory()
        suppliers: list[Supplier] = []

        # Missing file -> start empty, no error
        if not Path(self.__file_name).exists():
            print(f"{self.__file_name} not found.")
            print("Starting with an empty inventory.")
            return inventory, suppliers

        print(f"{self.__file_name} found.")
        try:
            with open(self.__file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"{self.__file_name} is not valid JSON. Starting with an empty inventory.")
            return inventory, suppliers

        # Older files were just a list of products
        if isinstance(data, list):
            data = {"suppliers": [], "products": data}

        suppliers_by_id: dict[str, Supplier] = {}
        for item in data.get("suppliers", []):
            try:
                supplier = Supplier(item["id"], item["name"], item["contact_email"])
            except KeyError as error:
                print(f"Skipping invalid supplier {item.get('id', '?')}: missing {error}")
                continue
            suppliers_by_id[supplier.get_supplier_id()] = supplier

        for item in data.get("products", []):
            supplier_id = item.get("supplier_id", UNKNOWN_SUPPLIER_ID)
            if supplier_id not in suppliers_by_id:
                suppliers_by_id[supplier_id] = Supplier(
                    supplier_id, "Unknown Supplier", "unknown@example.com")
            try:
                product = self.__create_product(item, suppliers_by_id[supplier_id])
            except (KeyError, ValueError) as error:
                print(f"Skipping invalid product {item.get('id', '?')}: {error}")
                continue
            inventory.add_product(product)

        suppliers = list(suppliers_by_id.values())
        print("Inventory loaded successfully.")
        return inventory, suppliers

    def __create_product(self, item: dict, supplier: Supplier) -> Product:
        """Use the saved "type" to build the matching subclass."""
        product_type = item.get("type")
        if product_type == PhysicalProduct.TYPE:
            return PhysicalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                supplier, item["weight"], item.get("transaction_history"),
            )
        if product_type == DigitalProduct.TYPE:
            return DigitalProduct(
                item["id"], item["name"], item["price"], item["stock"],
                supplier, item["download_size"], item.get("transaction_history"),
            )
        raise ValueError(f"unknown product type '{product_type}'")

    def save(self, inventory: Inventory, suppliers: list[Supplier]) -> None:
        # Also save any supplier that is only reachable through a product
        all_suppliers: dict[str, Supplier] = {
            s.get_supplier_id(): s for s in suppliers}
        for product in inventory.get_products():
            supplier = product.get_supplier()
            all_suppliers.setdefault(supplier.get_supplier_id(), supplier)

        data = {
            "suppliers": [s.to_dict() for s in all_suppliers.values()],
            "products": [p.to_dict() for p in inventory.get_products()],
        }
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
