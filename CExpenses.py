from protocol import *



class CExpensesGUI():

    def __init__(self, root, previous_page, callback_expenses, id):

        self.root = root
        self.root.title("Purple Trust Bank")
        self.root.geometry("1000x700")

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        self.previous_page = previous_page
        self.callback_expenses = callback_expenses
        self.id = id

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        # Time updating thread
        self.time_thread = threading.Thread(target=self.update_time, daemon=True)
        self.time_label = None

        self.expense_window = None

        # Pie Chart data
        self.sizes = []
        self.labels = []


    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Expenses",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(40, 20))


        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="#ada6b3"
        )
        self.time_label.place(relx=0.01, rely=0.01, anchor="nw")

        # Expense Button
        self.expense_button = ctk.CTkButton(
            self.main_frame,
            text="Enter expense",
            width=110,
            height=30,
            border_width=1,
            fg_color=self.primary_color,
            command=self.open_expenses_window
        )


        self.expense_button.place(relx=0.45, rely=0.25)

        # Connection Status
        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
        )
        self.connection_status.pack()
        self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()


        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="back",
            font=("Arial", 16, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color="white",
            width=0,
            command=self.open_previous_page

        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="nw")

        if len(self.sizes) > 0:
            fig = Figure(figsize=(4, 3), dpi=100)
            ax = fig.add_subplot(111)

            # Create the pie chart
            ax.pie(self.sizes, labels=self.labels, autopct='%1.1f%%', textprops={'fontsize': 8,'color':'white'})
            ax.axis('equal')
            fig.set_facecolor(self.secondary_color)

            # 3. Create Canvas and Place it in the CTkFrame
            canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
            canvas.draw()
            canvas.get_tk_widget().place(anchor="s", relx=0.7, rely=0.85)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second


    def open_expenses_window(self):
        write_to_log(f"[CLIENT_GUI] opened Expenses window")

        self.expense_window = CExpensesWnd(self.callback_expenses, self.id)
        self.expense_window.run()

    def show_page(self, next_frame, previous_frame):
        next_frame.pack(fill="both", expand=True, padx=20, pady=20)
        previous_frame.pack_forget()

    def open_previous_page(self):
        self.main_frame.pack_forget()
        self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)

    def run(self):
        self.create_ui()
        self.root.mainloop()





class CExpensesWnd:
    def __init__(self, callback_expenses, id):

        self.callback_expenses = callback_expenses
        self.id = id

        self.root = ctk.CTk()
        self.root.title("Purple Trust Bank")
        self.root.geometry("420x390")
        self.root.resizable(False, False)

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        self.expense_types = ["Food", "Clothes", "Gadgets", "Gifts","Other"]
        self.payment_types = ["Cash", "Credit"]


    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)


        self.expense_amount_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.expense_amount_label = ctk.CTkLabel(self.expense_amount_frame, text="Expense amount", font=("Arial", 15, "bold")).pack(anchor="w")
        self.expense_amount_frame.place(anchor="nw",relx=0.15, rely=0.05)
        self.expense_amount_entry = ctk.CTkEntry(self.expense_amount_frame, width=220, height=25, border_width=1)
        self.amount_error_message = ctk.CTkLabel(self.main_frame, text="error")
        self.expense_amount_entry.pack()

        self.types_combo_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.types_combo_label = ctk.CTkLabel(self.types_combo_frame, text="Expense type", font=("Arial", 15, "bold")).pack(anchor="w")
        self.types_combo_frame.place(anchor="w",relx=0.15, rely=0.36)
        self.type_error_message = ctk.CTkLabel(self.main_frame, text="Choose an expense type")
        self.types_combo = ctk.CTkComboBox(self.types_combo_frame, values=self.expense_types, state="readonly")
        self.types_combo.pack()

        self.payment_types_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.payment_types_label = ctk.CTkLabel(self.payment_types_frame, text="How did you pay?", font=("Arial", 15, "bold")).pack(anchor="w")
        self.payment_types_frame.place(anchor="w",relx=0.15, rely=0.6)
        self.payment_error_message = ctk.CTkLabel(self.main_frame, text="Choose a payment type")
        self.payment_types_buttons = ctk.CTkSegmentedButton(self.payment_types_frame, values=self.payment_types)
        self.payment_types_buttons.pack(anchor="w")

        self.submit_button = ctk.CTkButton(
            self.main_frame,
            text="Submit",
            width=80,
            height=40,
            font=("Arial", 20),
            border_width=2,
            fg_color=self.primary_color,
            command=self.on_click_submit,
        )
        self.submit_button.place(anchor="s",rely=0.9, relx=0.5)

    def handle_error_massages(self):
        self.amount_error_message.place_forget()
        self.type_error_message.place_forget()
        self.payment_error_message.place_forget()

        if self.expense_amount_entry.get() == "" or not is_positive_number(self.expense_amount_entry.get()):
            self.amount_error_message.configure(text="please enter a positive number")
            self.amount_error_message.place(anchor="nw",relx=0.15, rely=0.2)
            return False
        if self.types_combo.get() == "":
            self.type_error_message.place(anchor="w",relx=0.15, rely=0.479)
            return False
        if self.payment_types_buttons.get() == "":
            self.payment_error_message.place(anchor="w", relx=0.15, rely=0.71)
            return False

        return True

    def on_click_submit(self):
        if self.handle_error_massages():
            expenses_data = (float(self.expense_amount_entry.get()), self.types_combo.get(), self.payment_types_buttons.get())
            data = (self.id, expenses_data)
            self.callback_expenses(data, "EXPENSES-1")


    def run(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    pass
