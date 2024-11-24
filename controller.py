# controller.py

from model import Product
from view import POSView
from database import Database

class POSController:
    def __init__(self):
        self.view = POSView()
        self.db = Database()
        self.db.create_tables()

    def add_product(self, name, price, quantity):
        self.db.add_product(name, price, quantity)
        self.view.show_message(f"Added {name} to inventory.")

    def load_inventory(self):
        products = self.db.get_all_products()
        return [Product(*product) for product in products]

    def update_product_quantity(self, product_id, quantity_change):
        self.db.update_product_quantity(product_id, quantity_change)

    def process_transaction(self, customer_name, purchased_items, amount_paid):
        total = sum(item['product'].price * item['quantity'] for item in purchased_items)
        change = amount_paid - total

        if change < 0:
            self.view.show_message("Insufficient payment. Transaction failed.")
            return

        for item in purchased_items:
            product = item['product']
            self.update_product_quantity(product.id, -item['quantity'])  # Subtract purchased quantity

        self.db.log_transaction(customer_name, total, change)
        self.view.show_transaction(customer_name, total, change)
