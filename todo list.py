import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status INTEGER)')
conn.commit()

# Functions
def add_task():
    task = entry.get().strip()
    if task == "":
        messagebox.showwarning("Input Error", "Task cannot be empty!")
    else:
        cursor.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, 0))
        conn.commit()
        entry.delete(0, tk.END)
        load_tasks()

def delete_task():
    try:
        selected_item = listbox.curselection()[0]
        task_id = listbox.get(selected_item).split(" - ")[0]
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "No task selected!")

def mark_done():
    try:
        selected_item = listbox.curselection()[0]
        task_id = listbox.get(selected_item).split(" - ")[0]
        cursor.execute('UPDATE tasks SET status = 1 WHERE id = ?', (task_id,))
        conn.commit()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "No task selected!")

def load_tasks():
    listbox.delete(0, tk.END)
    for row in cursor.execute('SELECT id, task, status FROM tasks'):
        status = "✔" if row[2] == 1 else "✖"
        listbox.insert(tk.END, f"{row[0]} - {row[1]} [{status}]")

# GUI Setup
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Task", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Mark Done", command=mark_done).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Task", command=delete_task).grid(row=0, column=2, padx=5)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=20)

load_tasks()
root.mainloop()

# Close the database connection
conn.close()
