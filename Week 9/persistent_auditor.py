from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory_file import InventoryFile
from physical_product import PhysicalProduct

INVENTORY_FILE = "inventory.json"
LINE = "-" * 48


def get_valid_number(prompt, number_type):
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


def choose_product_type():
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


def add_product(inventory):
    print("\nAdd New Product")
    product_type = choose_product_type()

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty.")
        return
    if inventory.search_product(product_id):
        print("\nProduct ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nProduct name cannot be empty.")
        return

    price = get_valid_number("Price: ", float)
    stock = get_valid_number("Stock Quantity: ", int)

    if product_type == PhysicalProduct.TYPE:
        weight = get_valid_number("Weight (kg): ", float)
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_valid_number("Download Size (MB): ", float)
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    new_stock = get_valid_number("\nNew Stock Quantity: ", int)
    product.update_stock(new_stock)
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    # Only products that signed the CanBeShipped contract have a shipping cost
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print(LINE)


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory_file = InventoryFile(INVENTORY_FILE)
    inventory = inventory_file.load()
    display_menu()

    while True:
        option = input("\nEnter option: ").strip()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            inventory_file.save(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            inventory_file.save(inventory)
            print("Inventory saved successfully.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            display_menu()

    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")


if __name__ == "__main__":
    main()
