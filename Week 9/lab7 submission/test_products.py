"""Lab 7 checks (section 7). Run with:  python -m unittest -v"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from physical_product import PhysicalProduct
from product import Product


def captured_display(product):
    """Run display_information() and return what it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.guitar = PhysicalProduct("P100", "Guitar", 450, 5, 3.5)
        self.os = DigitalProduct("D100", "Operating System", 199, 100, 5200)

    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.guitar.get_weight(), 3.5)
        output = captured_display(self.guitar)
        self.assertIn("Name: Guitar", output)        # from Product
        self.assertIn("Weight: 3.50 kg", output)     # from PhysicalProduct

    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.os.get_download_size(), 5200)
        output = captured_display(self.os)
        self.assertIn("Name: Operating System", output)
        self.assertIn("Download Size: 5200.00 MB", output)

    def test_both_implement_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os.get_fulfilment_info())

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X1", "Generic", 1, 1)

    def test_can_be_shipped_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P1", "Mouse", 25, 1, 0.1)
        heavy = PhysicalProduct("P2", "Desk", 300, 1, 20)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 5.20)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 45.00)

    def test_digital_is_not_shippable(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertNotIsInstance(self.os, CanBeShipped)
        self.assertFalse(hasattr(self.os, "calculate_shipping_cost"))


class TestInventory(unittest.TestCase):

    def test_add_search_and_update(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(PhysicalProduct("P1", "Mouse", 25, 10, 0.1)))
        self.assertFalse(inventory.add_product(DigitalProduct("p1", "Dup", 1, 1, 1)))
        product = inventory.search_product("p1")
        product.update_stock(15)
        self.assertEqual(product.get_stock(), 15)
        self.assertEqual(product.get_transaction_history(), [10, 5])


class TestInventoryFile(unittest.TestCase):

    def test_save_and_load_keep_product_types(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P1", "Guitar", 450, 5, 3.5))
        inventory.add_product(DigitalProduct("D1", "OS", 199, 100, 5200))

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with redirect_stdout(io.StringIO()):
                InventoryFile(path).save(inventory)
                loaded = InventoryFile(path).load()

        guitar = loaded.search_product("P1")
        os_product = loaded.search_product("D1")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 3.5)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(os_product.get_download_size(), 5200)


if __name__ == "__main__":
    unittest.main()
