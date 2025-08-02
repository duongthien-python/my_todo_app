import os
import json
from datetime import datetime
import sys

def get_path(filename):
    if getattr(sys, 'frozen', False):
        # Đang chạy từ file .exe đã build
        base_path = os.path.dirname(sys.executable)
    else:
        # Đang chạy file .py trực tiếp
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


# Ví dụ:
json_path = get_path("static.json")


class Focus:
    def __init__(self, duration):
        self.focus_mode = False
        self.focus_time_left = int(duration) * 60
        self.time = ""
        self.path = json_path

    def time_left(self):
        if self.focus_time_left > 0:
            self.focus_time_left -= 1
            hour = self.focus_time_left // 3600
            minutes = (self.focus_time_left % 3600) // 60
            seconds = self.focus_time_left % 60
            self.time = f"{hour:02}:{minutes:02}:{seconds:02}"
            return True
        else:
            return False

    def take_time(self):
        return self.time

    def reset(self, duration):
        self.focus_time_left = int(duration) * 60
        self.time = ""

    def save_time_done(self, time):
        # 🔧 Nếu file không tồn tại thì tạo mới
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

        # 🔧 Đọc dữ liệu cũ
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                time_done = json.load(f)
        except json.JSONDecodeError:
            time_done = []

        # 🔧 Thêm phiên mới
        time_done.append({
            "time have done": time,
            "study time have done on": datetime.now().isoformat()
        })

        # 🔧 Ghi lại
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(time_done, f, indent=2, ensure_ascii=False)
