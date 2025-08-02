from Manager import Manager
from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta
from focus_mode import Focus
import tkinter.messagebox as msg

class UI:
    def __init__(self, manager: Manager):
        self.root = tk.Tk()
        self.ttk = ttk
        self.manager = manager
        self.style = ttk.Style()
        self.vars = []
        self.setup_style()
        self.setup_ui()
        self.focus = None
        self.root.mainloop()

    def setup_style(self):
        self.root.title("TO DO APP ✨")
        self.root.geometry("700x800")
        self.root.configure(bg="#f0f4f8")
        self.style.theme_use("clam")

        self.style.configure("Rounded.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            relief="flat",
            background="#8e44ad",
            foreground="white",
            borderwidth=0)
        self.style.map("Rounded.TButton",
            background=[("active", "#9b59b6")])

        self.style.configure("TCheckbutton",
            background="#f0f4f8",
            font=("Segoe UI", 11),
            foreground="#2c3e50",
            focuscolor="#f0f4f8")

        self.style.configure("TEntry",
            font=("Segoe UI", 11),
            padding=6,
            relief="flat")

        self.style.configure("TLabel",
            font=("Segoe UI", 14, "bold"),
            background="#f0f4f8",
            foreground="#34495e")

    def setup_ui(self):
        self.all_widgets = []  # 🔧 Lưu lại tất cả widget ban đầu

        self.ttk.Label(self.root, text="📋 Danh sách việc cần làm").grid(row=0, column=0, pady=20)
        self.frame_task = self.ttk.Frame(self.root, style="TFrame")
        self.frame_task.grid(row=1, column=0, padx=20, sticky="w")

        self.user_inp = self.ttk.Entry(self.root, width=50)
        self.user_inp.grid(row=3, column=0, pady=20)

        time = self.ttk.Entry(self.root, width=25)
        time.insert(0, "25")
        time.grid(row=3, column=1)

        button_frame = self.ttk.Frame(self.root, style="TFrame")
        button_frame.grid(row=2, column=0, pady=10)

        self.ttk.Button(button_frame, text="➕ Thêm việc", style="Rounded.TButton", command=self.add_task).grid(row=0, column=0, padx=10)
        self.ttk.Button(button_frame, text="🧹 Xóa việc đã xong", style="Rounded.TButton", command=self.delete_and_refresh).grid(row=0, column=1, padx=10)

        self.focus_button = self.ttk.Button(self.root, text="Bật chế độ học tập trung", command=lambda: self.on_focus_mode(time.get()))
        self.focus_button.grid(row=2, column=1, pady=5)

        # ✅ Lưu widget ban đầu
        self.all_widgets = self.root.winfo_children().copy()
        self.show_tasks()

    def show_tasks(self):
        for widget in self.frame_task.winfo_children():
            widget.destroy()

        self.vars.clear()
        tasks = self.manager.tasks

        for index, task in enumerate(tasks):
            var = tk.IntVar(value=1 if task.done else 0)
            self.vars.append(var)

            deadline_str = task.deadline.strftime("%d/%m/%Y %H:%M")

            checkbox = self.ttk.Checkbutton(
                self.frame_task,
                text=f"{task.title}\n📅 Deadline: {deadline_str}",
                variable=var,
                style="TCheckbutton",
                command=lambda idx=index: self.update_done(idx)
            )
            checkbox.grid(row=index, column=0, sticky="w", pady=6)

    def update_done(self, idx):
        self.manager.tasks[idx].done = bool(self.vars[idx].get())
        self.manager.save()

    def add_task(self):
        title = self.user_inp.get().strip()
        if title:
            now = datetime.now()
            deadline = now + timedelta(days=1)
            task = {
                "title": title,
                "done": False,
                "time": now,
                "deadline": deadline
            }
            self.manager.add(task)
            self.user_inp.delete(0, tk.END)
            self.show_tasks()

    def delete_and_refresh(self):
        self.manager.delete()
        self.show_tasks()

    def on_focus_mode(self, time):
        # ✅ Ẩn toàn bộ widget
        for widget in self.all_widgets:
            widget.grid_remove()
        self.root.configure(bg="black")

        self.focus_mode = Focus(time)
        self.label_timer = self.ttk.Label(self.root, text="", font=("Arial", 72, "bold"), foreground="white", background="black")
        self.label_timer.place(relx=0.5, rely=0.5, anchor="center")  # ⭐ Đặt giữa

        self.exit_button = self.ttk.Button(self.root, text="⛔ Dừng lại", command= self.exit_focus_mode)
        self.exit_button.grid(row=1, column=0, columnspan=2)

        self.update_focus_timer(time)

    def update_focus_timer(self, time):
        still_running = self.focus_mode.time_left()
        self.label_timer.config(text=self.focus_mode.take_time())

        if still_running:
            self.root.after(1000, lambda: self.update_focus_timer(time))
        else:
            msg.showinfo(f"Hoàn thành!", f"Bạn đã hoàn thành {time} phút học tập trung!")
            self.focus_mode.save_time_done(int(time))
            self.exit_focus_mode()

    def exit_focus_mode(self):
        # ✅ Hiện lại toàn bộ widget
        for widget in self.all_widgets:
            widget.grid()
        self.label_timer.destroy()
        self.exit_button.destroy()
        self.root.configure(bg="#f0f4f8")
