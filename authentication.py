# authentication.py

from user import UserDatabase
from user import User

class Authentication:
    def __init__(self):
        self.user_db = UserDatabase()
        self.user_db.create_user_table()

    def signup(self):
        print("=== Sign Up ===")
        name = input("Enter your name: ")
        position = input("Enter your position (cashier/inventory manager): ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        existing_user = self.user_db.get_user_by_email(email)
        if existing_user:
            print("This email is already registered.")
            return None
        
        self.user_db.add_user(name, position, email, password)
        print("Sign-up successful! You can now log in.")

    def login(self):
        print("=== Log In ===")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user_data = self.user_db.get_user_by_email(email)
        if not user_data:
            print("No user found with that email.")
            return None

        user = User(*user_data)
        if User.check_password(user.password, password):
            print(f"Welcome {user.name}!")
            return user
        else:
            print("Incorrect password.")
            return None
