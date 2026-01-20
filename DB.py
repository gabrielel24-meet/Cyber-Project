import sqlite3

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

# cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
#         id TEXT PRIMARY KEY,
#         expense_type TEXT NOT NULL,
#         payment_type TEXT NOT NULL,
#         expense_amount REAL,
#         FOREIGN KEY (id) REFERENCES users(id)
#     );
#     """)

# Insert data record
# cursor.execute("""INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#                ("3", "bobby", "boten", "3","3",3,0))

cursor.execute("""INSERT INTO expenses (id, expense_type, payment_type, expense_amount) VALUES (?, ?, ?, ?)""",
               ("1", "Food","Cash",50))

# Update Data
# cursor.execute("ALTER TABLE users RENAME COLUMN email to phone_number")
# cursor.execute(f"UPDATE users SET password = ? WHERE account_number = ?", ( 1, 1))

# Delete Data
# cursor.execute("DELETE FROM users WHERE id = ?",(10,))

#Confirm and save data into DataBase
conn.commit()

# Close connection
conn.close()