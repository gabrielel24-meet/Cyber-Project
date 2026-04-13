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
        self.yearly_data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Food': [0,0,0,0,0,0,0,0,0,0,0,0],
            'Clothes': [0,0,0,0,0,0,0,0,0,0,0,0],
            'Gadgets': [0,0,0,0,0,0,0,0,0,0,0,0],
            'Gifts': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Other': [0,0,0,0,0,0,0,0,0,0,0,0]
        }


        self.responses_flag = (False, None)
        self.login_successfully_flag = None
        self.face_matches = False
        self.id_exists = False
        self.transactions = None



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


                    server_handler = threading.Thread(target=self.handle_responses, daemon=True)
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
                elif cmd == "LOGIN-1":
                    self.update_user_data(response)
                elif cmd == "LOGIN-2":
                    self.update_face_id_login_data(response)
                elif cmd == "CHECK_ID":
                    self.update_id_login(response)
                elif cmd == "REGISTER":
                    self.handle_register(response)
                elif cmd == "TRANSFER-1":
                    self.transfer_money(response)
                elif cmd == "TRANSFER-2":
                    self.receive_money(response)
                elif cmd == "EXPENSES-1":
                    self.update_expenses(response)
                elif cmd == "EXPENSES-2":
                    self.update_expenses(response)
                elif cmd == "TRANSACTIONS":
                    self.update_transactions(response)
                    self.update_right_panel()

        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on handle_responses: {}".format(e))
            self.connection_status = False
            return False


    def update_balance(self,data):
        self.balance = float(data)

    def update_transactions(self, data):
        self.transactions = data
        self.responses_flag = (True, "TRANSACTIONS")

    def send_data(self, cmd, args):
       protocol_send_data(cmd, args, self._client_socket, self.fernet)
       write_to_log(f"[CLIENT_BL] send to server {cmd} > {args}")

    def receive_data(self) -> tuple:
        cmd, args = protocol_receive_data(self._client_socket, self.fernet)
        write_to_log(f"[CLIENT_BL] received {cmd} > {args} ")
        return cmd,args


    def update_user_data(self,data):
        write_to_log(data)
        flag = data[0]
        if flag:
            account_data = data[1]
            self.login_successfully_flag = True
            self.id = account_data[0]
            self.first_name = account_data[1]
            self.last_name = account_data[2]
            self.phone_number = account_data[3]
            self.password = account_data[4]
            self.account_number = account_data[5]
            self.balance = account_data[6]


    def update_face_id_login_data(self, data):
        flag = data[0]

        if flag:
            account_data = data[1]
            self.login_successfully_flag = True
            self.id = account_data[0]
            self.first_name = account_data[1]
            self.last_name = account_data[2]
            self.phone_number = account_data[3]
            self.password = account_data[4]
            self.account_number = account_data[5]
            print(type(self.account_number))
            self.balance = account_data[6]

            self.face_matches = True
            self.responses_flag = (True, "LOGIN-2")
        else:
            self.responses_flag = (True, "LOGIN-2")

    def update_id_login(self, data):
        self.id_exists = data
        self.responses_flag = (True, "CHECK_ID")

    def transfer_money(self, data):
        amount = data[0]
        destination = data[1]
        write_to_log(f"[CLIENT_BL] transferred {amount}₪ to client {destination}")

        self.send_data("GET_BALANCE", self.account_number)
        self.responses_flag = (True, "TRANSFER")

    def receive_money(self, data):
        amount = data[0]
        source = data[1]
        write_to_log(f"[CLIENT_BL] Received {amount}₪ from client {source}")

        self.send_data("GET_BALANCE", self.account_number)
        self.responses_flag = (True, "TRANSFER")

    def handle_register(self, response):
        message = response[1]
        self.responses_flag = (True, message)

    def update_expenses(self, response):
        # self.sizes = []
        # self.labels = []
        self.yearly_data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Food': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Clothes': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Gadgets': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Gifts': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'Other': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        dictionary = {"Food":0, "Clothes":0, "Gadgets":0, "Gifts":0,"Other":0}

        # Expense: (expense_id, expense_type, payment_type, expense_amount, month, year)
        for expense in response:
            expense_type = expense[1]
            expense_amount = expense[3]
            dictionary[expense_type] += expense_amount

        # for key in dictionary:
        #     if dictionary[key] > 0:
        #         self.sizes.append(dictionary[key])
        #         self.labels.append(key)

        for expense in response:
            expense_month = expense[4]
            month_index = self.yearly_data['Month'].index(expense_month)
            expense_type = expense[1]
            expense_amount = expense[3]

            self.yearly_data[expense_type][month_index] += expense_amount

if __name__ == "__main__":
    pass