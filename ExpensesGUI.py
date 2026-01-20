from protocol import *

class CExpenses:
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
            self.callback_expenses(data)





    def run(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == '__main__':
    ExpensesWnd = CExpenses()
    ExpensesWnd.run()