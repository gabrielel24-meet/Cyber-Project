from protocol import *
import socket
class CServerBL:

#gabababababa
    def __init__(self, host, port):

        self._host = host
        self._port = port
        self._server_socket = None
        self._is_srv_running = True
        self._client_handlers: {str : (threading.Thread,Event)} = {}

    def start_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(5)
            write_to_log(f"[SERVER_BL] listening...")

            while self._is_srv_running and self._server_socket is not None:
                # Accept socket request for connection
                client_socket, address = self._server_socket.accept()
                write_to_log(f"[SERVER_BL] Client connected {client_socket}{address} ")

                # Start Thread
                cl_handler = CClientHandler(client_socket, address)
                cl_handler.start()
                stop_event = threading.Event()
                self._client_handlers[address] = (cl_handler,stop_event)

                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {threading.active_count() - 1}")

        except Exception as e:
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
        try:
            cmd = self._client_socket.recv(1024).decode()
            if cmd == "GET_AMOUNT":
                self._client_socket.send(2000).encode()

        except Exception as e:
            self._client_socket.close()
            write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")