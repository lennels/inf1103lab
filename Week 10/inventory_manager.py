import json
from pathlib import Path

#  Global Constant
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

def find_product(inventory, product_id):
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None

def load_inventory():
    # Missing file -> start with an empty inventory, no error
    if not Path(INVENTORY_FILE).exists():
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with an empty inventory.")
        return []

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as file:
            inventory = json.load(file)
    except json.JSONDecodeError:
        print(f"{INVENTORY_FILE} is not valid JSON. Starting with an empty inventory.")
        return []
    print("Inventory loaded successfully.")
    return inventory

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(inventory, file, indent=4)

def display_all(inventory):
    print("\nCurrent Inventory")
    print(LINE)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty.")
        return
    if find_product(inventory, product_id):
        print("\nProduct ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nProduct name cannot be empty.")
        return

    price = get_valid_number("Price: ", float)
    stock = get_valid_number("Stock Quantity: ", int)

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "transaction_history": [stock]
    })
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    new_stock = get_valid_number("\nNew Stock Quantity: ", int)
    # Record the change in stock so the history is kept, not just the total
    product.setdefault("transaction_history", []).append(new_stock - product["stock"])
    product["stock"] = new_stock
    print("\nStock updated successfully!")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
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

    inventory = load_inventory()
    display_menu()

    while True:
        option = input("\nEnter option: ").strip()
        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            display_menu()

    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")

if __name__ == "__main__":
    main()
