import threading
from base64 import encode


from protocol import *
import socket


class CServerBL:

    def __init__(self, host, port):

        self._host = host
        self._port = port
        self._server_socket = None
        self._is_srv_running = True
        self._client_handlers: {str : CClientHandler} = {}
        self._clients_data = {}


    def start_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(5)
            write_to_log(f"[SERVER_BL] listening...")

            while self._is_srv_running and self._server_socket is not None:
                # Accept socket request for connection
                client_socket, address = self._server_socket.accept()
                write_to_log(f"[SERVER_BL] Client {address} connected ")

                # Start Thread
                cl_handler = CClientHandler(self._host, self._port,client_socket, address)
                cl_handler._client_thread.start()
                stop_event = threading.Event()
                self._client_handlers[address] = cl_handler
                cl_handler._client_handlers = self._client_handlers
                cl_handler._clients_data = self._clients_data

                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {len(self._client_handlers)}")

        except Exception as e:
            write_to_log("[SERVER_BL] Exception in start_server fn : {}".format(e))

    def stop_server(self):
        for address in self._client_handlers:
            self._client_handlers[address].stop()
            write_to_log(f"[SERVER_BL] Thread closed for : {address} ")



class CClientHandler(CServerBL):
    _client_socket = None
    _address = None
    _client_thread = None
    host = None
    port = None

    def __init__(self, host, port, client_socket, address):
        super().__init__(host,  port,)

        self._client_socket = client_socket
        self._address = address
        self._client_thread = threading.Thread(target=self.run)

    def run(self):
        # This code run in separate thread for every client
        try:
            while True:
                request = self._client_socket.recv(1024).decode()
                cmd, args = get_cmd_and_args(request)

                write_to_log(f"[SERVER_BL] received from {self._address} - cmd: {cmd}, args: {args}")

                if check_cmd(cmd) == 1:
                    response = create_response_msg(cmd,args)
                elif check_cmd(cmd) == 2:
                    response = create_response_msg_DB(cmd, args)
                else:
                    response = "Non-supported cmd"

                if cmd == "LOGIN" and response[0] == True:
                    self._clients_data[self._address] = response[1]
                    response = str((cmd,response[1]))
                    self._client_socket.send(response.encode())
                    write_to_log(f"[SERVER_BL] sent '{response}'")
                elif cmd == "TRANSFER" and response[0] == True:
                    self.notify_transfer(response[1])
                else:
                    response = cmd, response
                    write_to_log(f"[SERVER_BL] sent '{response}'")
                    self._client_socket.send(str(response).encode())

        except Exception as e:
            self._client_socket.close()
            write_to_log(f"[SERVER_BL] error - '{e}'")
            write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")


    def notify_transfer(self, data):
        try:
            current = data["source"]
            destination = data["destination"]
            amount = data["amount"]

            response = str(("TRANSFER-1",f"Client {current} transferred {amount}₪ to client {destination}"))
            self._client_socket.send(response.encode())
            write_to_log(f"[SERVER_BL] sent to {current} - '{response}'")

            for address, client in self._clients_data.items():
                if client[5] == destination:
                    destination_ip = address
                    response = str(("TRANSFER-2",f"Received {amount}₪ from client {current}"))
                    self._client_handlers[destination_ip]._client_socket.send(response.encode())
                    write_to_log(f"[SERVER_BL] sent to {destination} - '{response}'")

        except Exception as e:
            self._client_socket.send(f"Error - {e}")



    def stop(self):
        self._client_socket.close()
        self._client_thread.join()
