# menu.py (Updated with Transaction Handling)

from inventory import Inventory
from transaction import Transaction
from email_alert import send_email

class MainMenu:
    def __init__(self, user):
        self.user = user
        alert_email = "grushfav@gmail.com"
        self.inventory = Inventory()
        self.transaction = Transaction(self.inventory, alert_email)

    def show_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Start Transaction")
            print("2. Inventory (Add/Update/Remove Product)")
            if self.user.position == "inventory manager":
                print("3. Set Notification Alert (Low Stock)")
            print("4. Generate Report")
            print("5. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.start_transaction()
            elif choice == "2":
                self.manage_inventory()
            elif choice == "3" and self.user.position == "inventory manager":
                self.set_notification_alert()
            elif choice == "4":
                self.generate_daily_report()  # Handle report generation here
            elif choice == "5":
                print("Exiting...")
                self.inventory.close()  # Close the inventory database connection
                break
            else:
                print("Invalid choice. Please try again.")

    def start_transaction(self):
        print("\n--- Start Transaction ---")
        while True:
            print("\n1. Add Item to Cart")
            print("2. View Cart")
            print("3. Complete Transaction")
            print("4. Cancel Transaction")

            choice = input("Select an option: ")

            if choice == "1":
                self.add_item_to_cart()
            elif choice == "2":
                self.view_cart()
            elif choice == "3":
                self.complete_transaction()
                break
            elif choice == "4":
                print("Transaction canceled.")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_item_to_cart(self):
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity: "))
        self.transaction.add_to_cart(product_id, quantity)

    def view_cart(self):
        print("\n--- Cart Contents ---")
        total = 0
        for product, quantity in self.transaction.cart:
            print(f"ID: {product[0]} | Name: {product[1]} | Price: {product[2]} | Quantity: {quantity}")
            total += product[2] * quantity
        print(f"Total: {total}")

    def complete_transaction(self):
        total = self.transaction.calculate_total()
        print(f"Total: {total}")
        amount_paid = float(input("Enter amount paid: "))
        change = self.transaction.process_payment(amount_paid)

        if change is False:
            print("Transaction failed. Insufficient payment.")
        else:
            print(f"Change: {change}")
            self.transaction.complete_transaction()  # Update inventory and clear cart
    
    def manage_inventory(self):
        print("\n--- Inventory Management ---")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Remove Product")
        print("4. List Products")
        print("5. Go Back")

        choice = input("Select an option: ")

        if choice == "1":
            self.add_product()
        elif choice == "2":
            self.update_product()
        elif choice == "3":
            self.remove_product()
        elif choice == "4":
            self.list_products()
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")

    def add_product(self):
        print("\n--- Add Product ---")
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        self.inventory.add_product(name, price, quantity)
        print(f"Product '{name}' added successfully!")

    def update_product(self):
        print("\n--- Update Product ---")
        product_id = int(input("Enter product ID to update: "))
        name = input("Enter new product name (leave empty to skip): ")
        price = input("Enter new product price (leave empty to skip): ")
        quantity = input("Enter new product quantity (leave empty to skip): ")

        if price:
            price = float(price)
        else:
            price = None
        if quantity:
            quantity = int(quantity)
        else:
            quantity = None

        self.inventory.update_product(product_id, name, price, quantity)
        print(f"Product ID {product_id} updated successfully!")

    def remove_product(self):
        print("\n--- Remove Product ---")
        product_id = int(input("Enter product ID to remove: "))
        self.inventory.remove_product(product_id)
        print(f"Product ID {product_id} removed successfully!")

    def list_products(self):
        print("\n--- List Products ---")
        products = self.inventory.list_products()
        if products:
            for product in products:
                print(f"ID: {product[0]} | Name: {product[1]} | Price: {product[2]} | Quantity: {product[3]}")
        else:
            print("No products in inventory.")

    def set_notification_alert(self):
        print("\n--- Set Notification Alert ---")
        threshold = int(input("Enter the low stock threshold: "))
        low_stock_items = self.inventory.get_low_stock_items(threshold)

        if not low_stock_items:
            print("No products are below the threshold.")
        else:
            print("\nLow Stock Products:")
            message = "The following items are below the stock threshold:\n\n"
            for product in low_stock_items:
                print(f"ID: {product[0]} | Name: {product[1]} | Quantity: {product[3]}")
                message += f"ID: {product[0]} | Name: {product[1]} | Quantity: {product[3]}\n"

            # Send email alert
            manager_email = input("Enter inventory manager's email: ")
            subject = "Low Stock Alert"
            send_email(manager_email, subject, message)

    def generate_daily_report(self):
        """Handle the option to generate and email the daily report"""
        print("Generating and sending daily report...")

        # Generate the daily report
        report = self.transaction_report.generate_daily_report()

        # Send the report via email
        self.transaction_report.send_report_by_email(report)

        # Optionally, print the report to the console as well
        print("\nDaily Report Generated and Sent!")
        print(report)  # Print to screen

    def complete_transaction(self):
        total = self.transaction.calculate_total()
        print(f"Total: ${total:.2f}")
        amount_paid = float(input("Enter amount paid: $"))

        change = self.transaction.process_payment(amount_paid)

        if change is False:
            print("Transaction failed. Insufficient payment.")
        else:
            print(f"Change: ${change:.2f}")
            self.transaction.complete_transaction()

    def get_cart(self):
        # A simple cart for the example. You can expand this to allow user input.
        product1 = self.inventory.get_product(1)  # Get product by ID
        product2 = self.inventory.get_product(2)
        product3 = self.inventory.get_product(3)
        return [(product1, 3), (product2, 5), (product3, 2)]  # Example cart