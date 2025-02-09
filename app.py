import tkinter as tk
from tkinter import ttk
from todo import TodoApp
from expense import ExpenseApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity & Finance Manager")
        self.root.geometry("800x600")
        
        # Color scheme
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        style = ttk.Style()
        style.configure("Header.TLabel", 
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=("Helvetica", 24, "bold"),
                       padding=20)
        
        style.configure("Card.TFrame",
                       background=self.fg_color,
                       relief="raised",
                       borderwidth=2)
        
        style.configure("CardTitle.TLabel",
                       background=self.fg_color,
                       foreground=self.bg_color,
                       font=("Helvetica", 16, "bold"),
                       padding=10)
        
        # Main container
        container = ttk.Frame(self.root, style="Card.TFrame", padding=30)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        header = ttk.Label(
            container,
            text="🚀 Productivity & Finance Manager",
            style="Header.TLabel"
        )
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Cards container
        cards_frame = ttk.Frame(container)
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # Todo Card
        todo_card = self.create_card(
            cards_frame,
            "📝 Task Management",
            "Open Todo List",
            self.open_todo
        )
        todo_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Expense Card
        expense_card = self.create_card(
            cards_frame,
            "💰 Expense Tracking",
            "Open Expense Tracker",
            self.open_expense
        )
        expense_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            background=self.bg_color,
            foreground=self.fg_color,
            padding=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_card(self, parent, title, button_text, command):
        card = ttk.Frame(parent, style="Card.TFrame")
        
        ttk.Label(
            card,
            text=title,
            style="CardTitle.TLabel"
        ).pack(fill=tk.X)
        
        btn = tk.Button(
            card,
            text=button_text,
            command=command,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Helvetica", 10),
            relief="flat",
            pady=10,
            cursor="hand2"
        )
        btn.pack(pady=20)
        
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.configure(bg="#2980b9"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.accent_color))
        
        return card

    def open_todo(self):
        self.status_var.set("Opening Todo List...")
        todo_window = tk.Toplevel(self.root)
        TodoApp(todo_window)
        self.status_var.set("Ready")
    
    def open_expense(self):
        self.status_var.set("Opening Expense Tracker...")
        expense_window = tk.Toplevel(self.root)
        ExpenseApp(expense_window)
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()