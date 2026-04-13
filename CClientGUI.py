from doctest import master

from protocol import *
from protocol_DB import *
from CClientBL import *
from CLogin import *
from CRegister import *
from CExpenses import *


class CClientGUI(CClientBL):

    def __init__(self, host, port):

        super().__init__(host, port)

        self.root = ctk.CTk()
        self.root.title("Finance Plan")
        self.root.geometry("1100x700")

        ctk.set_appearance_mode("light")
        self.is_dark_mode = False

        # Configure purple color scheme
        self.primary_color = ("#6A0DAD", "#2D1B4E")
        self.secondary_color = ("#8A2BE2", "#3E2A6D")
        self.accent_color = ("#9370DB", "#9B5DE5")
        self.text_color = "#FFFFFF"
        self.card_color = ("#a187d6", "#4B357D")  # סגול מעושן עדין
        self.rows_color = ("#D8C7F7", "#5B3B8C")  # יותר מודגש אבל רגוע

        self.hidden_secondary_color = ("#6E2DB5", "#2A1F3D")
        self.hidden_card_color = ("#E0CFFF", "#3A2A5A")
        self.hidden_rows_color = ("#D8C2F0", "#4A3475")

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        # Time updating thread
        self.time_thread = threading.Thread(target=self.update_time, daemon=True)
        self.time_label = None

        # Connection status updating thread
        self.connection_status_thread = threading.Thread(target=self.update_connection_status, daemon=True)
        self.connection_status_label = None

        # Client's IP and port
        self._entry_Port = port
        self._entry_IP = host

        # Menu
        self.menu_frame = None
        self.menu_open = False
        self.menu_img = None

        self.login_page = None
        self.expenses_page = None

        self.destination_user_frame = None
        self.transfer_amount_frame = None
        self.transaction_rows = []

        self.check_for_responses_thread = threading.Thread(target=self.check_for_responses).start()

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bank name header
        self.bank_name_label = ctk.CTkLabel(
            self.main_frame,
            text="FINANCE PLAN BANK",
            font=("Arial", 50, "bold"),
            text_color=self.text_color
        )
        self.bank_name_label.pack(pady=(80, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="#ada6b3"
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")


        # Balance display
        self.balance_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Balance: {self.balance}₪",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        # Transfer Button
        self.transfer_frame = ctk.CTkFrame(
            self.main_frame,
            # fg_color=self.secondary_color
        )
        self.cancel_transfer_button = ctk.CTkButton(
            self.transfer_frame,
            text="Cancel Transfer",
            width=110,
            height=30,
            border_width=1,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.on_click_close_transfer
        )


        self.destination_user_frame = ctk.CTkFrame(self.transfer_frame, fg_color=self.secondary_color)
        self.destination_user_label = ctk.CTkLabel(self.destination_user_frame, text="Transfer destination account", font=("Arial", 15, "bold"))
        self.destination_user_entry = ctk.CTkEntry(self.destination_user_frame, width=220, height=25, border_width=1)
        self.destination_error_message = ctk.CTkLabel(self.transfer_frame,text="can't transfer to yourself")

        self.destination_user_label.pack(anchor="w", padx=10)
        self.destination_user_entry.pack()

        self.transfer_amount_frame = ctk.CTkFrame(self.transfer_frame, fg_color=self.secondary_color)
        self.transfer_amount_label = ctk.CTkLabel(self.transfer_amount_frame, text="Amount", font=("Arial", 15, "bold"))
        self.transfer_amount_entry = ctk.CTkEntry(self.transfer_amount_frame, width=220, height=25, border_width=1)
        self.amount_error_message = ctk.CTkLabel(self.transfer_frame)

        self.destination_user_frame.place(relx=0.4, rely=0.4)
        self.transfer_amount_frame.place(relx=0.41, rely=0.55)
        self.transfer_amount_label.pack(anchor="w", padx=10)
        self.transfer_amount_entry.pack()

        self.on_click_transfer = ctk.CTkButton(
            self.transfer_frame,
            text="Transfer Money",
            font = ("Arial", 15, "bold"),
            width=130, height=40,
            border_width=1,
            fg_color= "blue",
            command= self.on_click_transfer_money
        )
        self.on_click_transfer.place(relx=0.44, rely=0.7)



        # Welcome Text
        self.welcome_frame = ctk.CTkFrame(
            self.main_frame,
            width=800,
            height=280,
            fg_color= self.secondary_color,
        )
        self.welcome_title = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome!",
            font = ("Arial", 40, "bold"),
            text_color=self.text_color,
        )
        self.welcome_text = ctk.CTkLabel(
            self.welcome_frame,
            text="Finance Plan is the first and only bank that cares for you! \n Here, our top priorities are to make sure you always know your financial situation \n & help you spend your money smarter.",
            font=("Arial", 20),
            # text_color=self.accent_color,
            text_color=self.text_color,

        )

        self.login_button = ctk.CTkButton(
            self.welcome_frame,
            text="sign in",
            width=110,
            height=30,
            border_width=2,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.open_login_page

        )
        self.welcome_title.place(relx = 0.5, rely=0.1, anchor = 'center')
        self.welcome_text.place(relx = 0.5, rely=0.4, anchor = 'center')
        if not self.login_successfully_flag:
            self.welcome_frame.place(relx = 0.5, rely=0.5, anchor = 'center')
            self.login_button.place(relx = 0.5, rely=0.75, anchor = 'center')


        image_path = "Images/bank.png"
        pil_image = Image.open(image_path)

        self.bank_img = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(100, 100)
        )

        self.bank_img_label = ctk.CTkLabel(
            self.main_frame,
            image=self.bank_img,
            text = "",
        )
        self.bank_img_label.place(relx = 0.5, rely=0.8, anchor = 'center')


        # Transactions Frame
        self.transactions_frame = ctk.CTkFrame(
            self.main_frame,
            width=350,
            fg_color=self.card_color
        )
        self.transactions_title = ctk.CTkLabel(
            self.transactions_frame,
            text="Transactions",
            text_color=self.text_color,
            font=("Arial", 22, "bold")
        )
        self.transactions_list_frame = ctk.CTkScrollableFrame(
            self.transactions_frame,
            width=400,
            height=400,
            fg_color=self.card_color

        )
        self.transactions_title.pack(pady=10)
        self.transactions_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Quick menu
        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.secondary_color,
        )

        self.user_title = ctk.CTkLabel(
            self.right_panel,
            text="User",
            font=("Arial", 25, "bold"),
            text_color=self.text_color,
        )
        self.user_name_label = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 18, "bold"),
            text_color = self.text_color,
        )
        self.account_label = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 16),
            text_color = self.text_color,
        )
        self.phone_label = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 16),
            text_color = self.text_color,
        )
        self.user_title.place(relx=0.07, rely=0.07)
        self.user_name_label.place(relx=0.07, rely=0.1)
        self.phone_label.place(relx=0.07, rely=0.2)
        self.account_label.place(relx=0.07, rely=0.3)


        self.summary_title = ctk.CTkLabel(
            self.right_panel,
            text="This Month",
            font=("Arial", 18, "bold"),
            text_color = self.text_color,
        )
        self.total_spent_label = ctk.CTkLabel(
            self.right_panel,
            text="₪0",
            font=("Arial", 16, "bold"),
            text_color = self.text_color,
        )
        self.top_category_label = ctk.CTkLabel(
            self.right_panel,
            text="Top: -",
            font=("Arial", 16),
            text_color = self.text_color,
        )
        self.quick_info = ctk.CTkLabel(
            self.right_panel,
            text="Quick Menu",
            font=("Arial", 18, "bold"),
            text_color = self.text_color,
        )
        self.last_title = ctk.CTkLabel(
            self.right_panel,
            text="Last Transaction:",
            font=("Arial", 16, "bold"),
            text_color = self.text_color,
        )
        self.last_transaction_label = ctk.CTkLabel(
            self.right_panel,
            text="-",
            font=("Arial", 15),
            text_color = self.text_color,
        )

        self.summary_title.place(relx=0.07, rely=0.5)
        self.total_spent_label.place(relx=0.07, rely=0.6)
        self.top_category_label.place(relx=0.07, rely=0.7)
        self.quick_info.place(relx=0.07, rely=0.8)
        self.last_title.place(relx=0.07, rely=0.9)
        self.last_transaction_label.place(relx=0.07, rely=0.95)



        # Connection Status
        self.connection_status_label = ctk.CTkLabel(
            self.main_frame,
            text="Not connected",
            text_color = self.text_color,
        )
        self.connection_status_label.place(relx=0.01, rely=1.0, anchor="sw")

        # Menu
        self.menu_img = ctk.CTkImage(
            light_image=Image.open("Images/menu.png"),
            dark_image=Image.open("Images/menu.png"),
            size=(25, 25)
        )

        self.menu_button = ctk.CTkButton(
            self.main_frame,
            image=self.menu_img,
            text="",
            width=30,
            fg_color="transparent",
            hover_color=self.primary_color,
            command=self.toggle_menu
        )

        self.menu_frame = ctk.CTkFrame(
            self.main_frame,
            width=0,
            fg_color=self.secondary_color,
            corner_radius=0,
        )

        self.menu_frame.place(x=0, y=0, relheight=1)

        # Close (X) button
        self.close_menu_btn = ctk.CTkButton(
            self.menu_frame,
            text="X",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=self.primary_color,
            command=self.toggle_menu
        )

        self.close_menu_btn.place(x=10, y=10)

        self.menu_title = ctk.CTkLabel(
            self.menu_frame,
            text="Menu",
            font=("Arial", 25, "bold"),
            text_color=self.text_color,
        )
        self.menu_title.place(relx = 0.4, rely = 0.07)


        # Expenses button
        self.expense_img = ctk.CTkImage(
            light_image=Image.open("Images/expenses.png"),
            dark_image=Image.open("Images/expenses.png"),
            size=(25, 25)
        )
        self.menu_expenses_btn = ctk.CTkButton(
            self.menu_frame,
            text="  Expenses",
            font=('Arial',18,"bold"),
            image=self.expense_img,
            width=250,
            height=50,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            compound="left",
            anchor="w",
            command=self.open_expenses,
        )
        self.menu_expenses_btn.place(relx = 0.05, rely = 0.2)

        # Transfer button
        self.transfer = ctk.CTkImage(
            light_image=Image.open("Images/icon2.png"),
            dark_image=Image.open("Images/icon2.png"),
            size=(25, 25)
        )
        self.menu_transfer_btn = ctk.CTkButton(
            self.menu_frame,
            text="  Transfer",
            font=('Arial', 18, "bold"),
            image=self.transfer,
            width=250,
            height=50,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            compound="left",
            anchor="w",
            command=self.on_click_open_transfer,
        )
        self.menu_transfer_btn.place(relx=0.05, rely=0.3)

        self.menu_signout_btn = ctk.CTkButton(
            self.menu_frame,
            text="Sign Out",
            width=180,
            height=40,
            fg_color="#8B0000",  # darker red for emphasis
            hover_color="#A52A2A",
            # command=self.on_click_sign_out
        )

        self.menu_signout_btn.place(relx=0.5, rely=0.95, anchor="s")


        self.time_thread.start()
        self.connection_status_thread.start()

        # Theme
        self.theme_frame = self.create_theme_switch(self.main_frame)
        self.theme_frame.place(relx=0.45, rely = 0.9)


    def create_theme_switch(self, frame):
        theme_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            text_color=self.text_color,
            command=self.toggle_theme
        )

        theme_switch.pack(anchor="w")

        return theme_frame


    def update_connection_status(self):
        if self.connection_status:
            self.connection_status_label.configure(text="connected")
        else:
            self.connection_status_label.configure(text="Not connected")

        self.root.after(1000, self.update_connection_status)


    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def toggle_menu(self):
        if not self.menu_open:
            self.open_menu()
        else:
            self.close_menu()

    def open_menu(self):
        self.main_frame.configure(fg_color=self.hidden_secondary_color)
        self.transactions_frame.configure(fg_color=self.hidden_card_color)
        self.transactions_list_frame.configure(fg_color=self.hidden_card_color)
        self.update_transaction_rows_color()
        self.transactions_title.configure(text_color="#928f94")
        self.bank_name_label.configure(text_color="#928f94")
        self.balance_label.configure(text_color="#928f94")

        self.menu_open = True
        self.menu_frame.configure(width=300)

    def close_menu(self):
        self.main_frame.configure(fg_color=self.secondary_color)
        self.transactions_frame.configure(fg_color=self.card_color)
        self.transactions_list_frame.configure(fg_color=self.card_color)
        self.update_transaction_rows_color()
        self.transactions_title.configure(text_color="white")
        self.bank_name_label.configure(text_color="white")
        self.balance_label.configure(text_color="white")

        self.menu_open = False
        self.menu_frame.configure(width=0)


    def check_for_responses(self):
        flag, cmd = self.responses_flag
        if flag == True:
            if cmd == "TRANSFER":
                self.update_balance_label()
            elif cmd in register_cmd:
                self.update_register_page(cmd)
            elif cmd == "EXPENSES-2":
                self.update_expenses_window()
            elif cmd == "LOGIN-2":
                self.update_login_page()
            elif cmd == "CHECK_ID":
                self.update_login_id_page()
            elif cmd == "TRANSACTIONS":
                self.display_transactions()

        self.responses_flag = False,None
        self.root.after(10, self.check_for_responses)

    def open_login_page(self):
        write_to_log("[CLIENT_GUI] opened Login page")
        def callback_login(data):
            write_to_log(f"[CLIENT_GUI] Received data from Login page: {data}")
            cmd, args = data
            self.send_data(cmd, args)
            time.sleep(0.1)
            if cmd == "LOGIN-1":
                if self.login_successfully_flag:
                    create_home_page()
                    self.show_page(self.main_frame, self.login_page.main_frame)
            if cmd == "LOGIN-2":
                if self.login_successfully_flag:
                    create_home_page()

        def callback_register(data):
            write_to_log(f"[CLIENT_GUI] Received data from Register page: {data}")
            self.send_data("REGISTER", data)
            time.sleep(0.1)

        def create_home_page():
            self.menu_button.place(relx=0.01, rely=0.05, anchor="nw")
            self.bank_name_label.pack(pady=(40, 20))
            self.bank_name_label.configure(text=f"Hi {self.first_name} {self.last_name}", font=("Arial", 30, "bold"))
            self.balance_label.pack(pady=20)
            self.right_panel.place(relx=0.55, rely=0.3, relwidth=0.35, relheight=0.55)
            self.update_balance_label()
            self.update_right_panel()
            self.transactions_frame.place(relx=0.1, rely=0.3, relheight=0.55, relwidth=0.4)
            self.welcome_frame.place_forget()
            self.bank_img_label.place_forget()
            self.theme_frame.destroy()
            self.theme_frame = self.create_theme_switch(self.menu_frame)
            self.theme_frame.place(relx=0.05, rely=0.4)

            self.send_data("EXPENSES-2", self.id)
            self.send_data("TRANSACTIONS", self.account_number)

        self.main_frame.pack_forget()
        if self.login_page == None:
            self.login_page = CLogin(self.root,self.main_frame, callback_login, callback_register)
            self.login_page.run()
        else:
            self.login_page.show_choose_frame()
            self.login_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)


    def update_login_page(self):
        self.login_page.face_recognized = True

        if self.face_matches:
            self.login_page.face_matches = True
        else:
            self.login_page.face_matches = False

    def update_login_id_page(self):
            self.login_page.id_exists = self.id_exists

    def update_right_panel(self):
        self.user_name_label.configure(
            text=f"{self.first_name} {self.last_name}",
            text_color = self.text_color,
        )
        self.account_label.configure(
            text=f"Account: {self.account_number}",
            text_color = self.text_color,
        )
        self.phone_label.configure(
            text=f"Phone: {self.phone_number}",
            text_color = self.text_color,
        )

        print(self.sizes)
        print(self.labels)
        if len(self.sizes) > 0:
            total = sum(self.sizes)
            self.total_spent_label.configure(text=f"{total}₪")

            max_value = max(self.sizes)
            index = self.sizes.index(max_value)
            top_category = self.labels[index]

            self.top_category_label.configure(text=f"Top: {top_category}")
        else:
            self.total_spent_label.configure(text="₪0")
            self.top_category_label.configure(text="Top: -")


        if self.transactions and len(self.transactions) > 0:
            last = self.transactions[-1]
            current = last[1]
            destination = last[2]
            amount = last[3]

            if current == self.account_number:
                text = f"Sent ₪{amount}"
            else:
                text = f"Received ₪{amount}"

            self.last_transaction_label.configure(text=text)
        else:
            self.last_transaction_label.configure(text="-")
    def display_transactions(self):

        for widget in self.transactions_list_frame.winfo_children():
            widget.destroy()

        self.transactions.sort(reverse=True)
        self.transaction_rows.clear()

        for t in self.transactions:

            current = t[1]
            destination = t[2]
            amount = t[3]
            date = t[4]

            row = ctk.CTkFrame(
                self.transactions_list_frame,
                fg_color=self.rows_color,
                corner_radius=10,
            )
            self.transaction_rows.append(row)
            row.pack(fill="x", pady=6, padx=6)

            top_frame = ctk.CTkFrame(row, fg_color="transparent")
            top_frame.pack(anchor="w", padx=8, pady=(6, 0))

            if current == self.account_number:

                ctk.CTkLabel(
                    top_frame,
                    text="Sent ",
                    font=("Arial", 15),
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text=f"{amount}₪ ",
                    text_color="#FF6B6B",
                    font=("Arial", 16, "bold")
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text="to ",
                    font=("Arial", 15)
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text=f"[{destination}]",
                    text_color="#4DABF7",
                    font=("Arial", 15, "bold")
                ).pack(side="left")

            elif destination == self.account_number:

                ctk.CTkLabel(
                    top_frame,
                    text="Received ",
                    font=("Arial", 15),
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text=f"{amount}₪ ",
                    text_color="#51CF66",
                    font=("Arial", 16, "bold")
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text="from ",
                    font=("Arial", 15)
                ).pack(side="left")

                ctk.CTkLabel(
                    top_frame,
                    text=f"[{current}]",
                    text_color="#4DABF7",
                    font=("Arial", 15, "bold")
                ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=date,
                text_color="#9E8CC9",
                font=("Arial", 12),
            ).pack(anchor="w", padx=8, pady=(0, 6))


    def open_expenses(self):
        self.toggle_menu()
        write_to_log(f"[CLIENT_GUI] opened Expenses page")
        def callback_expenses(data, cmd):
            write_to_log(f"[CLIENT_GUI] Received data from Expenses window: {data}")
            self.send_data(cmd, data)
            time.sleep(0.1)
            self.root.after(0, self.expenses_page.expense_window.root.destroy)
            self.update_expenses_window()
            self.root.after(0,self.expenses_page.update_graphs)

        self.main_frame.pack_forget()
        if self.expenses_page == None:
            self.expenses_page = CExpensesGUI(self.root, self.main_frame, callback_expenses, self.id)
            self.update_expenses_window()
            self.expenses_page.run()
        else:
            self.expenses_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_page(self, next_frame, previous_frame):
        next_frame.pack(fill="both", expand=True, padx=20, pady=20)
        previous_frame.pack_forget()

    def update_balance_label(self):
        self.balance_label.configure(text=f"Balance: {self.balance}₪")
        write_to_log(f"[CLIENT_GUI] updated balance label to {self.balance}₪")

    def update_register_page(self, data):
        self.login_page.register_page.handle_register_message(data)

    def toggle_theme(self):
        if self.is_dark_mode:
            ctk.set_appearance_mode("light")
            self.is_dark_mode = False
        else:
            ctk.set_appearance_mode("dark")
            self.is_dark_mode = True

    def update_expenses_window(self):
        self.expenses_page.yearly_data = self.yearly_data

    def update_transaction_rows_color(self):

        if self.menu_open:
            color = self.rows_color
        else:
            color = self.hidden_rows_color

        for row in self.transaction_rows:
            row.configure(fg_color=color)


    def on_click_open_transfer(self):
        self.toggle_menu()
        self.cancel_transfer_button.place(relx=0.5, rely=0.1)
        self.transfer_frame.place(relx=0.4, rely=0.3, relheight=0.55, relwidth=0.4)

    def on_click_close_transfer(self):
        self.on_click_transfer.place_forget()
        self.transfer_frame.place_forget()
        self.display_transactions()
        self.destination_user_entry.delete(0, "end")
        self.transfer_amount_entry.delete(0, "end")


    def on_click_transfer_money(self):
        error_flag = True
        self.destination_error_message.pack_forget()
        self.amount_error_message.pack_forget()

        if self.destination_user_entry.get() == self.account_number:
            self.destination_error_message.pack(anchor="w")
            error_flag = False
        if not is_positive_number(self.transfer_amount_entry.get()):
            self.amount_error_message.configure(text="please enter a positive number")
            self.amount_error_message.pack(anchor="w")
            error_flag = False

        if error_flag:
            args = (self.account_number, self.destination_user_entry.get(), int(self.transfer_amount_entry.get()))
            self.send_data("TRANSFER", args)
            self.on_click_close_transfer()


    def run(self):
        self._client_socket = threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    client = CClientGUI("172.16.3.137", PORT)
    client.run()

