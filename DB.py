import sqlite3

# Connect to DB (if it doesn't exist it will be created)
conn = sqlite3.connect("Bank.db")

# Create object "cursor" to execute SQL-queries
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE users (
#         id TEXT PRIMARY KEY,
#         first_name TEXT NOT NULL,
#         last_name TEXT NOT NULL,
#         email TEXT UNIQUE,
#         password TEXT NOT NULL,
#         account_number TEXT NOT NULL,
#         balance REAL DEFAULT 0
#     );
#     """)

# Insert data record
cursor.execute("""INSERT INTO users (id, first_name, last_name, email, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
               ("1", "gabi", "eliav", "geliav2008@gmail.com","1111",1,1000))
#Confirm and save data into DataBase
conn.commit()

# Close connection
conn.close()