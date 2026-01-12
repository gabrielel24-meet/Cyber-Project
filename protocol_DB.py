import random

from protocol import *


login_cmd = ["LOGIN", "REGISTER"]
register_cmd = ["ID_PHONE_TAKEN", "ID_TAKEN", "PHONE_TAKEN", "REGISTERED"]


def create_response_msg_DB(cmd, args):
    response = ""

    if cmd == "LOGIN":
        response = login(args)
    if cmd == "REGISTER":
        response = register(args)
    return response


def login(data):
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()

    data = ast.literal_eval(data)
    id = data["id"]

    cursor.execute(f"SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()

    if user == None:
        return "None"
    else:
        if (data["phone_number"] == user[3] and data["password"] == user[4] and data["account_number"] == user[5]):
            return True, user
        else:
            return False, "Error"

def register(data):

        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
        data = ast.literal_eval(data)
        cursor.execute("SELECT id, phone_number, account_number FROM users")
        rows = cursor.fetchall()

        for row in rows:
            if row[0] == data["id"] and row[1] == data["phone_number"]:
                return False, "ID_PHONE_TAKEN"
            if row[0] == data["id"]:
                return False, "ID_TAKEN"
            if row[1] == data["phone_number"]:
                return False, "PHONE_TAKEN"

        account_numbers = []
        for row in rows:
            account_numbers.append(row[2])
        account_number = str(random.randint(1,1000))

        while account_number in account_numbers:
            account_number = str(random.randint(1, 6))

        id1,first,last,phone,password = data["id"], data["first_name"], data["last_name"], data["phone_number"], data["password"]

        cursor.execute(
            """INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (id1,first,last,phone,password, account_number,0))

        conn.commit()
        return True, "REGISTERED"



if __name__ == "__main__":
    data = "{'first_name': 'aaa', 'last_name': 'aaa', 'id': '11', 'phone_number': '90', 'password': '1111', }"
    print(register(data))
