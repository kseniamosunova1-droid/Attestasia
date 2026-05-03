import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учёба"},
    {"name": "Пробежка", "type": "спорт"},
    {"name": "Провести встречу", "type": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.history = self.load_history()
        self.current_filter = None

        # Виджеты
        self.task_label = tk.Label(root, text="Ваша задача появится здесь", font=("Arial", 14))
        self.task_label.pack(pady=10)

        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        self.filter_var = tk.StringVar(value="все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        for t in ["все", "учёба", "спорт", "работа"]:
            tk.Radiobutton(filter_frame, text=t, variable=self.filter_var, value=t, command=self.update_history_list).pack(side=tk.LEFT)

        self.history_listbox = tk.Listbox(root, width=50, height=10)
        self.history_listbox.pack(pady=10)

        self.add_task_entry = tk.Entry(root, width=40)
        self.add_task_entry.pack(pady=5)
        self.add_task_type = tk.StringVar(value="учёба")
        type_frame = tk.Frame(root)
        type_frame.pack(pady=5)
        for t in ["учёба", "спорт", "работа"]:
            tk.Radiobutton(type_frame, text=t, variable=self.add_task_type, value=t).pack(side=tk.LEFT)
        self.add_task_btn = tk.Button(root, text="Добавить задачу", command=self.add_custom_task)
        self.add_task_btn.pack(pady=5)

        self.update_history_list()

    def generate_task(self):
        task = random.choice(PREDEFINED_TASKS)
        self.history.append(task)
        self.save_history()
        self.task_label.config(text=f"Задача: {task['name']} ({task['type']})")
        self.update_history_list()

    def add_custom_task(self):
        name = self.add_task_entry.get().strip()
        task_type = self.add_task_type.get()
        if not name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return
        task = {"name": name, "type": task_type}
        self.history.append(task)
        self.save_history()
        self.add_task_entry.delete(0, tk.END)
        self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        for task in self.history:
            if filter_type == "все" or task["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

    def save_history(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if not os.path.exists("tasks.json"):
            return []
        with open("tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
