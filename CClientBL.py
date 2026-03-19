import time

from fontTools.misc.eexec import encrypt

from protocol import *


class CClientBL:

    def __init__(self, host: str, port: int):

        self._client_socket = None
        self._host = host
        self._port = port
        self.connection_status = False

        self.first_name = None
        self.last_name = None
        self.id = None
        self.phone_number = None
        self.password = None
        self.account_number = None
        self.balance = None

        # Pie Chart data
        self.expenses = []
        self.sizes = []
        self.labels = []

        self.responses_flag = (False, None)
        self.login_successfully_flag = None


    def connect_to_server(self):
        while True:
            try:
                if self.connection_status == False:
                    # Connecting to server
                    self._client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    self._client_socket.connect((self._host, self._port))
                    write_to_log(f"[CLIENT_BL] connected to server {CLIENT_HOST}")
                    self.connection_status = ast.literal_eval(self._client_socket.recv(1024).decode())

                    # Setting encryption
                    public_pem = self._client_socket.recv(1024)
                    public_key = self.load_public_key(public_pem)
                    write_to_log("[CLIENT_BL] Public key received")

                    session_key = Fernet.generate_key()
                    self.fernet = Fernet(session_key)
                    write_to_log("[CLIENT_BL] Session key generated")

                    encrypted_session_key = self.encrypt_session_key(public_key,session_key)
                    self._client_socket.send(encrypted_session_key)
                    write_to_log("[CLIENT_BL] Encrypted session key sent to server")


                    server_handler = threading.Thread(target=self.handle_responses)
                    server_handler.start()

            except Exception as e:
                write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))
            time.sleep(1)

    def load_public_key(self, public_pem: bytes):
        public_key = serialization.load_pem_public_key(public_pem)
        return public_key

    def encrypt_session_key(self,public_key, session_key):
        encrypted_session_key = public_key.encrypt(session_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return encrypted_session_key


    def handle_responses(self):
        try:
            while True:
                cmd, response = self.receive_data()

                if cmd == "CLOSE":
                    self.connection_status = False
                elif cmd == "GET_BALANCE":
                    self.update_balance(response)
                elif cmd == "LOGIN":
                    self.update_user_data(response)
                elif cmd == "REGISTER":
                    self.handle_register(response)
                elif cmd == "TRANSFER-1":
                    self.transfer_money()
                elif cmd == "TRANSFER-2":
                    self.transfer_money()
                    self.responses_flag = (True,"TRANSFER-2")
                elif cmd == "EXPENSES-1":
                    self.update_expenses(response)
                elif cmd == "EXPENSES-2":
                    self.update_expenses(response)

        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on handle_responses: {}".format(e))
            return False


    def update_balance(self,data):
        self.balance = float(data)


    def send_data(self, cmd, args):
        try:
            request = create_request_msg(cmd, args).encode()
            encrypted_request = self.fernet.encrypt(request)
            self._client_socket.send(encrypted_request)
            write_to_log(f"[CLIENT_BL] send to server '{encrypted_request}'")
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on send_data: {}".format(e))
            return False


    def receive_data(self) -> str:
        try:
            encrypted_request = self._client_socket.recv(1024)
            request = self.fernet.decrypt(encrypted_request).decode()
            request = ast.literal_eval(request)
            write_to_log(f"[CLIENT_BL] received {request} ")
            return request
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on receive: {}".format(e))
            return "Error"

    def update_user_data(self,data):
        write_to_log(data)
        if data[1] != "Error":
            self.login_successfully_flag = True
            self.id = data[0]
            self.first_name = data[1]
            self.last_name = data[2]
            self.phone_number = data[3]
            self.password = data[4]
            self.account_number = data[5]
            self.balance = data[6]

    def transfer_money(self):
        self.send_data("GET_BALANCE",self.account_number)

    def handle_register(self, response):
        message = response[1]
        self.responses_flag = (True, message)

    def update_expenses(self, response):
        self.sizes = []
        self.labels = []
        dictionary = {"Food":0, "Clothes":0, "Gadgets":0, "Gifts":0,"Other":0}

        for expense in response:
            dictionary[expense[1]] += expense[3]

        for key in dictionary:
            if dictionary[key] > 0:
                self.sizes.append(dictionary[key])
                self.labels.append(key)

if __name__ == "__main__":
    pass