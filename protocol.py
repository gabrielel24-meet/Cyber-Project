import logging
import threading
from threading import Event
import customtkinter as ctk
from datetime import datetime
import socket
import time
import sqlite3
import ast
from protocol_DB import *
import random
import matplotlib.pyplot as plt


clients :{str:(threading.Thread,Event)} = {}

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 8822
BUFFER_SIZE: int = 1024
DISCONNECT_MSG = "bye"


LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

standard_cmd = ["GET_BALANCE","TRANSFER","EXPENSES"]

def write_to_log(msg):
    logging.info(msg)
    print(msg)


def check_cmd(cmd) -> int:
    if cmd in standard_cmd:
        return 1
    elif cmd in login_cmd:
        return 2
    return -1


def create_request_msg(cmd,args):
    request = ""
    if check_cmd(cmd) == 1:
        request = f"{cmd}>{args}"
    elif check_cmd(cmd) == 2:
        request = f"{cmd}>{args}"

    return request


def create_response_msg(cmd,args):
    response = ""

    if cmd == "GET_BALANCE":
        response = get_balance(args)
    elif cmd == "TRANSFER":
        response = transfer(args)
    elif cmd == "EXPENSES":
        response = expenses(args)

    return response

def get_cmd_and_args(request):
    split_request = request.split(">")
    cmd = split_request[0]
    args = split_request[1]

    return cmd, args

def get_balance(account_number):
    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE account_number = ?",(account_number,))
    balance = cursor.fetchone()[0]
    conn.close()

    return balance


def transfer(data):
    try:
        data = ast.literal_eval(data)
        current = data[0]
        destination = data[1]
        amount = data[2]

        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT balance FROM users WHERE account_number = ?", (current,))
        current_balance = cursor.fetchone()[0]

        cursor.execute(f"SELECT balance FROM users WHERE account_number = ?", (destination,))
        destination_balance = cursor.fetchone()[0]

        cursor.execute(f"UPDATE users SET balance = ? WHERE account_number = ?",((current_balance - amount),current))
        cursor.execute(f"UPDATE users SET balance = ? WHERE account_number = ?",(destination_balance + amount,destination))
        conn.commit()
        conn.close()


        return True , {"source":current, "destination":destination, "amount":amount}

    except Exception as e:
        return False ,f"{e}"


def expenses(data):
    try:
        data = ast.literal_eval(data)
        conn = sqlite3.connect("Bank.db")
        cursor = conn.cursor()

        id = data[0]
        expense_amount = data[1][0]
        payment_type = data[1][1]
        expense_type = data[1][2]

        cursor.execute("""INSERT INTO user_expenses (id, expense_type, payment_type, expense_amount) VALUES (?, ?, ?, ?)""",
                       (id, expense_type, payment_type, expense_amount))

        conn.commit()
        conn.close()

        return True
    except Exception as e:
        conn.close()
        write_to_log(e)
        return False


def is_positive_number(str):
    try:
        str = float(str)
        if str > 0:
            return True
        else:
            return False
    except:
        return  False



if __name__ == "__main__":
    print(expenses("(2,('Food','cash',12))"))