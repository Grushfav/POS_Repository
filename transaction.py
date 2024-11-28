# transaction.py
from email_alert import send_email
from inventory import *
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sqlite3


class Transaction:
    def __init__(self, inventory, alert_email):
        self.inventory = inventory
        self.cart = []
        self.alert_email = alert_email  # Inventory manager's email
        self.transactions_log = []  

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
        # Get the current time for the transaction
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\nTransaction Time: {transaction_time}")
        print("="*50)
        print(f"{'Item':<20}{'Unit Price':<12}{'Quantity':<10}{'Total Price':<12}")
        print("="*50)

        # Initialize total cost for the transaction
        total_cost = 0

        # Loop through the cart to print the details of each item
        for product, quantity in self.cart:
            name = product[1]  # Name of the product
            price = product[2]  # Unit price of the product
            total_price = price * quantity  # Total price for the product

            # Print the item details
            print(f"{name:<20}{price:<12}{quantity:<10}{total_price:<12.2f}")

            # Add the total price to the overall total
            total_cost += total_price

        print("="*40)
        print(f"{'Total Cost:':<32}{total_cost:.2f}")
        print("="*40)

        # Update inventory quantities
        for product, quantity in self.cart:
            new_quantity = product[3] - quantity
            self.inventory.update_product(product[0], quantity=new_quantity)

        # Print receipt (already handled above with the formatted table)

        # Check stock levels and send email alerts if necessary
        self.check_low_stock()

        # Clear the cart
        self.cart.clear()
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

    def record_transaction(self, cart):
        """Record each transaction for later reporting"""
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_revenue = 0

        for product, quantity in cart:
            name = product[1]
            price = product[2]
            total_price = price * quantity
            total_revenue += total_price

            # Add to the transactions log
            self.transactions_log.append({
                'time': transaction_time,
                'product': name,
                'quantity': quantity,
                'total_price': total_price
            })

        return total_revenue

    def generate_daily_report(self):
        """Generate daily sales report"""
        report = f"Daily Sales Report - {datetime.now().strftime('%Y-%m-%d')}\n"
        report += "=" * 50 + "\n"
        report += f"{'Item':<20}{'Quantity Sold':<15}{'Revenue Generated':<15}\n"
        report += "=" * 50 + "\n"

        # Calculate total sales and revenue per item
        item_sales = {}
        total_revenue = 0

        for transaction in self.transactions_log:
            item = transaction['product']
            if item not in item_sales:
                item_sales[item] = {'quantity': 0, 'revenue': 0}
            item_sales[item]['quantity'] += transaction['quantity']
            item_sales[item]['revenue'] += transaction['total_price']
            total_revenue += transaction['total_price']

      
        for item, data in item_sales.items():
            report += f"{item:<20}{data['quantity']:<15}{data['revenue']:<15.2f}\n"

        report += "=" * 50 + "\n"
        report += f"Total Revenue for the Day: {total_revenue:.2f}\n"
        report += "=" * 50 + "\n\n"

        # Get low stock items
        low_stock_items = self.inventory.get_low_stock_items(threshold=12)
        if low_stock_items:
            report += "Low Stock Items Report:\n"
            report += "=" * 50 + "\n"
            report += f"{'Item':<20}{'Current Stock':<15}\n"
            report += "=" * 50 + "\n"
            for item in low_stock_items:
                report += f"{item[1]:<20}{item[3]:<15}\n"
            report += "=" * 50 + "\n"
        else:
            report += "No low stock items.\n"
        
        return report

    def send_report_by_email(self, report):
        """Send the generated report by email"""
        try:
            # Setup email
            message = MIMEMultipart()
            message['From'] = 'your-email@gmail.com'
            message['To'] = self.alert_email
            message['Subject'] = 'Daily Sales and Inventory Report'
            message.attach(MIMEText(report, 'plain'))

            # Send the email using SMTP
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('your-email@gmail.com', 'your-password')
                server.sendmail('your-email@gmail.com', self.alert_email, message.as_string())

            print("Report successfully sent!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def generate_and_send_report(self, cart):
        """Complete flow to generate and send report"""
        # Record the transaction
        total_revenue = self.record_transaction(cart)

        # Generate the daily report
        report = self.generate_daily_report()

        # Send the report via email
        self.send_report_by_email(report)

        # Optionally, you can also print the report to the screen
        print(report)

