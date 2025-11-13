from protocol import *


class CClientBL:

    def __init__(self, host: str, port: int):

        self._client_socket = None
        self._host = host
        self._port = port
    def connect_to_server(self):
        try:
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((CLIENT_HOST,PORT))
            write_to_log(f"[Client] connected to server {CLIENT_HOST}")
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))


if __name__ == "__main__":
    pass