import logging
import threading
from threading import Event
import customtkinter as ctk
from datetime import datetime
import socket

from numpy.random import standard_t

clients :{str:(threading.Thread,Event)} = {}

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 8822
BUFFER_SIZE: int = 1024
DISCONNECT_MSG = "bye"

LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

standard_cmd = ["GET_AMOUNT"]

def write_to_log(msg):
    logging.info(msg)
    print(msg)


def check_cmd(cmd) -> int:
    if cmd in standard_cmd:
        return 1
    return -1


def create_response_msg(cmd):
    response = ""

    if cmd == "GET_AMOUNT":
        response = get_balance()

    return response

def get_balance():
    return "2000"
