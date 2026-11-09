"""Lab 8 walkthrough: run each relationship and print the results.

Run with:  python lab8_demo.py
Write down your "Predict first" answers BEFORE running this.
"""
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

LINE = "=" * 48


def heading(title: str) -> None:
    print(f"\n{LINE}\n{title}\n{LINE}")


def show_product_details(product: Product) -> None:
    """Section 6.2: only uses behaviour every Product supports."""
    product.display_information()
    print(product.get_fulfilment_info())


def demo_association() -> None:
    heading("Section 2: Association (Supplier - Product)")
    supplier = Supplier("SUP001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200, 15, supplier, 2.1)
    editor = DigitalProduct("D001", "Photo Editor", 79.9, 50, supplier, 850)

    print("Supplier info through each product:")
    laptop.get_supplier().display_information()
    editor.get_supplier().display_information()
    print(f"Same supplier object? {laptop.get_supplier() is editor.get_supplier()}")
    print(f"Supplier is a separate object from the product? {laptop is not supplier}")

    print("\nPredict first: del supplier")
    del supplier
    print("After del, laptop's supplier is:", laptop.get_supplier())


def demo_aggregation() -> None:
    heading("Section 3: Aggregation (Inventory - Product)")
    supplier = Supplier("SUP002", "Melody Instruments", "orders@melody.example.com")
    guitar = PhysicalProduct("P003", "Guitar", 450, 5, supplier, 3.5)
    print("1. Product created before any inventory:", guitar)

    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(guitar)
    print("2. Added to Inventory A. Found:", inventory_a.find_product("P003") is guitar)

    print("Predict first: does the product still work after removal?")
    removed = inventory_a.remove_product("P003")
    print("3. Removed from A. Still in A?", inventory_a.find_product("P003") is not None)
    removed.update_stock(6)
    print("   Product still usable, stock now:", removed.get_stock())

    inventory_b.add_product(guitar)
    print("4. Added same object to Inventory B:", inventory_b.find_product("P003") is guitar)
    print(f"   id(guitar)={id(guitar)}  id(in B)={id(inventory_b.find_product('P003'))}")


def demo_composition() -> None:
    heading("Section 4: Composition (Order - OrderLine)")
    supplier = Supplier("SUP001", "TechWorld Pte Ltd", "sales@techworld.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200, 15, supplier, 2.1)
    mouse = PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1)
    editor = DigitalProduct("D001", "Photo Editor", 79.9, 50, supplier, 850)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(mouse, 2)
    order_1.add_order_line(editor, 1)
    order_1.display_order()

    print("\nPredict first: same product in two orders")
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 3)
    order_2.display_order()
    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"Same OrderLine object? {line_1 is line_2}  "
          f"(id {id(line_1)} vs {id(line_2)})")
    print(f"Same Product object?   {line_1.get_product() is line_2.get_product()}  "
          f"(id {id(line_1.get_product())} vs {id(line_2.get_product())})")

    print("\nRemoving the Mouse line from O001 through the Order:")
    order_1.remove_order_line("P002")
    order_1.display_order()


def demo_polymorphism() -> None:
    heading("Sections 6-7: LSP and polymorphism")
    supplier = Supplier("SUP003", "SoftHouse Digital", "licensing@softhouse.example.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.5, 40, supplier, 0.1))
    inventory.add_product(DigitalProduct("D002", "Operating System", 199, 100, supplier, 5200))

    print("Predict first: what does each get_fulfilment_info() print?")
    print("One loop over list[Product], no isinstance():\n")
    for product in inventory.get_products():
        show_product_details(product)
        print()

    print("update_stock() works the same for both subclasses:")
    for product in inventory.get_products():
        product.update_stock(10)
        print(f"  {product.get_name()}: stock={product.get_stock()}")


if __name__ == "__main__":
    demo_association()
    demo_aggregation()
    demo_composition()
    demo_polymorphism()
