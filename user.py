# user.py

import sqlite3
import hashlib

class User:
    def __init__(self, id, name, position, email, password):
        self.id = id
        self.name = name
        self.position = position
        self.email = email
        self.password = password

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(stored_hash, password):
        return stored_hash == hashlib.sha256(password.encode()).hexdigest()

class UserDatabase:
    def __init__(self, db_name='pos_inventory.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL)''')
        self.conn.commit()

    def add_user(self, name, position, email, password):
        password_hash = User.hash_password(password)
        self.cursor.execute('''INSERT INTO users (name, position, email, password)
                               VALUES (?, ?, ?, ?)''', (name, position, email, password_hash))
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute('''SELECT * FROM users WHERE email = ?''', (email,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
