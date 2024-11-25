# transaction.py
from email_alert import send_email
from inventory import *



class Transaction:
    def __init__(self, inventory, alert_email):
        self.inventory = inventory
        self.cart = []
        self.alert_email = alert_email  # Inventory manager's email

    def add_to_cart(self, product_id, quantity):
        product = self.inventory.get_product(product_id)
        if product:
            if product[3] >= quantity:  # Check if enough stock is available
                self.cart.append((product, quantity))
                print(f"{quantity} x {product[1]} added to the cart.")
            else:
                print(f"Not enough stock for {product[1]}. Only {product[3]} available.")
        else:
            print("Product not found.")

    def calculate_total(self):
        total = sum(product[2] * quantity for product, quantity in self.cart)  # price * quantity
        return total

    def process_payment(self, amount_paid):
        total = self.calculate_total()
        if amount_paid < total:
            print(f"Insufficient payment. Total is {total}, but only {amount_paid} was provided.")
            return False
        change = amount_paid - total
        return change

    def complete_transaction(self):
        # Update the inventory quantities
        for product, quantity in self.cart:
            new_quantity = product[3] - quantity
            self.inventory.update_product(product[0], quantity=new_quantity)
        print("Transaction complete! Inventory updated.")

        # Call print_receipt to display the transaction summary
        self.print_receipt()
        self.check_low_stock()
        self.cart.clear()  # Clear the cart after the transaction

    def check_low_stock(self):
        low_stock_products = []
        for product in self.inventory.get_all_products():
            if product[3] < 12:  # Threshold for low stock
                low_stock_products.append(product)

        if low_stock_products:
            self.send_low_stock_alert(low_stock_products)

    def send_low_stock_alert(self, low_stock_products):
        # Prepare the email message
        subject = "Low Stock Alert"
        message = "The following products are low in stock:\n\n"
        for product in low_stock_products:
            message += f"Product: {product[1]}, Quantity: {product[3]}\n"

        # Send the email
        try:
            send_email(self.alert_email, subject, message)
            print("Low stock alert email sent successfully.")
        except Exception as e:
            print(f"Failed to send low stock alert: {e}")
    def print_receipt(self):
        print("\n--- Transaction Summary ---")
        print(f"{'Product':<15} {'Quantity':<10} {'Cost':<10}")
        print("-" * 35)
        total = 0
        for product, quantity in self.cart:
            cost = product[2] * quantity
            total += cost
            print(f"{product[1]:<15} {quantity:<10} ${cost:<10.2f}")
        print("-" * 35)
        print(f"Total: ${total:.2f}")