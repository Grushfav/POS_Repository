# inventory.py

import sqlite3

class Inventory:
    def __init__(self, db_name='pos_inventory.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_inventory_table()

    def create_inventory_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL)''')
        self.conn.commit()

    def add_product(self, name, price, quantity):
        self.cursor.execute('''INSERT INTO inventory (name, price, quantity)
                               VALUES (?, ?, ?)''', (name, price, quantity))
        self.conn.commit()

    def update_product(self, product_id, name=None, price=None, quantity=None):
        if name:
            self.cursor.execute('''UPDATE inventory SET name = ? WHERE id = ?''', (name, product_id))
        if price is not None:
            self.cursor.execute('''UPDATE inventory SET price = ? WHERE id = ?''', (price, product_id))
        if quantity is not None:
            self.cursor.execute('''UPDATE inventory SET quantity = ? WHERE id = ?''', (quantity, product_id))
        self.conn.commit()

    def remove_product(self, product_id):
        self.cursor.execute('''DELETE FROM inventory WHERE id = ?''', (product_id,))
        self.conn.commit()

    def list_products(self):
        self.cursor.execute('''SELECT * FROM inventory''')
        return self.cursor.fetchall()

    def get_product(self, product_id):
        self.cursor.execute('''SELECT * FROM inventory WHERE id = ?''', (product_id,))
        return self.cursor.fetchone()
    
    def get_low_stock_items(self, threshold):
        self.cursor.execute("SELECT * FROM inventory WHERE quantity < ?", (threshold,))
        return self.cursor.fetchall()  # Fetch all products with quantity below the threshold

    
    def get_all_products(self):
        self.cursor.execute("SELECT * FROM inventory")
        return self.cursor.fetchall()  # Returns all rows from the inventory table

    
    def close(self):
        self.conn.close()

    