from protocol import *
import random
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

login_cmd = ["LOGIN-1","LOGIN-2","CHECK_ID", "REGISTER"]
register_cmd = ["ID_PHONE_TAKEN", "ID_TAKEN", "PHONE_TAKEN", "REGISTERED"]


def create_response_msg_DB(cmd, args):
    response = ""

    if cmd == "LOGIN-1":
        response = regular_login(args)
    if cmd == "LOGIN-2":
        response = face_id_login(args)
    if cmd == "CHECK_ID":
        response = check_id(args)
    if cmd == "REGISTER":
        response = register(args)

    return response


def regular_login(data):
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()

    id = data["id"]

    cursor.execute(f"SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    if user == None:
        return "None"
    else:
        phone_number = data["phone_number"]

        ph = PasswordHasher()
        password = data["password"]
        password_flag = (ph.verify(user[4],password))

        if (phone_number == user[3] and password_flag):
            return True, user
        else:
            return False, None


def face_id_login(data):
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()

    id = data["id"]

    cursor.execute(f"SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    if user == None:
        return "None"
    else:
        face_encodings = data["face_encodings"]
        face_encodings = json.loads(face_encodings)
        face_encodings = np.array(face_encodings)

        reference_encodings = user[7]
        reference_encodings = json.loads(reference_encodings)
        reference_encodings = np.array(reference_encodings)

        matches = face_recognition.compare_faces([reference_encodings], face_encodings)

        if matches[0]:
            return True, user
        else:
            return False, None


def check_id(data):
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()

    id = data["id"]

    cursor.execute(f"SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()

    if user == None:
        return False
    else:
        return True


def register(data):

        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()
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

        id1,first,last,phone,password,face_encodings = data["id"], data["first_name"], data["last_name"], data["phone_number"], data["password"], data["face_encodings"]

        ph = PasswordHasher()
        password = ph.hash(password)

        cursor.execute(
            """INSERT INTO users (id, first_name, last_name, phone_number, password, account_number, balance, face_encodings) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (id1,first,last,phone,password, account_number,0, face_encodings))

        conn.commit()
        conn.close()

        return True, "REGISTERED"



if __name__ == "__main__":
    data = "{'first_name': 'aaa', 'last_name': 'aaa', 'id': '11', 'phone_number': '90', 'password': '1111', }"
    print(register(data))
