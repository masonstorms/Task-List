import tkinter as tk
from tkinter import ttk

class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.tasks = {}

        # Task Entry
        ttk.Label(master, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(master)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        # Priority Entry
        ttk.Label(master, text="Priority:").grid(row=1, column=0, padx=5, pady=5)
        self.priority_entry = ttk.Entry(master)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add Task Button
        ttk.Button(master, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=10)

        # Error Label
        self.error_label = ttk.Label(master, text="", foreground="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Task List
        self.task_listbox = tk.Listbox(master, width = 50)
        self.task_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Delete Task Button
        ttk.Button(master, text="Delete Task", command=self.delete_task).grid(row=5, column=0, columnspan=2, pady=10)

        # Populate tasks from file
        self.load_tasks()

        # Save tasks on exit
        master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def add_task(self):
        task_name = self.task_entry.get()
        priority = self.priority_entry.get()

        if not task_name or not priority:
            self.error_label.config(text="Error: Task name and priority cannot be blank.")
        else:
            try:
                priority = int(priority)
                self.tasks[task_name] = priority
                self.task_listbox.insert(tk.END, f"{task_name} (Priority: {priority})")
                self.task_entry.delete(0, tk.END)
                self.priority_entry.delete(0, tk.END)
                self.error_label.config(text="")
                self.save_tasks()
            except ValueError:
                self.error_label.config(text="Error: Priority must be a valid integer.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_name = self.task_listbox.get(selected_index)
            task_name = task_name.split()[0] 
            del self.tasks[task_name]
            self.task_listbox.delete(selected_index)
            self.task_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.error_label.config(text="")
            self.save_tasks()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    task_name, priority = line.strip().split(", ")
                    priority = int(priority)
                    self.tasks[task_name] = priority
                    self.task_listbox.insert(tk.END, f"{task_name} (Priority: {priority})")
        except FileNotFoundError:
            pass  # No previous tasks file

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task_name, priority in self.tasks.items():
                file.write(f"{task_name}, {priority}\n")

    def on_exit(self):
        self.save_tasks()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()