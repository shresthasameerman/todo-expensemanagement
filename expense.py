import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x600")
        
        # Color scheme and styling
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.configure("Custom.TButton", padding=6)
        style.configure("Custom.TEntry", padding=5)
        
        # Header
        header = tk.Label(root, text="💰 Expense Tracker", 
                         font=("Helvetica", 20, "bold"),
                         bg="#f0f0f0", fg="#2c3e50")
        header.pack(pady=20)

        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Entry frame
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)

        # Amount entry
        amount_label = ttk.Label(entry_frame, text="Amount (Rs.)", 
                                font=("Helvetica", 10))
        amount_label.pack()
        self.amount_entry = ttk.Entry(entry_frame, width=30, 
                                    style="Custom.TEntry")
        self.amount_entry.pack(pady=5)

        # Category entry
        category_label = ttk.Label(entry_frame, text="Category", 
                                  font=("Helvetica", 10))
        category_label.pack()
        self.category_entry = ttk.Entry(entry_frame, width=30, 
                                      style="Custom.TEntry")
        self.category_entry.pack(pady=5)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="➕ Add Expense", 
                  style="Custom.TButton",
                  command=self.add_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Delete", 
                  style="Custom.TButton",
                  command=self.delete_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📊 View Chart", 
                  style="Custom.TButton",
                  command=self.show_chart).pack(side=tk.LEFT, padx=5)

        # Enhanced Listbox
        self.expense_listbox = tk.Listbox(main_frame, 
                                        width=50, height=15,
                                        selectmode=tk.SINGLE,
                                        bg="white", fg="#2c3e50",
                                        selectbackground="#3498db",
                                        font=("Helvetica", 10))
        self.expense_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Database connection
        self.conn = sqlite3.connect("app_data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses 
            (id INTEGER PRIMARY KEY, amount REAL, category TEXT)
        """)
        self.conn.commit()

        # Keyboard bindings
        self.root.bind('<Return>', lambda e: self.add_expense())
        self.root.bind('<Delete>', lambda e: self.delete_expense())

        self.load_expenses()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        if amount and category:
            self.cursor.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
            self.conn.commit()
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.load_expenses()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def delete_expense(self):
        try:
            selected_expense = self.expense_listbox.get(self.expense_listbox.curselection())
            self.cursor.execute("DELETE FROM expenses WHERE category=?", (selected_expense.split(" - ")[1],))
            self.conn.commit()
            self.load_expenses()
        except:
            messagebox.showwarning("Warning", "Select an expense to delete!")

    def load_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT amount, category FROM expenses")
        for row in self.cursor.fetchall():
            self.expense_listbox.insert(tk.END, f"Rs. {row[0]} - {row[1]}")

    def show_chart(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = self.cursor.fetchall()

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(6,4))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("Expense Breakdown")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()

