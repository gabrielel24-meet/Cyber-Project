import sqlite3

# Connect to DB (if it doesn't exist it will be created)
conn = sqlite3.connect("Bank.db")

# Create object "cursor" to execute SQL-queries
cursor = conn.cursor()

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

# Insert data record
cursor.execute("""INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
               ("3", "bobby", "boten", "3","3",3,0))

# Update Data
# cursor.execute("ALTER TABLE users RENAME COLUMN email to phone_number")
# cursor.execute(f"UPDATE users SET balance = ? WHERE account_number = ?", ( 3000, 2))


#Confirm and save data into DataBase
conn.commit()

# Close connection
conn.close()