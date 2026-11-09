"""Lab 7 + Lab 8 checks. Run with:  python -m unittest -v"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def captured(func, *args) -> str:
    """Run func(*args) and return what it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


def show_product_details(product: Product) -> str:
    """Lab 8 section 6.2: uses only what every Product supports."""
    return captured(product.display_information) + product.get_fulfilment_info()


class TestProducts(unittest.TestCase):
    """Lab 7 behaviour, updated for the Supplier parameter."""

    def setUp(self):
        self.supplier = Supplier("SUP1", "Acme", "acme@example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 450, 5, self.supplier, 3.5)
        self.os = DigitalProduct("D100", "Operating System", 199, 100, self.supplier, 5200)

    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.guitar.get_weight(), 3.5)
        output = captured(self.guitar.display_information)
        self.assertIn("Name: Guitar", output)        # from Product
        self.assertIn("Weight: 3.50 kg", output)     # from PhysicalProduct

    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.os.get_download_size(), 5200)
        output = captured(self.os.display_information)
        self.assertIn("Name: Operating System", output)
        self.assertIn("Download Size: 5200.00 MB", output)

    def test_both_implement_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os.get_fulfilment_info())

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X1", "Generic", 1, 1, self.supplier)

    def test_can_be_shipped_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P1", "Mouse", 25, 1, self.supplier, 0.1)
        heavy = PhysicalProduct("P2", "Desk", 300, 1, self.supplier, 20)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 5.20)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 45.00)

    def test_digital_is_not_shippable(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertNotIsInstance(self.os, CanBeShipped)
        self.assertFalse(hasattr(self.os, "calculate_shipping_cost"))


class TestAssociation(unittest.TestCase):
    """Section 2: Supplier <-> Product."""

    def test_product_stores_reference_to_supplier(self):
        supplier = Supplier("SUP1", "Acme", "acme@example.com")
        laptop = PhysicalProduct("P1", "Laptop", 1200, 3, supplier, 2.1)
        ebook = DigitalProduct("D1", "E-book", 15, 50, supplier, 3)
        # Both products point at the same Supplier object, not a copy
        self.assertIs(laptop.get_supplier(), supplier)
        self.assertIs(ebook.get_supplier(), supplier)
        self.assertIn("Supplier: Acme", captured(laptop.display_information))

    def test_product_keeps_working_after_supplier_variable_deleted(self):
        supplier = Supplier("SUP1", "Acme", "acme@example.com")
        laptop = PhysicalProduct("P1", "Laptop", 1200, 3, supplier, 2.1)
        del supplier   # only removes the name, not the object
        self.assertEqual(laptop.get_supplier().get_name(), "Acme")

    def test_supplier_exists_without_products(self):
        supplier = Supplier("SUP2", "Solo", "solo@example.com")
        self.assertIn("Supplier Name: Solo", captured(supplier.display_information))


class TestAggregation(unittest.TestCase):
    """Section 3: Inventory groups Products it does not own."""

    def setUp(self):
        self.supplier = Supplier("SUP1", "Acme", "acme@example.com")
        # Product exists before any inventory does
        self.mouse = PhysicalProduct("P1", "Mouse", 25, 10, self.supplier, 0.1)

    def test_add_find_and_reject_duplicate_id(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.mouse))
        self.assertFalse(inventory.add_product(
            DigitalProduct("p1", "Dup", 1, 1, self.supplier, 1)))
        self.assertIs(inventory.find_product("p1"), self.mouse)
        self.assertIsNone(inventory.find_product("missing"))

    def test_transfer_between_inventories_does_not_destroy_product(self):
        inventory_a, inventory_b = Inventory(), Inventory()
        inventory_a.add_product(self.mouse)

        removed = inventory_a.remove_product("P1")
        self.assertIs(removed, self.mouse)
        self.assertIsNone(inventory_a.find_product("P1"))
        # Still a working product after removal
        self.mouse.update_stock(12)
        self.assertEqual(self.mouse.get_stock(), 12)

        inventory_b.add_product(self.mouse)
        self.assertIs(inventory_b.find_product("P1"), self.mouse)

    def test_remove_missing_product_returns_none(self):
        self.assertIsNone(Inventory().remove_product("nope"))

    def test_update_stock_records_history(self):
        inventory = Inventory()
        inventory.add_product(self.mouse)
        inventory.find_product("P1").update_stock(15)
        self.assertEqual(self.mouse.get_transaction_history(), [10, 5])


class TestComposition(unittest.TestCase):
    """Section 4: Order creates and owns its OrderLines."""

    def setUp(self):
        supplier = Supplier("SUP1", "Acme", "acme@example.com")
        self.laptop = PhysicalProduct("P1", "Laptop", 1200, 3, supplier, 2.1)
        self.ebook = DigitalProduct("D1", "E-book", 15, 50, supplier, 3)

    def test_order_creates_lines_and_calculates_total(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 2)
        order.add_order_line(self.ebook, 4)
        lines = order.get_order_lines()
        self.assertEqual(len(lines), 2)
        self.assertIsInstance(lines[0], OrderLine)
        self.assertAlmostEqual(lines[0].calculate_subtotal(), 2400)
        self.assertAlmostEqual(order.calculate_total(), 2460)

    def test_order_line_refers_to_product_without_owning_it(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 1)
        self.assertIs(order.get_order_lines()[0].get_product(), self.laptop)

    def test_same_product_in_two_orders_gives_two_lines_one_product(self):
        order_1, order_2 = Order("O1"), Order("O2")
        order_1.add_order_line(self.laptop, 1)
        order_2.add_order_line(self.laptop, 1)
        line_1 = order_1.get_order_lines()[0]
        line_2 = order_2.get_order_lines()[0]
        self.assertIsNot(line_1, line_2)                          # 2 OrderLines
        self.assertIs(line_1.get_product(), line_2.get_product())  # 1 Product

    def test_remove_order_line(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 1)
        order.add_order_line(self.ebook, 1)
        self.assertTrue(order.remove_order_line("p1"))
        self.assertFalse(order.remove_order_line("p1"))
        self.assertAlmostEqual(order.calculate_total(), 15)

    def test_order_lines_cannot_be_changed_from_outside(self):
        order = Order("O1")
        order.add_order_line(self.laptop, 1)
        with self.assertRaises(AttributeError):
            order.get_order_lines().append("anything")   # tuple, read-only

    def test_quantity_must_be_positive(self):
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(self.laptop, 0)


class TestLiskovAndPolymorphism(unittest.TestCase):
    """Sections 6 and 7: any Product can stand in for Product."""

    def setUp(self):
        supplier = Supplier("SUP1", "Acme", "acme@example.com")
        self.products: list[Product] = [
            PhysicalProduct("P1", "Laptop", 1200, 3, supplier, 2.1),
            DigitalProduct("D1", "E-book", 15, 50, supplier, 3),
        ]

    def test_show_product_details_works_for_every_subclass(self):
        physical, digital = (show_product_details(p) for p in self.products)
        self.assertIn("Weight: 2.10 kg", physical)
        self.assertIn("physical shipping", physical)
        self.assertIn("Download Size: 3.00 MB", digital)
        self.assertIn("digitally", digital)

    def test_inventory_display_uses_each_subclass_implementation(self):
        inventory = Inventory()
        for product in self.products:
            inventory.add_product(product)
        output = captured(inventory.display_all_products)
        self.assertIn("This product requires physical shipping.", output)
        self.assertIn("This product is delivered digitally via a download link.", output)

    def test_update_stock_contract_is_kept_by_every_subclass(self):
        for product in self.products:
            with self.subTest(product=type(product).__name__):
                product.update_stock(0)
                self.assertEqual(product.get_stock(), 0)
                product.update_stock(7)
                self.assertEqual(product.get_stock(), 7)
                self.assertEqual(product.get_transaction_history()[-1], 7)
                with self.assertRaises(ValueError):
                    product.update_stock(-1)


class TestInventoryFile(unittest.TestCase):

    def test_save_and_load_keep_types_and_shared_supplier(self):
        supplier = Supplier("SUP1", "Acme", "acme@example.com")
        unused = Supplier("SUP2", "Spare", "spare@example.com")
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P1", "Guitar", 450, 5, supplier, 3.5))
        inventory.add_product(DigitalProduct("D1", "OS", 199, 100, supplier, 5200))

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with redirect_stdout(io.StringIO()):
                InventoryFile(path).save(inventory, [supplier, unused])
                loaded, suppliers = InventoryFile(path).load()

        guitar = loaded.find_product("P1")
        os_product = loaded.find_product("D1")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 3.5)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(os_product.get_download_size(), 5200)
        # Both products share one loaded Supplier object
        self.assertIs(guitar.get_supplier(), os_product.get_supplier())
        self.assertEqual(guitar.get_supplier().get_contact_email(), "acme@example.com")
        # A supplier with no products is still kept
        self.assertEqual(sorted(s.get_supplier_id() for s in suppliers), ["SUP1", "SUP2"])

    def test_old_list_format_still_loads(self):
        old_data = [{"id": "P1", "name": "Mouse", "price": 25, "stock": 1,
                     "type": "physical", "weight": 0.1}]
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w", encoding="utf-8") as file:
                json.dump(old_data, file)
            with redirect_stdout(io.StringIO()):
                loaded, _ = InventoryFile(path).load()
        self.assertEqual(loaded.find_product("P1").get_supplier().get_name(),
                         "Unknown Supplier")


if __name__ == "__main__":
    unittest.main()
