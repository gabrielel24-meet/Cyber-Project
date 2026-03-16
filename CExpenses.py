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
        self.pie_canvas = None
        self.sizes = []
        self.labels = []
        self.colors= ['#5dade2', '#ec7063', '#58d68d','#FFD700','#60888F']



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
        self.expense_button.place(relx=0.45, rely=0.2)


        self.arrow_img = Image.open(ARROW_IMAGE)
        my_image = ctk.CTkImage(
            light_image= Image.open(ARROW_IMAGE),
            dark_image= Image.open(ARROW_IMAGE),
            size=(30, 30),
        )

        self.hide_chart_insights_button = ctk.CTkButton(
            self.main_frame,
            image=my_image,
            text="",
            width=20,
            fg_color=self.secondary_color,
            hover_color=self.primary_color,
            command=self.hide_chart_insights
        )



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



        self.insights_title = ctk.CTkLabel(
            self.main_frame,
            text="Insights",
            font=("Arial", 22, "bold"),
        )
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")  

        self.monthly_insights_frame = ctk.CTkFrame(
            self.main_frame,
            width=700,
            height=380,
            fg_color=self.secondary_color
        )
        self.monthly_insights_frame.place(anchor='s', relx=0.5, rely=0.96)  
        self.monthly_insights_frame.pack_propagate(False)  
        
        self.monthly_title = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20, "bold"),
            text="Monthly Insights"
        )
        self.monthly_insights_label = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 17),
            text=f"""You spend most of your money on """
        )

        self.bold_expense_label = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20, "bold")
        )

        self.yearly_insights_frame = ctk.CTkFrame(
            self.main_frame,
            width=700,
            height=380,
            fg_color=self.secondary_color
        )
        self.monthly_insights_frame.place(anchor='s', relx=0.5, rely=0.96)  
        self.monthly_insights_frame.pack_propagate(False)  

        try:
            self.show_pie()
        except Exception as e:
            write_to_log(f"Error on char: {e}")




    def show_pie(self):
        if len(self.sizes) > 0:
            self.create_pie()
            self.create_insights()
            self.hide_chart_insights_button.place(relx=0.9, rely=0.5)


    def hide_chart_insights(self):
        if self.pie_canvas:
            self.pie_canvas.get_tk_widget().place_forget()
        self.monthly_insights_frame.place_forget()
        self.create_bar()


    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def create_pie(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(self.sizes, labels=self.labels, colors=self.colors, autopct='%1.1f%%', textprops={'fontsize': 10, 'color': 'white'})
        ax.axis('equal')
        fig.set_facecolor(self.secondary_color)

        self.pie_canvas = FigureCanvasTkAgg(fig, master=self.monthly_insights_frame)
        self.pie_canvas.draw()
        self.pie_canvas.get_tk_widget().place(anchor="center", relx=0.8, rely=0.5)


    def create_insights(self):
        biggest_expense = self.insights()
        color_index = self.labels.index(biggest_expense)
        color = self.colors[color_index]

        self.bold_expense_label.configure(text=f"""{biggest_expense}""",text_color=color)

        self.monthly_insights_frame.place(anchor='s',relx=0.5, rely=0.96)
        self.monthly_title.place(x=20, y=50)
        self.monthly_insights_label.place(x=20, y=80)
        self.bold_expense_label.place(x=280, y=80)

     

    def create_bar(self):
        data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'Food': [1200, 1500, 1100, 1300, 1400, 1200, 1100, 1250, 1350, 1450, 1550, 1650],
            'Clothes': [400, 200, 800, 600, 700, 500, 400, 450, 550, 650, 750, 850],
            'Gifts': [600, 900, 500, 700, 800, 3000, 500, 550, 650, 750, 850, 950],
            'Gadgets': [300, 400, 200, 500, 600, 400, 300, 350, 450, 550, 650, 750],
            'Other': [300, 400, 200, 500, 600, 400, 300, 350, 450, 550, 650, 750]
        }
        df = pd.DataFrame(data)
        df.set_index('Month', inplace=True)

        # 2. יצירת האובייקט של Matplotlib (Figure)
        # שימוש ב-facecolor תואם לרקע של ה-UI (אופציונלי)
        fig, ax = plt.subplots(figsize=(8,5), dpi=100, facecolor=self.secondary_color,)
        
        # יצירת הגרף הנערם
        df.plot(kind='bar', stacked=True, ax=ax, color=self.colors)

        # עיצוב הגרף באנגלית
        ax.set_xlabel('Month',color='white',fontsize=12)
        ax.set_ylabel('Amount (₪)',color='white',fontsize=12)
        ax.legend(title='Categories',)
        plt.xticks(rotation=0,color='white')
        plt.yticks(color='white')

        # 3. שילוב הגרף בתוך CustomTkinter
        self.bar_canvas = FigureCanvasTkAgg(fig, master=self.yearly_insights_frame)
        self.bar_canvas.draw()

        self.yearly_insights_frame.place(anchor='s', relx=0.5, rely=0.96)
        self.bar_canvas.get_tk_widget().place(anchor="center", relx=0.65, rely=0.5)



    def insights(self):
        max_num = max(self.sizes)
        place = self.sizes.index(max_num)
        expense = self.labels[place]

        return expense

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




def test():
    pass
if __name__ == "__main__":
    exp = CExpensesGUI()
    exp.run()
