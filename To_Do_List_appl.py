import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
from ttkthemes import ThemedTk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry('700x650+200+100')
        self.root.set_theme("clearlooks")  # Set the theme 

        self.tasks = []

        # UI Components
        self.label = ttk.Label(self.root, text='To-Do List App', font=('Helvetica', 20, 'bold'), padding=(0, 10), background='#2E4053', foreground='white')
        self.label.pack(side='top', fill=tk.X)

        self.task_label = ttk.Label(self.root, text='Add Task:', font=('Helvetica', 14), background='#34495E', foreground='white', padding=(5, 5))
        self.task_label.pack(side='top', fill=tk.X)

        self.task_entry = ttk.Entry(self.root, font=('Helvetica', 14))
        self.task_entry.pack(side='top', pady=5, padx=10, fill=tk.X)

        self.priority_label = ttk.Label(self.root, text='Priority:', font=('Helvetica', 14), background='#34495E', foreground='white', padding=(5, 5))
        self.priority_label.pack(side='top', fill=tk.X)

        self.priority_var = tk.StringVar()
        self.priority_var.set("Low")
        self.priority_menu = ttk.Combobox(self.root, values=["Low", "Medium", "High"], textvariable=self.priority_var, state="readonly", font=('Helvetica', 14))
        self.priority_menu.pack(side='top', pady=5, padx=10, fill=tk.X)

        self.due_date_label = ttk.Label(self.root, text='Due Date:', font=('Helvetica', 14), background='#34495E', foreground='white', padding=(5, 5))
        self.due_date_label.pack(side='top', fill=tk.X)

        self.due_date_entry = DateEntry(self.root, font=('Helvetica', 14), date_pattern='yyyy-mm-dd', borderwidth=2, relief="groove")
        self.due_date_entry.pack(side='top', pady=5, padx=10, fill=tk.X)

        self.add_button = ttk.Button(self.root, text='Add Task', command=self.add_task, style="TButton", padding=(10, 5))
        self.add_button.pack(side='top', pady=10, padx=10, fill=tk.X)

        self.task_listbox = tk.Listbox(self.root, font=('Helvetica', 14), selectbackground='#3498DB', selectmode=tk.SINGLE, bg="#ECF0F1", bd=2, relief="groove")
        self.task_listbox.pack(side='top', pady=10, padx=10, fill=tk.BOTH, expand=True)

       
        self.delete_task_button = ttk.Button(self.root, text='Delete Task', command=self.delete_task, style="TButton", padding=(10, 5))
        self.delete_task_button.pack(side='top', pady=10, padx=10, fill=tk.X, expand=True)

        self.load_tasks_from_file()
        self.update_task_listbox()

    def add_task(self):
        task_text = self.task_entry.get()
        priority = self.priority_var.get()
        due_date_str = self.due_date_entry.get()

        if task_text:
            task = {
                "text": task_text,
                "priority": priority,
                "due_date": due_date_str,
                "completed": False
            }

            self.tasks.append(task)
            self.update_task_listbox()
            self.save_tasks_to_file()

            self.task_entry.delete(0, tk.END)
            self.priority_var.set("Low")
            self.due_date_entry.set_date(datetime.now())  # Reset the calendar to today's date
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

  
    def delete_task(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.update_task_listbox()
            self.save_tasks_to_file()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = f"{task['text']} || Priority: {task['priority']} || Due Date: {task['due_date']} || {'Completed' if task['completed'] else 'Pending'}"
            self.task_listbox.insert(tk.END, task_text)

    def load_tasks_from_file(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            pass

    def save_tasks_to_file(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=2)

def main():
    root = ThemedTk(theme="clearlooks")  # Set the theme for the main window
    ui = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
