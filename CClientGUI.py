from protocol import *
from CClientBL import *
from Login import *

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
        self._entry_Port = PORT
        self._entry_IP = socket.gethostbyname(socket.gethostname())

        self.login_page = None


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
            text_color="white"
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        # Currency/Balance display
        self.balance_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Balance: {self._balance}₪",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.balance_label.pack(pady=20)

        self.login_button = ctk.CTkButton(
            self.main_frame,
            text = "Login",
            width=110,
            height=30,
            border_width=2,
            fg_color= self.primary_color,
            command= self.open_login_page

        )
        self.login_button.place(relx=0.99, rely=0.01, anchor="ne")

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


    def open_login_page(self):

        # def callback_login(data):


        self.main_frame.pack_forget()
        if self.login_page == None:
            self.login_page = CLogin(self.root,self.main_frame, 1)
            self.login_page.run()
        else:
            self.login_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)



    def run(self):
        self._client_socket = threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.create_ui()
        self.root.mainloop()



if __name__ == "__main__":
    client = CClientGUI(CLIENT_HOST, PORT)
    client.run()
