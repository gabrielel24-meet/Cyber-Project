from protocol import *

login_cmd = ["LOGIN"]

def create_response_msg_DB(cmd, args):
    response = ""

    if cmd == "LOGIN":
        response = login(args)

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
        if (data["email"] == user[3] and data["password"] == user[4] and data["account_number"] == user[5]):
            return str(user)
        else:
            return "Error"



if __name__ == "__main__":
    print(login({'first_name': '', 'last_name': '', 'id': '1', 'email': 'geliav2008@gmail.com', 'password': '1111', 'account_number': '1'}))
