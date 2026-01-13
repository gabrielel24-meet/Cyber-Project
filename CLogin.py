from protocol import *
from CClientBL import *
from CRegister import *
# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CLogin:

    def __init__(self, root, previous_page, callback_login, callback_register):

        self.root = root
        self.root.title("Purple Trust Bank")
        self.root.geometry("1000x700")

        self.previous_page = previous_page
        self.callback_login = callback_login
        self.callback_register = callback_register

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        self.register_page = None

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
            text_color="#ada6b3"
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        self.register_button = ctk.CTkButton(
            self.main_frame,
            text="sign up",
            width=110,
            height=30,
            border_width=2,
            fg_color=self.primary_color,
            command=self.open_register_page

        )
        self.register_button.place(relx=0.99, rely=0.01, anchor="ne")


        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="back",
            font = ("Arial", 16, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color="white",
            width=0,
            command=self.open_previous_page

        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="nw")


        self.first_name_entry = self.create_entry(self.main_frame, "First Name",0.2,0.2)
        self.last_name_entry = self.create_entry(self.main_frame, "Last Name",0.2,0.4)
        self.id_entry = self.create_entry(self.main_frame, "ID",0.2,0.6)

        self.phone_number_entry = self.create_entry(self.main_frame, "Phone Number",0.6, 0.2)
        self.password_entry = self.create_entry(self.main_frame, "Password",0.6, 0.4)
        self.account_number_entry = self.create_entry(self.main_frame, "Account Number",0.6, 0.6)

        self.submit_button = ctk.CTkButton(
            self.main_frame,
            text="Submit",
            width=150,
            height=40,
            font=("Arial",25),
            border_width=2,
            fg_color=self.primary_color,
            command=self.on_click_login,
        )

        self.submit_button.place(relx=0.45,rely=0.8)

        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
        )
        self.connection_status.pack()
        self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()

    def create_entry(self, parent, label_text, x,y):
        frame = ctk.CTkFrame(parent, fg_color=self.secondary_color)
        frame.place(relx=x, rely=y)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 15, "bold"),
        )
        label.pack(anchor="w", padx=10)

        textbox = ctk.CTkEntry(
            frame,
            width=220,
            height=25,
            border_width=1,
        )
        textbox.pack()

        return textbox

    def open_previous_page(self):
        self.main_frame.pack_forget()
        self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)

    def open_register_page(self):
        self.main_frame.pack_forget()

        if self.register_page == None:
            self.register_page = CRegister(self.root, self.main_frame, self.callback_register)
            self.register_page.run()
        else:
            self.register_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def run(self):
        self.create_ui()
        self.root.mainloop()

    def on_click_login(self):
        data = {"first_name": self.first_name_entry.get(),
                "last_name":self.last_name_entry.get(),
                "id": self.id_entry.get(),
                "phone_number": self.phone_number_entry.get(),
                "password": self.password_entry.get(),
                "account_number":self.account_number_entry.get()}

        self.callback_login(data)



if __name__ == "__main__":
    pass
