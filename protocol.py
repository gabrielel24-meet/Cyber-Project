import logging
import threading
from threading import Event
import customtkinter as ctk
from datetime import datetime
import socket

clients :{str:(threading.Thread,Event)} = {}

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "192.168.1.100"
PORT: int = 8822
BUFFER_SIZE: int = 1024
DISCONNECT_MSG = "bye"

LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

def write_to_log(msg):
    logging.info(msg)
    print(msg)
