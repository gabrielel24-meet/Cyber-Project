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

            self._client_socket.send("GET_AMOUNT".encode())
            self._balance = self._client_socket.recv(1024)
            write_to_log(self._balance)
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))


if __name__ == "__main__":
    pass