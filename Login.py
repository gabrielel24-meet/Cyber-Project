from protocol import *
from CClientBL import *

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CLogin:

    def __init__(self, root, previous_page):

        self.root = root
        self.root.title("Purple Trust Bank")
        self.root.geometry("1000x700")

        self.previous_page = previous_page

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
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        self.home_button = ctk.CTkButton(
            self.main_frame,
            text="Home",
            width=110,
            height=30,
            border_width=2,
            fg_color=self.primary_color,
            command=self.open_home_page

        )
        self.home_button.place(relx=0.99, rely=0.01, anchor="ne")


        self.first_name_box = self.create_textbox(self.main_frame, "First Name",0.2,0.2)
        self.last_name_box = self.create_textbox(self.main_frame, "Last Name",0.2,0.4)
        self.id_box = self.create_textbox(self.main_frame, "ID",0.2,0.6)

        self.email_box = self.create_textbox(self.main_frame, "Email",0.6, 0.2)
        self.password_box = self.create_textbox(self.main_frame, "Password",0.6, 0.4)
        self.account_number_box = self.create_textbox(self.main_frame, "Account Number",0.6, 0.6)

        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
        )
        self.connection_status.pack()
        self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()

    def create_textbox(self, parent, label_text, x,y):
        frame = ctk.CTkFrame(parent, fg_color=self.secondary_color)
        frame.place(relx=x, rely=y)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 15, "bold"),
        )
        label.pack(anchor="w", padx=10)

        textbox = ctk.CTkTextbox(
            frame,
            width=220,
            height=15,
            border_width=2,
        )
        textbox.pack()

        return textbox

    def open_home_page(self):
        self.main_frame.pack_forget()
        self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def run(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    Login_page = CLogin(ctk.CTk(),ctk.CTkFrame())
    Login_page.run()
