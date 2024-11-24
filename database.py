# database.py

import sqlite3

class Database:
    def __init__(self, db_name='pos_inventory.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create products table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL)''')
        
        # Create transactions table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            total REAL NOT NULL,
            change REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        self.conn.commit()
    
    def add_product(self, name, price, quantity):
        self.cursor.execute('''INSERT INTO products (name, price, quantity)
                               VALUES (?, ?, ?)''', (name, price, quantity))
        self.conn.commit()

    def get_all_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def update_product_quantity(self, product_id, quantity_change):
        self.cursor.execute('''UPDATE products
                               SET quantity = quantity + ?
                               WHERE id = ?''', (quantity_change, product_id))
        self.conn.commit()

    def log_transaction(self, customer_name, total, change):
        self.cursor.execute('''INSERT INTO transactions (customer_name, total, change)
                               VALUES (?, ?, ?)''', (customer_name, total, change))
        self.conn.commit()

    def close(self):
        self.conn.close()
