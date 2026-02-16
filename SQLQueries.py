import sqlite3
conn = sqlite3.connect("Bank.db")
cursor = conn.cursor()
rows = conn.execute("SELECT * FROM user_expenses WHERE id = 1").fetchall()
# rows = conn.execute("SELECT * FROM users").fetchall()
for row in rows:
    print(row)