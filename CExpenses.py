from protocol import *



class CExpensesGUI():

    def __init__(self, root, previous_page, callback_expenses, id):

        self.root = root
        self.root.title("Purple Trust Bank")
        self.root.geometry("1100x700")

        # Configure purple color scheme
        self.primary_color = ("#6A0DAD", "#2D1B4E")
        self.secondary_color = ("#8A2BE2", "#3E2A6D")
        self.accent_color = ("#9370DB", "#9B5DE5")
        self.text_color = ("#FFFFFF", "#6f4cba")

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
        self.expense_types = ["Food", "Clothes", "Gadgets", "Gifts","Other"]
        self.pie_canvas = None
        self.current_month_index = datetime.now().month - 1
        self.sizes = []
        self.labels = []

        # Bar Chart data
        self.bar_canvas = None
        self.yearly_data = {}
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


        # Arrow buttons
        chart_right_arrow_img = ctk.CTkImage(
            light_image= Image.open(RIGHT_ARROW_IMAGE),
            dark_image= Image.open(RIGHT_ARROW_IMAGE),
            size=(40, 40),
        )
        chart_left_arrow_img = ctk.CTkImage(
            light_image= Image.open(LEFT_ARROW_IMAGE),
            dark_image= Image.open(LEFT_ARROW_IMAGE),
            size=(40, 40),
        )

        month_right_arrow_img = ctk.CTkImage(
            light_image=Image.open(RIGHT_ARROW_IMAGE),
            dark_image=Image.open(RIGHT_ARROW_IMAGE),
            size=(20, 20),
        )
        month_left_arrow_img = ctk.CTkImage(
            light_image=Image.open(LEFT_ARROW_IMAGE),
            dark_image=Image.open(LEFT_ARROW_IMAGE),
            size=(20, 20),
        )

        self.switch_chart_btn_1 = ctk.CTkButton(
            self.main_frame,
            image=chart_right_arrow_img,
            text="",
            width=30,
            fg_color=self.secondary_color,
            hover_color=self.primary_color,
            command=self.show_bar
        )

        self.switch_chart_btn_2 = ctk.CTkButton(
            self.main_frame,
            image=chart_left_arrow_img,
            text="",
            width=30,
            fg_color=self.secondary_color,
            hover_color=self.primary_color,
            command=self.show_pie
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


        # Insights
        self.insights_title = ctk.CTkLabel(
            self.main_frame,
            text="Insights",
            font=("Arial", 22, "bold"),
        )
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")  

        # Monthly insights
        self.monthly_insights_frame = ctk.CTkFrame(
            self.main_frame,
            width=900,
            height=400,
            fg_color=self.secondary_color
        )

        self.switch_month_btn_1 = ctk.CTkButton(
            self.monthly_insights_frame,
            image=month_right_arrow_img,
            text="",
            width=20,
            fg_color=self.secondary_color,
            hover_color=self.primary_color,
            command=self.next_month
        )

        self.switch_month_btn_2 = ctk.CTkButton(
            self.monthly_insights_frame,
            image=month_left_arrow_img,
            text="",
            width=20,
            fg_color=self.secondary_color,
            hover_color=self.primary_color,
            command=self.prev_month
        )
        self.monthly_title = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 25, "bold"),
            text="Monthly Insights"
        )
        self.month_label = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 23, "bold"),
            text_color=self.text_color,
        )
        self.monthly_insights_label = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20),
            text=f"""You spend most of your money on """
        )
        self.bold_montly_expense_label = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 22, "bold")
        )
        self.monthly_first_half = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20),
            text=f""" """
        )
        self.monthly_second_half = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20),
            text=f""" """
        )
        self.bold_monthly_total_amount = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 22, "bold")
        )
        self.monthly_insights_label_3 = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20),
            text=f""" """
        )
        self.bold_montly_change = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 22, "bold")
        )
        self.monthly_insights_label_4 = ctk.CTkLabel(
            self.monthly_insights_frame,
            font=("Arial", 20),
            text=f""" """
        )


        # Yearly insights
        self.yearly_insights_frame = ctk.CTkFrame(
            self.main_frame,
            width=950,
            height=400,
            fg_color=self.secondary_color
        )

        self.yearly_title = ctk.CTkLabel(
            self.yearly_insights_frame,
            font=("Arial", 25, "bold"),
            text="Yearly Insights"
        )
        self.yearly_insights_label = ctk.CTkLabel(
            self.yearly_insights_frame,
            font=("Arial", 17),
            text=f"""You spend most of your money on """
        )

        self.bold_yearly_expense_label = ctk.CTkLabel(
            self.yearly_insights_frame,
            font=("Arial", 20, "bold")
        )

        try:
            self.update_monthly_pie_data()
            self.show_pie()
        except Exception as e:
            write_to_log(f"Error on char: {e}")


    def update_graphs(self):
        self.update_monthly_pie_data()

        if self.monthly_insights_frame.winfo_manager() != '':
            self.pie_canvas.get_tk_widget().place_forget()
            self.show_pie()
        else:
            self.show_bar()

    def show_pie(self):
        self.hide_bar()

        month_name = calendar.month_name[self.current_month_index + 1]
        self.month_label.configure(text=f"{month_name}")
        self.month_label.place(x=160, y=100)

        self.monthly_insights_frame.place(anchor='s', relx=0.47, rely=0.9)
        self.monthly_title.place(x=110, y=50)

        if self.current_month_index < 11:
            self.switch_month_btn_1.place(x=320, y=100)

        if self.current_month_index > 0:
            self.switch_month_btn_2.place(x=35, y=100)

        if len(self.sizes) > 0:
            self.create_pie()
            self.create_pie_insights()
        else:
            self.monthly_first_half.place_forget()
            self.monthly_second_half.place_forget()
            self.bold_montly_change.place_forget()
            self.monthly_insights_label.place_forget()
            self.monthly_insights_label_3.place_forget()
            self.monthly_insights_label_4.place_forget()
            self.bold_monthly_total_amount.place_forget()
            self.bold_montly_expense_label.place_forget()
            self.pie_canvas.get_tk_widget().place_forget()


        self.switch_chart_btn_1.place(relx=0.9, rely=0.5)

            
    def show_bar(self):
        self.hide_pie_insights_frame()
        self.create_bar()
        self.create_bar_insights()
        self.switch_chart_btn_2.place(relx=0.04, rely=0.5)

        
    def hide_pie_insights_frame(self):
        if self.pie_canvas:
            self.pie_canvas.get_tk_widget().place_forget()
        self.monthly_insights_frame.place_forget()
        self.switch_chart_btn_1.place_forget()

    def hide_bar(self):
        if self.bar_canvas:
            self.bar_canvas.get_tk_widget().place_forget()
        self.yearly_insights_frame.place_forget()
        self.switch_chart_btn_2.place_forget()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def update_monthly_pie_data(self):
        self.sizes = []
        self.labels = []

        for expense_type in self.expense_types:
            value = self.yearly_data[expense_type][self.current_month_index]
            if value > 0:
                self.sizes.append(value)
                self.labels.append(expense_type)


    def create_pie(self):
        fig = Figure(figsize=(5.5, 5), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(self.sizes, labels=self.labels, colors=self.colors, autopct='%1.1f%%', textprops={'fontsize': 12, 'color': 'white'})
        ax.axis('equal')
        fig.set_facecolor(self.secondary_color[1])

        self.pie_canvas = FigureCanvasTkAgg(fig, master=self.monthly_insights_frame)
        self.pie_canvas.draw()
        self.pie_canvas.get_tk_widget().place(anchor="center", relx=0.75, rely=0.5)


    def create_pie_insights(self):
        max_num = max(self.sizes)
        place = self.sizes.index(max_num)
        biggest_expense_label = self.labels[place]

        color_index = self.labels.index(biggest_expense_label)
        color = self.colors[color_index]

        first_half, second_half, direction = self.get_month_change_insight()
        if direction == "increased":
            change_color = "red"
        else:
            change_color = "green"

        rank = self.get_month_rank_insight()

        self.monthly_first_half.configure(text=f"{first_half}")
        self.monthly_second_half.configure(text=f"{second_half}")
        self.bold_montly_change.configure(text=f"{direction}",text_color=change_color)
        self.monthly_insights_label_3.configure(text=f"This month is ranked #{rank} in spending this year")
        self.monthly_insights_label_4.configure(text=f"Overall: ")
        self.bold_monthly_total_amount.configure(text=f"{int(sum(self.sizes))}₪")
        self.bold_montly_expense_label.configure(text=f"""{biggest_expense_label}""",text_color=color)


        self.monthly_insights_label_4.place(x=5, y=160)
        self.bold_monthly_total_amount.place(x=80, y=160)
        self.monthly_insights_label.place(x=5, y=210)
        self.bold_montly_expense_label.place(x=320, y=210)
        self.monthly_first_half.place(x=5, y=260)
        self.monthly_second_half.place(x=200, y=260)
        self.bold_montly_change.place(x=85, y=260)
        self.monthly_insights_label_3.place(x=5, y=310)




    def create_bar_insights(self):
        biggest_expense = 0
        biggest_expense_label = ''
        for i in range(5):
            expense = sum(self.yearly_data[self.expense_types[i]])
            if expense > biggest_expense:
                biggest_expense = expense
                biggest_expense_label = self.expense_types[i]

        color_index = self.expense_types.index(biggest_expense_label)
        color = self.colors[color_index]

        self.bold_yearly_expense_label.configure(text=f"""{biggest_expense_label}""", text_color=color)

        self.yearly_insights_frame.place(anchor='s', relx=0.55, rely=0.9)
        self.yearly_title.place(x=90, y=50)
        self.yearly_insights_label.place(x=10, y=100)
        self.bold_yearly_expense_label.place(x=270, y=100)

     

    def create_bar(self):

        df = pd.DataFrame(self.yearly_data)
        df.set_index('Month', inplace=True)

        fig, ax = plt.subplots(figsize=(7,5), dpi=100, facecolor=self.secondary_color[1],)
        
        df.plot(kind='bar', stacked=True, ax=ax, color=self.colors)

        ax.set_xlabel('Month',color='white',fontsize=12)
        ax.set_ylabel('Amount (₪)',color='white',fontsize=12)
        ax.legend(title='Categories',)
        plt.xticks(rotation=0,color='white')
        plt.yticks(color='white')

        self.bar_canvas = FigureCanvasTkAgg(fig, master=self.yearly_insights_frame)
        self.bar_canvas.draw()

        self.bar_canvas.get_tk_widget().place(anchor="center", relx=0.67, rely=0.48)

    def next_month(self):
        self.current_month_index = self.current_month_index + 1
        if self.current_month_index == 11:
            self.switch_month_btn_1.place_forget()
        self.update_graphs()

    def prev_month(self):
        self.current_month_index = self.current_month_index - 1
        if self.current_month_index == 0:
            self.switch_month_btn_2.place_forget()
        self.update_graphs()

    def get_month_change_insight(self):
        i = self.current_month_index

        if i == 0:
            return "No data for previous month", "", ""

        insights = []

        for expense_type in self.expense_types:
            current = self.yearly_data[expense_type][i]
            prev = self.yearly_data[expense_type][i - 1]

            if prev > 0 and current > 0:
                percent = ((current - prev) / prev) * 100

                if abs(percent) > 20:
                    if percent > 0:
                        direction = "increased"
                    else:
                        direction = "decreased"
                    insights.append(f"{expense_type} {direction} by {abs(percent):.0f}%")

        if insights:
            chosen_insight = (max(insights, key=len)).split()
            direction = chosen_insight[1]

            chosen_insight.pop(1)

            first_hlf = chosen_insight[0]
            second_half = chosen_insight[1] + " " + chosen_insight[2]

            return first_hlf, second_half, direction
        else:
            return "No significant changes from last month", "", ""


    def get_month_rank_insight(self):
        monthly_totals = []

        for i in range(12):
            total = 0

            for expense_type in self.expense_types:
                total += self.yearly_data[expense_type][i]

            monthly_totals.append(total)

        current_total = monthly_totals[self.current_month_index]

        sorted_totals = sorted(monthly_totals, reverse=True)

        rank = sorted_totals.index(current_total) + 1

        return rank


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
