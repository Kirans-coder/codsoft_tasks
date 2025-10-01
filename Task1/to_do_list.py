import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class MyTaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Task Manager")
        self.geometry("750x650")
        self.resizable(False, False)
        self.data_file = "my_tasks.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)
        self.create_ui()
        self.load_tasks()

    def create_ui(self):
        tk.Label(self, text="My Task Manager", font=("Arial", 24, "bold")).pack(pady=10)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        self.input_box = tk.Entry(input_frame, width=40, font=("Arial", 14))
        self.input_box.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Add Priority Task", command=self.add_priority_task).pack(side=tk.LEFT, padx=5)

        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_box = tk.Entry(search_frame, width=20, font=("Arial", 12))
        self.search_box.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_tasks).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_tasks).pack(side=tk.LEFT, padx=5)

        self.task_view = tk.Listbox(self, width=70, height=22, font=("Arial", 12))
        self.task_view.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mark Completed", command=self.mark_completed).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort by Priority", command=self.sort_priority).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_tasks).pack(side=tk.LEFT, padx=5)

    def load_tasks(self):
        self.task_view.delete(0, tk.END)
        with open(self.data_file, "r") as f:
            self.tasks = json.load(f)
        for task in self.tasks:
            display_text = f"{'[PRIORITY] ' if task.get('priority') else ''}{task['name']} {'(Done)' if task.get('completed') else ''}"
            self.task_view.insert(tk.END, display_text)

    def save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        name = self.input_box.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter a task name")
            return
        self.tasks.append({"name": name, "completed": False, "priority": False, "timestamp": str(datetime.now())})
        self.save_tasks()
        self.input_box.delete(0, tk.END)
        self.load_tasks()

    def add_priority_task(self):
        name = self.input_box.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter a task name")
            return
        self.tasks.append({"name": name, "completed": False, "priority": True, "timestamp": str(datetime.now())})
        self.save_tasks()
        self.input_box.delete(0, tk.END)
        self.load_tasks()

    def delete_task(self):
        selected = self.task_view.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete")
            return
        index = selected[0]
        del self.tasks[index]
        self.save_tasks()
        self.load_tasks()

    def mark_completed(self):
        selected = self.task_view.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to mark completed")
            return
        index = selected[0]
        self.tasks[index]["completed"] = True
        self.save_tasks()
        self.load_tasks()

    def edit_task(self):
        selected = self.task_view.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to edit")
            return
        index = selected[0]
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Task")
        edit_win.geometry("400x150")
        tk.Label(edit_win, text="Edit Task Name:", font=("Arial", 12)).pack(pady=10)
        edit_entry = tk.Entry(edit_win, width=40, font=("Arial", 12))
        edit_entry.pack(pady=5)
        edit_entry.insert(0, self.tasks[index]['name'])
        def save_edit():
            new_name = edit_entry.get().strip()
            if new_name:
                self.tasks[index]['name'] = new_name
                self.save_tasks()
                self.load_tasks()
                edit_win.destroy()
        tk.Button(edit_win, text="Save", command=save_edit).pack(pady=10)

    def sort_priority(self):
        self.tasks.sort(key=lambda x: x.get('priority', False), reverse=True)
        self.save_tasks()
        self.load_tasks()

    def search_tasks(self):
        query = self.search_box.get().strip().lower()
        self.task_view.delete(0, tk.END)
        for task in self.tasks:
            if query in task['name'].lower():
                display_text = f"{'[PRIORITY] ' if task.get('priority') else ''}{task['name']} {'(Done)' if task.get('completed') else ''}"
                self.task_view.insert(tk.END, display_text)

    def clear_tasks(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.load_tasks()

if __name__ == "__main__":
    app = MyTaskManager()
    app.mainloop()
