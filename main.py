# main.py

from authentication import Authentication
from menu import MainMenu

def main():
    auth = Authentication()

    while True:
        print("\n--- Welcome to POS System ---")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            user = auth.login()
        
            if user:
                menu = MainMenu(user)
                menu.show_menu()
        elif choice == "2":
            auth.signup()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
1