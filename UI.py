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
        self.after_id = None
        self.setup_style()
        self.setup_ui()
        self.focus_mode = None
        self.root.mainloop()

    # ========== STYLE ==========
    def setup_style(self):
        self.root.title("TO DO APP ✨")
        self.root.geometry("700x800")
        self.root.configure(bg="#f0f4f8")
        self.style.theme_use("clam")

        self.style.configure("Rounded.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10, relief="flat",
            background="#8e44ad", foreground="white", borderwidth=0)
        self.style.map("Rounded.TButton", background=[("active", "#9b59b6")])

        self.style.configure("TCheckbutton",
            background="#f0f4f8", font=("Segoe UI", 11),
            foreground="#2c3e50", focuscolor="#f0f4f8")

        self.style.configure("TEntry",
            font=("Segoe UI", 11), padding=6, relief="flat")

        self.style.configure("TLabel",
            font=("Segoe UI", 14, "bold"),
            background="#f0f4f8", foreground="#34495e")

    # ========== UI CHÍNH ==========
    def setup_ui(self):
        self.ttk.Label(self.root, text="📋 Danh sách việc cần làm").grid(row=0, column=0, pady=20)
        self.frame_task = self.ttk.Frame(self.root)
        self.frame_task.grid(row=1, column=0, padx=20, sticky="w")

        self.user_inp = self.ttk.Entry(self.root, width=50)
        self.user_inp.grid(row=3, column=0, pady=20)

        self.time_entry = self.ttk.Entry(self.root, width=25)
        self.time_entry.insert(0, "25")
        self.time_entry.grid(row=3, column=1)

        button_frame = self.ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, pady=10)
        self.ttk.Button(button_frame, text="➕ Thêm daily task", style="Rounded.TButton", command= lambda: self.add_task("daily task")).grid(row=0, column=0, padx=10)
        self.ttk.Button(button_frame, text="➕ Thêm day task", style="Rounded.TButton", command= lambda: self.add_task("day task")).grid(row=0, column=1, padx=10)
        self.ttk.Button(button_frame, text="🧹 Xóa việc đã xong", style="Rounded.TButton", command=self.delete_and_refresh).grid(row=1, column=0, padx=10, pady= 10)
        self.ttk.Button(button_frame, text="biểu đồ hiệu suất", style="Rounded.TButton", command= self.thong_ke).grid(row=1, column=1, padx=10,pady=10)

        self.focus_button = self.ttk.Button(self.root, text="Bật chế độ học tập trung",
                                            command=lambda: self.start_focus_mode(int(self.time_entry.get())))
        self.focus_button.grid(row=2, column=1, pady=5)

        self.pomo_button = self.ttk.Button(self.root, text="🎯 Bắt đầu Pomodoro",
                                           command=self.start_pomodoro)
        self.pomo_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.all_widgets = self.root.winfo_children().copy()
        self.show_tasks()

    # ========== DANH SÁCH TASK ==========
    def show_tasks(self):
        for widget in self.frame_task.winfo_children():
            widget.destroy()
        self.vars.clear()
        for index, task in enumerate(self.manager.tasks):
            var = tk.IntVar(value=1 if task.done else 0)
            self.vars.append(var)
            deadline_str = task.deadline.strftime("%d/%m/%Y %H:%M")
            checkbox = self.ttk.Checkbutton(
                self.frame_task,
                text=f"{task.title}\n📅 Deadline: {deadline_str} \n phân loại: {task.loai} ",
                variable=var, style="TCheckbutton",
                command=lambda idx=index: self.update_done(idx)
            )
            checkbox.grid(row=index, column=0, sticky="w", pady=6)

    def update_done(self, idx):
        self.manager.tasks[idx].done = bool(self.vars[idx].get())
        self.manager.save()

    def add_task(self,loai):
        title = self.user_inp.get().strip()
        if title:
            now = datetime.now()
            deadline = now + timedelta(days=1)
            self.manager.add({"title": title,"loai": loai , "done": False, "time": now, "deadline": deadline})
            self.user_inp.delete(0, tk.END)
            self.show_tasks()

    def delete_and_refresh(self):
        self.manager.delete()
        self.show_tasks()

    # ========== UI CHUNG CHO TIMER ==========
    def create_timer_ui(self, bg_color, title=None, status=None):
        for widget in self.all_widgets:
            widget.grid_remove()
        self.root.configure(bg=bg_color)
        if title:
            self.title_label = self.ttk.Label(self.root, text=title, font=("Segoe UI", 20, "bold"),
                                              foreground="white", background=bg_color)
            self.title_label.grid(row=0, column=0, columnspan=2, pady=(30, 10))
        if status:
            self.status_label = self.ttk.Label(self.root, text=status, font=("Segoe UI", 14),
                                               foreground="white", background=bg_color)
            self.status_label.grid(row=1, column=0, columnspan=2, pady=10)
        self.timer_label = self.ttk.Label(self.root, text="", font=("Arial", 72),
                                          foreground="white", background=bg_color)
        self.timer_label.grid(row=2, column=0, columnspan=2, pady=20)
        self.stop_button = self.ttk.Button(self.root, text="⛔ Dừng lại", command=self.exit_timer_mode)
        self.stop_button.grid(row=3, column=0, columnspan=2, pady=10)

    # ========== TIMER CHUNG ==========
    def start_timer(self, tick_func, update_ui_func, on_finish):
        if not self.timer_label.winfo_exists():
            return
        running = tick_func()
        update_ui_func()
        if running:
            self.after_id = self.root.after(1000, lambda: self.start_timer(tick_func, update_ui_func, on_finish))
        else:
            on_finish()

    def exit_timer_mode(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        for widget in self.all_widgets:
            widget.grid()
        self.root.configure(bg="#f0f4f8")
        if hasattr(self, "timer_label"): self.timer_label.destroy()
        if hasattr(self, "title_label"): self.title_label.destroy()
        if hasattr(self, "status_label"): self.status_label.destroy()
        if hasattr(self, "stop_button"): self.stop_button.destroy()

    # ========== FOCUS MODE ==========
    def start_focus_mode(self, minutes):
        self.focus_mode = Focus(minutes)
        self.create_timer_ui("black")
        self.start_timer(
            tick_func=lambda: self.focus_mode.nomarl_timer(),
            update_ui_func=lambda: self.timer_label.config(text=self.focus_mode.get_time_str()),
            on_finish=lambda: [
                msg.showinfo("Hoàn thành!", f"Bạn đã hoàn thành {minutes} phút học tập trung!"),
                self.focus_mode.save_time_done(minutes),
                self.exit_timer_mode()
            ]
        )

    # ========== POMODORO MODE ==========
    def start_pomodoro(self):
        duration = 25
        periods = 4
        rest_minutes = 5
        self.focus_mode = Focus(duration)
        self.focus_mode.start_pomodoro(periods_total=periods, rest_minutes=rest_minutes)
        self.create_timer_ui("#1e272e", title="🧠 Pomodoro #1/4", status="📌 Trạng thái: Đang học")
        self.start_timer(
            tick_func=self.focus_mode.tick,
            update_ui_func=lambda: [
                self.timer_label.config(text=self.focus_mode.get_time_str()),
                self.status_label.config(text=f"📌 Trạng thái: {self.focus_mode.get_status()}")
            ],
            on_finish=lambda: [
                msg.showinfo("🎉 Xong rồi!", "Bạn đã hoàn thành tất cả các chu kỳ Pomodoro!"),
                self.focus_mode.save_time_done(),
                self.exit_timer_mode()
            ]
        )

    # ========== TẠO BẢNG THỐNG KÊ SỐ LIỆU ==========
    def thong_ke():
        pass
