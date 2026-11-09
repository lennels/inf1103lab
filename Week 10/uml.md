# Lab 8 UML class diagram

Paste the block below into https://mermaid.live to render and export it.

- Association: Supplier 1 —— 0..* Product (plain line)
- Aggregation: Inventory 0..1 ◇—— 0..* Product (hollow diamond)
- Composition: Order 1 ◆—— 0..* OrderLine (filled diamond)
- Association: OrderLine 0..* —— 1 Product
- Inheritance: PhysicalProduct, DigitalProduct ——▷ Product
- Realisation: PhysicalProduct ..▷ CanBeShipped

```mermaid
classDiagram
    direction LR

    class Supplier {
        -supplier_id: String
        -name: String
        -contact_email: String
        +get_supplier_id() String
        +get_name() String
        +get_contact_email() String
        +display_information() void
    }

    class Product {
        <<abstract>>
        -product_id: String
        -name: String
        -price: float
        -stock: int
        -supplier: Supplier
        -transaction_history: int [0..*]
        +get_product_id() String
        +get_name() String
        +get_price() float
        +get_stock() int
        +get_supplier() Supplier
        +update_stock(quantity: int) void
        +get_fulfilment_info()* String
        +display_information() void
    }

    class PhysicalProduct {
        -weight: float
        +get_weight() float
        +get_fulfilment_info() String
        +calculate_shipping_cost() float
        +display_information() void
    }

    class DigitalProduct {
        -download_size: float
        +get_download_size() float
        +get_fulfilment_info() String
        +display_information() void
    }

    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }

    class Inventory {
        -products: Product [0..*]
        +add_product(product: Product) bool
        +remove_product(product_id: String) Product [0..1]
        +find_product(product_id: String) Product [0..1]
        +get_products() Product [0..*]
        +display_all_products() void
    }

    class Order {
        -order_id: String
        -order_lines: OrderLine [0..*]
        +add_order_line(product: Product, quantity: int) void
        +remove_order_line(product_id: String) bool
        +calculate_total() float
        +display_order() void
    }

    class OrderLine {
        -product: Product
        -quantity: int
        +calculate_subtotal() float
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct

    Supplier "1" -- "0..*" Product : supplies
    Inventory "0..1" o-- "0..*" Product : contains
    Order "1" *-- "0..*" OrderLine : owns
    OrderLine "0..*" --> "1" Product : refers to
```
