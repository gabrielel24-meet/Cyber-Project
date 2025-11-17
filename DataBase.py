import sqlite3

# Connect to DB (if it doesn't exist it will be created)
conn = sqlite3.connect("Bank.db")

# Create object "cursor" to execute SQL-queries
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Bank (id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Amount INTEGER NOT NULL)""")

# Insert data record
cursor.execute("""INSERT INTO Bank (Name, Amount) VALUES (?, ?)""", ("geliav2008@gmail.com", 1234))


#Confirm and save data into DataBase
conn.commit()

# Close connection
conn.close()