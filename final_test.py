import customtkinter as ctk
from datetime import datetime
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class UltraModernBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Bank - Premium Banking")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#1a1a2e")

        # Purple color scheme
        self.colors = {
            "primary": "#6a0dad",
            "secondary": "#8a2be2",
            "accent": "#9370db",
            "dark_bg": "#1a1a2e",
            "card_bg": "#2d2d44",
            "text_light": "#ffffff",
            "text_gray": "#b8b8b8"
        }

        # Sample account data
        self.accounts = {
            "Main Account": {"balance": 12500.75, "number": "**** 4832"},
            "Savings": {"balance": 3500.00, "number": "**** 6914"},
            "Investment": {"balance": 8750.50, "number": "**** 2278"}
        }

        self.transactions = [
            {"date": "2024-01-15", "description": "Starbucks", "amount": -5.75, "type": "expense"},
            {"date": "2024-01-14", "description": "Salary Deposit", "amount": 3500.00, "type": "income"},
            {"date": "2024-01-12", "description": "Amazon Purchase", "amount": -89.99, "type": "expense"},
            {"date": "2024-01-10", "description": "Transfer from John", "amount": 150.00, "type": "income"},
            {"date": "2024-01-08", "description": "Netflix", "amount": -15.99, "type": "expense"},
        ]

        self.setup_ui()

    def setup_ui(self):
        # Create main container with sidebar and content area
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.colors["dark_bg"])
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.create_sidebar()

        # Main content area
        self.create_main_content()

        # Initialize with dashboard
        self.show_dashboard()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_container, width=250, fg_color=self.colors["card_bg"])
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        # Bank logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=20)

        logo_label = ctk.CTkLabel(
            logo_frame,
            text="💎 NEXUS BANK",
            font=("Arial", 20, "bold"),
            text_color=self.colors["primary"]
        )
        logo_label.pack()

        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("💳 Accounts", self.show_accounts),
            ("🔄 Transfer", self.show_transfer),
            ("📈 Analytics", self.show_analytics),
            ("⚙️ Settings", self.show_settings)
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 14),
                fg_color="transparent",
                hover_color=self.colors["primary"],
                text_color=self.colors["text_light"],
                anchor="w",
                command=command,
                height=40
            )
            btn.pack(fill="x", padx=10, pady=5)

        # User profile at bottom
        user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        user_frame.pack(side="bottom", fill="x", padx=10, pady=20)

        ctk.CTkLabel(
            user_frame,
            text="👤 Alex Morgan",
            font=("Arial", 12, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            user_frame,
            text="Premium Member",
            font=("Arial", 10),
            text_color=self.colors["primary"]
        ).pack(anchor="w")

    def create_main_content(self):
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Header with time and quick stats
        self.create_header()

        # Content frame where different pages will be shown
        self.content_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=10)

    def create_header(self):
        header = ctk.CTkFrame(self.content_area, height=80, fg_color=self.colors["card_bg"])
        header.pack(fill="x")
        header.pack_propagate(False)

        # Time and date
        time_frame = ctk.CTkFrame(header, fg_color="transparent")
        time_frame.pack(side="left", padx=20, pady=10)

        self.date_label = ctk.CTkLabel(
            time_frame,
            text="",
            font=("Arial", 12),
            text_color=self.colors["text_gray"]
        )
        self.date_label.pack(anchor="w")

        self.time_label = ctk.CTkLabel(
            time_frame,
            text="",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_light"]
        )
        self.time_label.pack(anchor="w")

        # Quick stats
        stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        stats_frame.pack(side="right", padx=20, pady=10)

        total_balance = sum(acc["balance"] for acc in self.accounts.values())

        ctk.CTkLabel(
            stats_frame,
            text=f"Total Balance: ${total_balance:,.2f}",
            font=("Arial", 14, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="e")

        ctk.CTkLabel(
            stats_frame,
            text="+2.3% this month",
            font=("Arial", 10),
            text_color="#00ff00"
        ).pack(anchor="e")

        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.root.after(1000, self.update_time)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content_frame()

        # Welcome section
        welcome_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors["card_bg"])
        welcome_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            welcome_frame,
            text="Welcome back, Alex! 👋",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=10)

        ctk.CTkLabel(
            welcome_frame,
            text="Here's your financial overview",
            font=("Arial", 14),
            text_color=self.colors["text_gray"]
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # Quick stats row
        stats_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_row.pack(fill="x", padx=10, pady=10)

        stats_data = [
            ("Total Balance", "$24,751.25", "+2.3%"),
            ("Monthly Income", "$3,500.00", "+5.1%"),
            ("Monthly Expenses", "$1,234.56", "-1.2%"),
            ("Investments", "$8,750.50", "+7.8%")
        ]

        for i, (title, value, change) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(stats_row, fg_color=self.colors["card_bg"], height=100)
            stat_card.pack(side="left", fill="both", expand=True, padx=5)
            stat_card.pack_propagate(False)

            ctk.CTkLabel(
                stat_card,
                text=title,
                font=("Arial", 12),
                text_color=self.colors["text_gray"]
            ).pack(anchor="w", padx=15, pady=(15, 0))

            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Arial", 18, "bold"),
                text_color=self.colors["text_light"]
            ).pack(anchor="w", padx=15, pady=5)

            ctk.CTkLabel(
                stat_card,
                text=change,
                font=("Arial", 10),
                text_color="#00ff00" if "+" in change else "#ff4444"
            ).pack(anchor="w", padx=15, pady=(0, 15))

        # Accounts and transactions row
        bottom_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        bottom_row.pack(fill="both", expand=True, padx=10, pady=10)

        # Accounts section
        accounts_frame = ctk.CTkFrame(bottom_row, fg_color=self.colors["card_bg"])
        accounts_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ctk.CTkLabel(
            accounts_frame,
            text="Your Accounts",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=15)

        for account, details in self.accounts.items():
            acc_card = ctk.CTkFrame(accounts_frame, fg_color="#3a3a5a")
            acc_card.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(
                acc_card,
                text=account,
                font=("Arial", 12, "bold"),
                text_color=self.colors["text_light"]
            ).pack(anchor="w", padx=10, pady=(10, 0))

            ctk.CTkLabel(
                acc_card,
                text=details["number"],
                font=("Arial", 10),
                text_color=self.colors["text_gray"]
            ).pack(anchor="w", padx=10)

            ctk.CTkLabel(
                acc_card,
                text=f"${details['balance']:,.2f}",
                font=("Arial", 14, "bold"),
                text_color=self.colors["primary"]
            ).pack(anchor="w", padx=10, pady=(0, 10))

        # Recent transactions
        transactions_frame = ctk.CTkFrame(bottom_row, fg_color=self.colors["card_bg"])
        transactions_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ctk.CTkLabel(
            transactions_frame,
            text="Recent Transactions",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=15)

        for transaction in self.transactions[:5]:
            trans_card = ctk.CTkFrame(transactions_frame, fg_color="transparent")
            trans_card.pack(fill="x", padx=15, pady=5)

            # Left side - description and date
            left_frame = ctk.CTkFrame(trans_card, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                left_frame,
                text=transaction["description"],
                font=("Arial", 12),
                text_color=self.colors["text_light"]
            ).pack(anchor="w")

            ctk.CTkLabel(
                left_frame,
                text=transaction["date"],
                font=("Arial", 10),
                text_color=self.colors["text_gray"]
            ).pack(anchor="w")

            # Right side - amount
            amount_color = "#00ff00" if transaction["amount"] > 0 else "#ff4444"
            amount_text = f"+${abs(transaction['amount']):.2f}" if transaction[
                                                                       "amount"] > 0 else f"-${abs(transaction['amount']):.2f}"

            ctk.CTkLabel(
                trans_card,
                text=amount_text,
                font=("Arial", 12, "bold"),
                text_color=amount_color
            ).pack(side="right")

    def show_accounts(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Account Management",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=10)

        # Add account cards with more details
        for account, details in self.accounts.items():
            account_card = ctk.CTkFrame(
                self.content_frame,
                fg_color=self.colors["card_bg"],
                height=120
            )
            account_card.pack(fill="x", padx=20, pady=10)
            account_card.pack_propagate(False)

            # Account header
            header_frame = ctk.CTkFrame(account_card, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(
                header_frame,
                text=account,
                font=("Arial", 18, "bold"),
                text_color=self.colors["text_light"]
            ).pack(side="left")

            ctk.CTkLabel(
                header_frame,
                text=details["number"],
                font=("Arial", 12),
                text_color=self.colors["text_gray"]
            ).pack(side="left", padx=20)

            ctk.CTkLabel(
                header_frame,
                text=f"${details['balance']:,.2f}",
                font=("Arial", 20, "bold"),
                text_color=self.colors["primary"]
            ).pack(side="right")

            # Action buttons
            btn_frame = ctk.CTkFrame(account_card, fg_color="transparent")
            btn_frame.pack(fill="x", padx=20, pady=(0, 15))

            actions = ["View Details", "Transfer", "History", "Settings"]
            for action in actions:
                ctk.CTkButton(
                    btn_frame,
                    text=action,
                    font=("Arial", 10),
                    fg_color=self.colors["primary"],
                    hover_color=self.colors["secondary"],
                    width=80,
                    height=25
                ).pack(side="left", padx=5)

    def show_transfer(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Money Transfer",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=10)

        # Transfer form
        form_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors["card_bg"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        form_fields = [
            ("From Account", "dropdown"),
            ("To Account", "dropdown"),
            ("Amount", "entry"),
            ("Description", "entry"),
            ("Schedule Transfer", "checkbox")
        ]

        for i, (label, field_type) in enumerate(form_fields):
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", padx=30, pady=15)

            ctk.CTkLabel(
                field_frame,
                text=label,
                font=("Arial", 14),
                text_color=self.colors["text_light"]
            ).pack(anchor="w")

            if field_type == "entry":
                ctk.CTkEntry(
                    field_frame,
                    placeholder_text=f"Enter {label.lower()}",
                    height=40,
                    font=("Arial", 12)
                ).pack(fill="x", pady=5)
            elif field_type == "dropdown":
                ctk.CTkComboBox(
                    field_frame,
                    values=[f"{acc} ({details['number']})" for acc, details in self.accounts.items()],
                    height=40,
                    font=("Arial", 12)
                ).pack(fill="x", pady=5)
            elif field_type == "checkbox":
                ctk.CTkCheckBox(
                    field_frame,
                    text="Schedule for later date",
                    font=("Arial", 12)
                ).pack(anchor="w", pady=5)

        # Transfer button
        ctk.CTkButton(
            form_frame,
            text="💸 Transfer Now",
            font=("Arial", 16, "bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"],
            height=50,
            command=self.process_transfer
        ).pack(fill="x", padx=30, pady=30)

    def show_analytics(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Financial Analytics",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=10)

        # Create sample charts
        chart_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors["card_bg"])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sample spending chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Spending by category
        categories = ['Food', 'Shopping', 'Bills', 'Entertainment', 'Other']
        amounts = [350, 420, 280, 150, 100]
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']

        ax1.pie(amounts, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Spending by Category')

        # Monthly trend
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        income = [3200, 3500, 3800, 4200, 3900, 4100]
        expenses = [2800, 3100, 2900, 3300, 3000, 3200]

        ax2.plot(months, income, label='Income', color='#00ff00', linewidth=2)
        ax2.plot(months, expenses, label='Expenses', color='#ff4444', linewidth=2)
        ax2.fill_between(months, income, expenses, alpha=0.2)
        ax2.set_title('Income vs Expenses')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        # Embed the chart in tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def show_settings(self):
        self.clear_content_frame()

        ctk.CTkLabel(
            self.content_frame,
            text="Settings & Preferences",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_light"]
        ).pack(anchor="w", padx=20, pady=10)

        settings_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors["card_bg"])
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)

        settings_options = [
            ("🔔 Notifications", "toggle"),
            ("🌙 Dark Mode", "toggle"),
            ("💳 Card Limits", "button"),
            ("👤 Personal Info", "button"),
            ("🔒 Security", "button"),
            ("🏦 Linked Accounts", "button")
        ]

        for i, (label, setting_type) in enumerate(settings_options):
            setting_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
            setting_frame.pack(fill="x", padx=30, pady=15)

            ctk.CTkLabel(
                setting_frame,
                text=label,
                font=("Arial", 14),
                text_color=self.colors["text_light"]
            ).pack(side="left")

            if setting_type == "toggle":
                ctk.CTkSwitch(
                    setting_frame,
                    text="",
                    width=50
                ).pack(side="right")
            elif setting_type == "button":
                ctk.CTkButton(
                    setting_frame,
                    text="Configure",
                    font=("Arial", 12),
                    fg_color=self.colors["primary"],
                    hover_color=self.colors["secondary"],
                    width=100
                ).pack(side="right")

    def process_transfer(self):
        # Simulate transfer processing
        print("Transfer processed!")
        # In a real app, this would handle the transfer logic


def main():
    root = ctk.CTk()
    app = UltraModernBankApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()