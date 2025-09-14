import os
import json
from datetime import datetime
import sys

def get_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

json_path = get_path("static.json")

class Focus:
    def __init__(self, duration_minutes=25):
        # duration_minutes: số phút mỗi phiên tập trung
        self.seconds_focus = int(duration_minutes) * 60
        self.seconds_rest = 5 * 60  # bạn có thể thay đổi (mặc định 5 phút)
        self.seconds_left = self.seconds_focus
        self.is_resting = False
        self.current_period = 0      # số phiên đã hoàn tất
        self.periods_total = 0      # tổng số phiên cần làm (set khi bắt đầu Pomodoro)
        self.path = json_path

    def nomarl_timer(self):
        if self.seconds_left>0:
            self.seconds_left -= 1
            return True
        else:
            return False



    def start_pomodoro(self, periods_total=4, rest_minutes=5):
        self.periods_total = int(periods_total)
        self.seconds_focus = int(self.seconds_focus)  # đảm bảo int
        self.seconds_rest = int(rest_minutes) * 60
        self.is_resting = False
        self.seconds_left = self.seconds_focus
        self.current_period = 0

    def tick(self):
        """
        Gọi mỗi giây. Trả True nếu vẫn còn đang chạy (chưa hoàn tất tất cả period),
        Trả False nếu đã hoàn tất toàn bộ Pomodoro.
        """
        if self.seconds_left > 0:
            self.seconds_left -= 1
            return True
        else:
            # Nếu đang nghỉ, kết thúc một chu kỳ nghỉ -> bắt đầu focus mới (nếu còn)
            if self.is_resting:
                self.is_resting = False
                self.seconds_left = self.seconds_focus
                # tiếp tục chạy nếu chưa hoàn tất all periods
                return self.current_period < self.periods_total
            else:
                # vừa kết thúc 1 phiên focus
                self.current_period += 1
                if self.current_period >= self.periods_total:
                    # hoàn tất toàn bộ chu kỳ
                    return False
                else:
                    # bắt đầu thời gian nghỉ
                    self.is_resting = True
                    self.seconds_left = self.seconds_rest
                    return True

    def get_time_str(self):
        s = self.seconds_left
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h:02}:{m:02}:{sec:02}"

    def get_status(self):
        if self.is_resting:
            return "Nghỉ ngơi"
        else:
            # hiện tại đang trong phiên tập trung, current_period là số hoàn tất
            return f"Đang học (#{self.current_period }/{self.periods_total})"

    def save_time_done(self,time: None):
        # Lưu lại số phiên đã hoàn tất
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                time_done = json.load(f)
        except json.JSONDecodeError:
            time_done = []
        if time is None:
            time_done.append({
                "periods_done": self.current_period,
                "finished_at": datetime.now().isoformat()
            })
        else:
            time_done.append({
                "time have done" : f"{time} minutes",
                "finished at" : datetime.now().isoformat()
            })

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(time_done, f, indent=2, ensure_ascii=False)
