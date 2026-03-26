from protocol_DB import *
from protocol import *


class CServerBL:

    def __init__(self, host, port):

        self._host = host
        self._port = port

        self._server_socket = None
        self.stop_event = threading.Event()
        self._is_srv_running = True


    def start_server(self):
        try:
            global clients_data
            global client_handlers
            clients_data = {}
            client_handlers = {}
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(5)
            self._server_socket.settimeout(1.0)
            write_to_log(f"[SERVER_BL] listening...")

            while self._is_srv_running and not self.stop_event.is_set():
                try:
                    client_socket, address = self._server_socket.accept()
                except socket.timeout:
                    continue
                except Exception as e:
                    break

                write_to_log(f"[SERVER_BL] Client {address} connected ")
                client_socket.send("True".encode())

                # Set encryption
                private_key, public_key = self.generate_rsa_keys()
                public_pem = self.public_key_to_pem(public_key)
                client_socket.send(public_pem)
                write_to_log(f"[SERVER_BL] Public key sent to client")

                encrypted_session_key = client_socket.recv(1024)
                session_key = self.decrypt_session_key(private_key,encrypted_session_key)
                write_to_log(f"[SERVER_BL] Session key received and decrypted")

                # Start Thread
                cl_handler = CClientHandler(self._host, self._port, client_socket, address, session_key)
                cl_handler._client_thread.start()
                client_handlers[address] = cl_handler

                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {len(client_handlers)}")

        except Exception as e:
            write_to_log("[SERVER_BL] Exception in start_server fn : {}".format(e))

    def stop_server(self):
        self.stop_event.set()
        self._server_socket.close()
        for address in client_handlers:
            fernet = client_handlers[address].fernet
            client_handlers[address]._client_socket.send(fernet.encrypt('("CLOSE","False")'.encode()))
            client_handlers[address].stop()
            write_to_log(f"[SERVER_BL] Thread closed for : {address} ")

    def generate_rsa_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def public_key_to_pem(self, public_key):
        public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return public_pem

    def decrypt_session_key(self, private_key, encrypted_session_key):
        session_key = private_key.decrypt(encrypted_session_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return session_key



class CClientHandler():
    _client_socket = None
    _address = None
    _client_thread = None
    host = None
    port = None

    def __init__(self, host, port, client_socket, address, session_key):

        self._client_socket = client_socket
        self._address = address
        self._client_thread = threading.Thread(target=self.run)
        self.host = host
        self.port = port
        self.session_key = session_key
        self.fernet = Fernet(self.session_key)


    def run(self):
        #This code run in separate thread for every client
        # try:
            while True:
                cmd, args = self.receive_data(self._address)

                if check_cmd(cmd) == 1:
                    response = create_response_msg(cmd,args)
                elif check_cmd(cmd) == 2:
                    response = create_response_msg_DB(cmd, args)
                else:
                    response = "Non-supported cmd"

                if cmd == "LOGIN" and response[0] == True:
                    clients_data[self._address] = response[1]
                    self.send_data(cmd,response,self._address)
                elif cmd == "TRANSFER" and response[0] == True:
                    self.notify_transfer(response[1])
                else:
                    self.send_data(cmd, response, self._address)
        # except Exception as e:
        #     self._client_socket.close()
        #     write_to_log(f"[SERVER_BL] error - '{e}'")
        #     write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")


    def send_data(self, cmd, args, address):
       protocol_send_data(cmd, args, self._client_socket, self.fernet, )
       write_to_log(f"[SERVER_BL] send to {address}: {cmd} > {args}")

    def receive_data(self, address) -> tuple:
        cmd, args = protocol_receive_data(self._client_socket, self.fernet,)
        write_to_log(f"[SERVER_BL] received from {address}: {cmd} > {args}")
        return cmd, args


    def notify_transfer(self, data):
        # try:
            current = data["source"]
            destination = data["destination"]
            amount = data["amount"]

            response = amount, destination
            self.send_data("TRANSFER-1", response, self._address)

            for address, client in clients_data.items():
                if client[5] == destination:
                    destination_ip = address
                    response = amount, current
                    destination_fernet = client_handlers[destination_ip].fernet
                    destination_socket = client_handlers[destination_ip]._client_socket
                    protocol_send_data("TRANSFER-2", response, destination_socket, destination_fernet)
                    write_to_log(f"[SERVER_BL] send to {address}: {"TRANSFER-2"} > {response}")

        # except Exception as e:
        #     self.send_data("TRANSFER-1", "Error", self._address)
        #     write_to_log(f"[SERVER_BL] Error on notify_transfer: {e}")



    def stop(self):
        self._client_socket.close()
        self._client_thread.join()
