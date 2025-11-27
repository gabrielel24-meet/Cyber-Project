from protocol import *
from CClientBL import *

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CLogin:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("Purple Trust Bank")
        self.root.geometry("700x500")

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

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bank name header
        self.Login_label = ctk.CTkLabel(
            self.main_frame,
            text="Login",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.Login_label.pack(pady=(40, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="white"
        )
        self.time_label.place(relx=0.99, rely=0.0, anchor="ne")

        self.Email_frame = ctk.CTkFrame(self.root)

        self.email_label
        self.email_box = ctk.CTkTextbox(
            self.main_frame,
            width=200,
            height=15,
            border_width=2,
            wrap=

        )

        self.email_box.pack()

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

    def run(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    client = CLogin()
    client.run()
