import threading
import time
from protocol import *
from CClientBL import *
from CLogin import *
from CRegister import *


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CClientGUI(CClientBL):

    def __init__(self, host, port):

        super().__init__(host, port)

        self.root = ctk.CTk()
        self.root.title("Purple Trust Bank")
        self.root.geometry("1000x700")

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        # Time updating thread
        self.time_thread = threading.Thread(target=self.update_time, daemon=True)
        self.time_label = None
        
        # Client's IP and port
        self._entry_Port = port
        self._entry_IP = host

        self.login_page = None

        self.destination_user_frame = None
        self.transfer_amount_frame = None

        self.check_for_responses_thread = threading.Thread(target=self.check_for_responses)

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bank name header
        self.bank_name_label = ctk.CTkLabel(
            self.main_frame,
            text="PURPLE TRUST BANK",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.bank_name_label.pack(pady=(40, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="#ada6b3"
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        # Currency/Balance display
        self.balance_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Balance: {self.balance}₪",
            font=("Arial", 20, "bold"),
            text_color="white"
        )

        self.login_button = ctk.CTkButton(
            self.main_frame,
            text = "sign in",
            width=110,
            height=30,
            border_width=2,
            fg_color= self.primary_color,
            command= self.open_login_page

        )
        self.login_button.place(relx=0.99, rely=0.01, anchor="ne")


        # Transfer Button
        self.transfer_button = ctk.CTkButton(
            self.main_frame,
            text="Transfer",
            width=110,
            height=30,
            border_width=1,
            fg_color=self.primary_color,
            command=self.on_click_open_transfer

        )

        self.destination_user_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.destination_user_label = ctk.CTkLabel(self.destination_user_frame, text="Transfer destination account", font=("Arial", 15, "bold"))
        self.destination_user_entry = ctk.CTkEntry(self.destination_user_frame, width=220, height=25, border_width=1)
        self.error_message = ctk.CTkLabel(self.destination_user_frame,text="can't transfer to yourself")

        self.destination_user_label.pack(anchor="w", padx=10)
        self.destination_user_entry.pack()

        self.transfer_amount_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.transfer_amount_label = ctk.CTkLabel(self.transfer_amount_frame, text="Amount", font=("Arial", 15, "bold"))
        self.transfer_amount_entry = ctk.CTkEntry(self.transfer_amount_frame, width=220, height=25, border_width=1)

        self.transfer_amount_label.pack(anchor="w", padx=10)
        self.transfer_amount_entry.pack()

        self.on_click_transfer = ctk.CTkButton(
            self.main_frame,
            text="Transfer Money",
            font = ("Arial", 15, "bold"),
            width=130, height=40,
            border_width=1,
            fg_color= "blue",
            command= self.on_click_transfer_money
        )


        # Connection Status
        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
        )
        self.connection_status.pack()
        self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()


    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def check_for_responses(self):
        flag,cmd = self.responses_flag
        if flag == True:
            if cmd == "TRANSFER-2":
                self.update_balance_label()
            elif cmd == "ID_PHONE_TAKEN":
                self.update_register_page(cmd)
            flag = False
        self.root.after(1000,self.check_for_responses)

    def open_login_page(self):

        def callback_login(data):
            write_to_log(f"[Client GUI] Received data from Login window: {data}")
            self.send_data("LOGIN", data)
            time.sleep(0.1)
            self.bank_name_label.configure(text=f"Hi {self.first_name} {self.last_name}")
            self.balance_label.pack(pady=20)
            self.show_page(self.main_frame, self.login_page.main_frame)
            self.update_balance_label()
            self.login_button.place_forget()
            self.transfer_button.pack()
            self.check_for_responses_thread.start()

        def callback_register(data):
            write_to_log(f"[Client GUI] Received data from Register window: {data}")
            self.send_data("REGISTER", data)
            time.sleep(0.1)


        self.main_frame.pack_forget()
        if self.login_page == None:
            self.login_page = CLogin(self.root,self.main_frame, callback_login, callback_register)
            self.login_page.run()
        else:
            self.login_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)


    def show_page(self, next_frame, previous_frame):
        next_frame.pack(fill="both", expand=True, padx=20, pady=20)
        previous_frame.pack_forget()

    def update_balance_label(self):
        self.balance_label.configure(text=f"Balance: {self.balance}₪")

    def update_register_page(self, data):
        self.login_page.register_page.show_taken_data_label(data)

    def on_click_open_transfer(self):
        self.destination_user_frame.pack(pady = 20)
        self.transfer_amount_frame.pack()
        self.transfer_button.configure(command=self.on_click_close_transfer, text="Cancel Transfer")
        self.on_click_transfer.pack(pady = 10)

    def on_click_close_transfer(self):
        self.destination_user_frame.pack_forget()
        self.transfer_amount_frame.pack_forget()
        self.transfer_button.configure(command=self.on_click_open_transfer, text="Transfer")
        self.on_click_transfer.pack_forget()

    def on_click_transfer_money(self):
        if self.destination_user_entry.get() != self.account_number:
            self.error_message.pack_forget()
            self.send_data("TRANSFER",(self.account_number ,self.destination_user_entry.get(), int(self.transfer_amount_entry.get())))
            self.on_click_close_transfer()
            time.sleep(0.1)
            self.update_balance_label()
        else:
            self.error_message.pack(anchor="w")

    def run(self):
        self._client_socket = threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    client = CClientGUI(CLIENT_HOST, PORT)
    client.run()

