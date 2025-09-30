from protocol import *
import socket
class CServerBL:

    def __init__(self, host, port):

        self._host = host
        self._port = port
        self._server_socket = None
        self._is_srv_running = True
        self._client_handlers = []

    def start_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(5)
            # write_to_log(f"[SERVER_BL] listening...")

            while self._is_srv_running and self._server_socket is not None:
                # Accept socket request for connection
                client_socket, address = self._server_socket.accept()
                write_to_log(f"[SERVER_BL] Client connected {client_socket}{address} ")

                # Start Thread
                cl_handler = CClientHandler(client_socket, address)
                cl_handler.start()
                self._client_handlers.append(cl_handler)
                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {threading.active_count() - 1}")

        except Exception as e:
            print(self._host)
            write_to_log("[SERVER_BL] Exception in start_server fn : {}".format(e))



class CClientHandler(threading.Thread):
    _client_socket = None
    _address = None

    def __init__(self, client_socket, address):
        super().__init__()

        self._client_socket = client_socket
        self._address = address

    def run(self):
        # This code run in separate thread for every client
        connected = True
        while connected:
            # 1. Get message from the socket and check it
            msg = self._client_socket.recv(BUFFER_SIZE).decode()
            write_to_log("[CLIENT] send - " + msg)

            response = input("Enter massage: ")
            self._client_socket.send(response.encode(1024))
            if response == DISCONNECT_MSG:
                connected = False

            self._client_socket.close()
            write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")