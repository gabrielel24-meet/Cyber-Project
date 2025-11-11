import threading

from protocol import *
from CClientBL import *

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CClientGUI(CClientBL):

    def __init__(self, host, port):

        super().__init__(host, port)

        self.root = ctk.CTk()
        self.root.title("Purple Trust Bank")
        self.root.geometry("400x300")

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        self.create_ui()

        self.time_thread = None

        self._entry_Port = PORT
        self._entry_IP = socket.gethostbyname(socket.gethostname())


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
        self.bank_name_label.pack(pady=(10, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="white"
        )
        self.time_label.pack(pady=10)

        # Currency/Balance display
        self.balance_label = ctk.CTkLabel(
            self.main_frame,
            text="Balance: $1,000.00",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.balance_label.pack(pady=20)

        # # Update time initially and start the clock
        # self.time_thread = threading.Thread(target=self.update_time)
        # self.time_thread.start()

        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
        )

        self.connection_status.pack(padx=50,pady=50)


    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def run(self):
        self._client_socket = threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.root.mainloop()
        print("Aaaa")



if __name__ == "__main__":
    client = CClientGUI(CLIENT_HOST, PORT)
    client.run()
