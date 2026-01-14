from protocol import *

class CExpenses:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Purple Trust Bank")
        self.root.geometry("400x350")

        # Configure purple color scheme
        self.primary_color = "#6A0DAD"  # Purple
        self.secondary_color = "#8A2BE2"  # Blue violet
        self.accent_color = "#9370DB"  # Medium purple

        # Set the background color
        self.root.configure(fg_color=self.primary_color)


    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)


        self.expense_amount_frame = ctk.CTkFrame(self.main_frame, fg_color=self.secondary_color)
        self.expense_amount_label = ctk.CTkLabel(self.expense_amount_frame, text="expense amount", font=("Arial", 15, "bold")).pack(anchor="w")
        self.expense_amount_frame.pack(pady=30)

        self.destination_user_entry = ctk.CTkEntry(self.expense_amount_frame, width=220, height=25, border_width=1)
        self.error_message = ctk.CTkLabel(self.expense_amount_frame, text="please enter a positive number")
        self.destination_user_entry.pack()

    def run(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == '__main__':
    ExpensesWnd = CExpenses()
    ExpensesWnd.run()