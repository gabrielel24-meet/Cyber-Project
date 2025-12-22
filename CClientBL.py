import time

from protocol import *


class CClientBL:

    def __init__(self, host: str, port: int):

        self._client_socket = None
        self._host = host
        self._port = port

        self.first_name = None
        self.last_name = None
        self.id = None
        self.phone_number = None
        self.password = None
        self.account_number = None
        self.balance = None

    def connect_to_server(self):
        try:
            self._client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._client_socket.connect((self._host,self._port))
            write_to_log(f"[Client] connected to server {CLIENT_HOST}")

        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))


    def get_balance(self,):
        self.send_data("GET_BALANCE",self.account_number)
        self.balance = float(self.receive_data())

    def send_data(self, cmd, args):
        try:
            request = create_request_msg(cmd,args)
            self._client_socket.send(request.encode())
            write_to_log(f"[CLIENT_BL] send to server '{request}'")
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on send_data: {}".format(e))
            return False

    def receive_data(self) -> str:
        try:
            msg = self._client_socket.recv(1024).decode()
            write_to_log(f"[CLIENT_BL] received {msg} ")
            return msg
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on receive: {}".format(e))
            return "Error"

    def update_user_data(self,data):
        self.id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.phone_number = data[3]
        self.password = data[4]
        self.account_number = data[5]
        self.balance = data[6]
        print(self.balance)

    def transfer_money(self, current_account_number, destination_account_number, amount):
        self.send_data("TRANSFER",(current_account_number,destination_account_number ,amount))
        write_to_log(self.receive_data())
        self.get_balance()


if __name__ == "__main__":
    pass