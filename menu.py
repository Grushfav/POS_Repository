# menu.py

class MainMenu:
    def __init__(self, user):
        self.user = user

    def show_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Start Transaction")
            print("2. Inventory (Add/Update/Remove Product)")
            if self.user.position == "inventory manager":
                print("3. Set Notification Alert (Low Stock)")
            print("4. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.start_transaction()
            elif choice == "2":
                self.manage_inventory()
            elif choice == "3" and self.user.position == "inventory manager":
                self.set_notification_alert()
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def start_transaction(self):
        print("Starting a new transaction...")
        # Add transaction logic here (e.g., process sale)

    def manage_inventory(self):
        print("Managing inventory...")
        # Add inventory management logic here (e.g., add/update/remove products)

    def set_notification_alert(self):
        print("Setting up low stock notification alert...")
        # Add notification alert setup (e.g., email inventory manager when stock is low)
