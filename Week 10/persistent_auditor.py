from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

# Keep inventory.json next to this script, whichever folder it is run from
INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"
LINE = "-" * 48


def get_valid_number(prompt: str, number_type: type[int] | type[float]) -> int | float:
    while True:
        user_input = input(prompt).strip()
        try:
            value = number_type(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if value < 0:
            print("Invalid input. Please enter a non-negative number.")
            continue
        return value


def choose_product_type() -> str:
    """Ask until the user picks physical (1) or digital (2)."""
    while True:
        print("Product Type:")
        print("  1. Physical")
        print("  2. Digital")
        choice = input("Choose type: ").strip()
        if choice == "1":
            return PhysicalProduct.TYPE
        if choice == "2":
            return DigitalProduct.TYPE
        print("Invalid choice. Please enter 1 or 2.")


def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_supplier_id().lower() == supplier_id.lower():
            return supplier
    return None


def choose_supplier(suppliers: list[Supplier]) -> Supplier | None:
    """Pick an existing supplier by ID, or create a new one.

    The Supplier is created here, separately from any Product, and then
    handed to the Product (association).
    """
    display_suppliers(suppliers)
    supplier_id = input("Supplier ID (existing or new): ").strip()
    if not supplier_id:
        print("\nSupplier ID cannot be empty.")
        return None

    supplier = find_supplier(suppliers, supplier_id)
    if supplier:
        print(f"Using supplier: {supplier.get_name()}")
        return supplier

    print("New supplier.")
    name = input("Supplier Name: ").strip()
    email = input("Contact Email: ").strip()
    if not name or not email:
        print("\nSupplier name and email cannot be empty.")
        return None
    supplier = Supplier(supplier_id, name, email)
    suppliers.append(supplier)
    return supplier


def add_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("\nAdd New Product")
    product_type = choose_product_type()

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty.")
        return
    if inventory.find_product(product_id):
        print("\nProduct ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nProduct name cannot be empty.")
        return

    price = get_valid_number("Price: ", float)
    stock = get_valid_number("Stock Quantity: ", int)
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product: Product
    if product_type == PhysicalProduct.TYPE:
        weight = get_valid_number("Weight (kg): ", float)
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_valid_number("Download Size (MB): ", float)
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    new_stock = get_valid_number("\nNew Stock Quantity: ", int)
    product.update_stock(new_stock)
    print("\nStock updated successfully!")


def show_product_details(product: Product) -> None:
    """Works for any Product subclass without checking its type (LSP)."""
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    show_product_details(product)
    print(LINE)


def display_suppliers(suppliers: list[Supplier]) -> None:
    print("\nSuppliers")
    print(LINE)
    if not suppliers:
        print("No suppliers yet.")
    for supplier in suppliers:
        print(supplier)
    print(LINE)


def create_order(inventory: Inventory) -> None:
    """Build an Order from products in the inventory.

    Orders are not saved to the file; they exist for this session only.
    """
    print("\nCreate Order")
    order_id = input("Order ID: ").strip()
    if not order_id:
        print("\nOrder ID cannot be empty.")
        return
    order = Order(order_id)

    print("Enter products to order. Leave Product ID blank to finish.")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if not product:
            print("Product not found.")
            continue
        quantity = get_valid_number("Quantity: ", int)
        if quantity == 0:
            print("Quantity must be at least 1.")
            continue
        # The Order creates the OrderLine itself (composition)
        order.add_order_line(product, quantity)

    order.display_order()


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Display Suppliers")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory_file = InventoryFile(INVENTORY_FILE)
    inventory, suppliers = inventory_file.load()
    display_menu()

    while True:
        option = input("\nEnter option: ").strip()
        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            display_suppliers(suppliers)
        elif option == "6":
            create_order(inventory)
        elif option == "7":
            print("\nSaving inventory...")
            inventory_file.save(inventory, suppliers)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "8":
            print("\nSaving inventory before exit...")
            inventory_file.save(inventory, suppliers)
            print("Inventory saved successfully.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 8.")
            display_menu()

    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")


if __name__ == "__main__":
    main()
