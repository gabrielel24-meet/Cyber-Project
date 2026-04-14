import sqlite3
from protocol import *

# Connect to DB (if it doesn't exist it will be created)
conn = sqlite3.connect("Bank.db")

# Create object "cursor" to execute SQL-queries
cursor = conn.cursor()

# Enable foreign keys in SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# cursor.execute("""CREATE TABLE users (
#         id TEXT PRIMARY KEY,
#         first_name TEXT NOT NULL,
#         last_name TEXT NOT NULL,
#         phone_number TEXT UNIQUE,
#         password TEXT NOT NULL,
#         account_number TEXT UNIQUE,
#         balance REAL DEFAULT 0
#     );
#     """)

# cursor.execute("""
#     CREATE TABLE user_expenses (
#         expenses_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         id TEXT NOT NULL,
#         expense_type TEXT NOT NULL,
#         payment_type TEXT NOT NULL,
#         expense_amount REAL,
#         date TEXT NOT NULL,

#         FOREIGN KEY (id) REFERENCES users(id)
#             ON DELETE CASCADE
# )
# """)

# cursor.execute("""CREATE TABLE IF NOT EXISTS transfers (
#         transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         source_account TEXT NOT NULL,
#         destination_account TEXT NOT NULL,
#         transfer_amount REAL,
#         date TEXT NOT NULL
#     );
# """)

# # Insert data record
# cursor.execute("""INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#                ("1", "gabi", "eliav", "1","1",1,10000))

# cursor.execute("""INSERT INTO user_expenses
# (id, expense_type, payment_type, expense_amount, month, year)
# VALUES
# (1, 'Food',     'Cash',   200, 'Jan', strftime('%Y','now')),
# (1, 'Gadgets',  'Credit', 800, 'Jan', strftime('%Y','now')),
# (1, 'Clothes',  'Cash',   300, 'Jan', strftime('%Y','now')),
# (1, 'Food',     'Credit', 500, 'Jan', strftime('%Y','now')),
#
# (1, 'Food',     'Credit', 600, 'Feb', strftime('%Y','now')),
# (1, 'Clothes',  'Cash',   200, 'Feb', strftime('%Y','now')),
# (1, 'Gifts',    'Credit', 150, 'Feb', strftime('%Y','now')),
# (1, 'Food',     'Cash',   400, 'Feb', strftime('%Y','now')),
# (1, 'Other',    'Credit', 350, 'Feb', strftime('%Y','now')),
#
# (1, 'Gadgets',  'Cash',   900, 'Mar', strftime('%Y','now')),
# (1, 'Food',     'Credit', 300, 'Mar', strftime('%Y','now')),
# (1, 'Clothes',  'Credit', 450, 'Mar', strftime('%Y','now')),
# (1, 'Gifts',    'Cash',   200, 'Mar', strftime('%Y','now')),
# (1, 'Food',     'Cash',   250, 'Mar', strftime('%Y','now')),
#
# (1, 'Other',    'Credit', 500, 'Apr', strftime('%Y','now')),
# (1, 'Food',     'Cash',   350, 'Apr', strftime('%Y','now')),
# (1, 'Clothes',  'Credit', 600, 'Apr', strftime('%Y','now')),
# (1, 'Gadgets',  'Credit', 700, 'Apr', strftime('%Y','now')),
# (1, 'Gifts',    'Cash',   180, 'Apr', strftime('%Y','now'));
# """)
# cursor.execute("""INSERT INTO user_expenses (id, expense_type, payment_type, expense_amount) VALUES (?, ?, ?, ?)""",
#                ("3", "Food","Credit",100))

# Update Data
# cursor.execute("ALTER TABLE users RENAME COLUMN email to phone_number")
# cursor.execute(f"UPDATE users SET password = ? WHERE account_number = ?", ( 1, 1))

# Add a column
# cursor.execute("ALTER TABLE transfers ADD COLUMN date TEXT")

# Delete Data
cursor.execute("DELETE FROM user_expenses WHERE expenses_id > 269",())

# cursor.execute(f"SELECT * FROM users WHERE id = ?", (1,))
# user = cursor.fetchone()
#
# print(user)

# Drop Table
# cursor.execute("DROP TABLE IF EXISTS transfers")

#Confirm and save data into DataBase
conn.commit()

# Close connection
conn.close()


