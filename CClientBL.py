from protocol import *


class CClientBL:

    def __init__(self, host: str, port: int):

        self._client_socket = None
        self._host = host
        self._port = port
        self._balance = None

    def connect_to_server(self):
        try:
            self._client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._client_socket.connect((CLIENT_HOST,PORT))
            write_to_log(f"[Client] connected to server {CLIENT_HOST}")

            self.get_balance()
            write_to_log(f"[Client] balance: {self._balance}")

        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))


    def get_balance(self):
        self.send_data("GET_AMOUNT",None)
        self._balance = int(self.receive_data())

    def send_data(self, cmd, args):
        try:
            request = create_request_msg(cmd,args)
            self._client_socket.send(request.encode())
            write_to_log(f"[Client] send to server '{request}'")
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

if __name__ == "__main__":
    pass