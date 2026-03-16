import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# הגדרת מראה ה-UI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker Visualization")
        self.geometry("800x600")

        data = {
            'Month': ['January', 'February', 'March'],
            'Food': [1200, 1500, 1100],
            'Clothing': [400, 200, 800],
            'Leisure': [600, 900, 500]
        }
        df = pd.DataFrame(data)
        df.set_index('Month', inplace=True)

        # 2. יצירת האובייקט של Matplotlib (Figure)
        # שימוש ב-facecolor תואם לרקע של ה-UI (אופציונלי)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # יצירת הגרף הנערם
        df.plot(kind='bar', stacked=True, ax=ax, color=['#5dade2', '#ec7063', '#58d68d'])

        # עיצוב הגרף באנגלית
        ax.set_title('Monthly Expenses by Category')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.legend(title='Categories')
        plt.xticks(rotation=0)

        # 3. שילוב הגרף בתוך CustomTkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        
        # הצבת הווידג'ט בחלון
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
