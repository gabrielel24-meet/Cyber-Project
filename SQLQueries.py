import sqlite3
conn = sqlite3.connect("Bank.db")
cursor = conn.cursor()
rows = conn.execute("SELECT * FROM users").fetchall()
for row in rows:
    print(row)