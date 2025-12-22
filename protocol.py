import logging
import threading
from threading import Event
import customtkinter as ctk
from datetime import datetime
import socket
import sqlite3
import ast
from protocol_DB import *

clients :{str:(threading.Thread,Event)} = {}

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 8822
BUFFER_SIZE: int = 1024
DISCONNECT_MSG = "bye"

LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

standard_cmd = ["GET_AMOUNT","TRANSFER"]

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

    if cmd == "GET_AMOUNT":
        response = get_balance()
    elif cmd == "TRANSFER":
        response = transfer()

    return response

def get_cmd_and_args(request):
    """Returns the command from buffer"""
    split_request = request.split(">")
    cmd = split_request[0]
    args = split_request[1]

    return cmd, args

def get_balance():
    return "2000"

def transfer(data):
    data = ast.literal_eval(data)

    previous = data[0]
    destination = data[1]
    amount = data[2]

    conn = sqlite3.connect("Bank.db")
    cursor = conn.cursor()


if __name__ == "__main__":
    print(transfer("('eee', 'sss', 123)"))