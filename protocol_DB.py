import random

from protocol import *


login_cmd = ["LOGIN","REGISTER"]

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
    flag = True

    while flag:
        try:
            conn = sqlite3.connect("Bank.db")
            cursor = conn.cursor()

            data = ast.literal_eval(data)
            account_number = random.randint(1, 10)
            print(account_number)

            id1,first,last,phone,passw = data["id"], data["first_name"], data["last_name"], data["phone_number"], data["password"]

            cursor.execute(
                """INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (id1,first,last,phone,passw, account_number,0))

            conn.commit()
            flag = False

        except Exception as e:
            print(e)


if __name__ == "__main__":
    data = "{'first_name': 'aaa', 'last_name': 'aaa', 'id': '101', 'phone_number': '11', 'password': '1111', }"
    register(data)
