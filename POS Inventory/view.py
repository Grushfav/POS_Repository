# view.py

class POSView:
    def show_product(self, product):
        print(f"Product: {product.name}")
        print(f"Price: ${product.price}")
        print(f"Quantity: {product.quantity}")
        print('-' * 30)

    def show_inventory(self, inventory):
        for product in inventory:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Quantity: {product[3]}")
        print('-' * 30)

    def show_message(self, message):
        print(message)

    def show_transaction(self, customer_name, total, change):
        print(f"Customer: {customer_name}")
        print(f"Total: ${total}")
        print(f"Change: ${change}")
        print('-' * 30)
