# main.py

from controller import POSController
from model import Product

def main():
    pos = POSController()

    # Adding products to the inventory
    pos.add_product("Apple", 0.5, 100)
    pos.add_product("Banana", 0.3, 150)

    # View the current inventory
    inventory = pos.load_inventory()
    pos.view.show_inventory([(product.id, product.name, product.price, product.quantity) for product in inventory])

    # Simulating a customer transaction
    customer_name = "John Doe"
    purchased_items = [
        {"product": inventory[0], "quantity": 3},  # 3 Apples
        {"product": inventory[1], "quantity": 5}   # 5 Bananas
    ]
    amount_paid = 5.00  # Customer pays $5

    pos.process_transaction(customer_name, purchased_items, amount_paid)

    # View the updated inventory after the transaction
    updated_inventory = pos.load_inventory()
    pos.view.show_inventory([(product.id, product.name, product.price, product.quantity) for product in updated_inventory])

if __name__ == "__main__":
    main()
