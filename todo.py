import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        
        # Color scheme
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.configure("Custom.TButton", padding=6)
        style.configure("Custom.TEntry", padding=5)
        
        # Header
        header = tk.Label(root, text="📝 My Todo List", font=("Helvetica", 16, "bold"), 
                         bg="#f0f0f0", fg="#333333")
        header.pack(pady=15)

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # UI Elements with improved styling
        self.task_entry = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.task_entry.pack(pady=10, padx=5, fill=tk.X)
        self.task_entry.insert(0, "Enter new task...")
        self.task_entry.bind("<FocusIn>", self._clear_placeholder)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="✚ Add Task", style="Custom.TButton", 
                  command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✖ Delete Task", style="Custom.TButton", 
                  command=self.delete_task).pack(side=tk.RIGHT, padx=5)

        # Enhanced Listbox
        self.task_listbox = tk.Listbox(main_frame, width=50, height=15, 
                                      selectmode=tk.SINGLE,
                                      bg="white", fg="#333333",
                                      selectbackground="#0078D7",
                                      font=("Helvetica", 10))
        self.task_listbox.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)

        # Database setup
        self.conn = sqlite3.connect("app_data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, task TEXT)")
        self.conn.commit()

        self.load_tasks()

    def _clear_placeholder(self, event):
        if self.task_entry.get() == "Enter new task...":
            self.task_entry.delete(0, tk.END)

    def add_task(self):
        task = self.task_entry.get()
        if task and task != "Enter new task...":
            self.cursor.execute("INSERT INTO todo (task) VALUES (?)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, "Enter new task...")
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection())
            self.cursor.execute("DELETE FROM todo WHERE task=?", (selected_task,))
            self.conn.commit()
            self.load_tasks()
        except:
            messagebox.showwarning("Warning", "Select a task to delete!")

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT task FROM todo")
        for row in self.cursor.fetchall():
            self.task_listbox.insert(tk.END, row[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

