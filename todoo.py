import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("400x400")

        # Database setup
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
        self.conn.commit()

        # GUI setup
        self.task_label = tk.Label(root, text="Enter a new task:")
        self.task_label.pack(pady=10)

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.tasks_listbox = tk.Listbox(root, width=50)
        self.tasks_listbox.pack(pady=10)

        self.delete_task_button = tk.Button(root, text="Delete Selected Task", command=self.delete_task)
        self.delete_task_button.pack(pady=10)

        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the database and display them in the Listbox."""
        self.tasks_listbox.delete(0, tk.END)  # Clear the Listbox
        self.cursor.execute("SELECT task FROM tasks")
        for row in self.cursor.fetchall():
            self.tasks_listbox.insert(tk.END, row[0])  # Insert tasks into Listbox

    def add_task(self):
        """Add a new task to the database."""
        task = self.task_entry.get()
        if task:
            self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)  # Clear the entry field
            self.load_tasks()  # Reload tasks
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        """Delete the selected task from the database."""
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task_to_delete = self.tasks_listbox.get(selected_task_index)
            self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task_to_delete,))
            self.conn.commit()
            self.load_tasks()  # Reload tasks
        else:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def __del__(self):
        """Close the database connection when the application exits."""
        self.conn.close()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
