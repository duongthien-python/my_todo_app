import os
import json
from datetime import datetime

class Focus:
    def __init__(self, path, duration_minutes: int = 25):
        self.seconds_focus = duration_minutes * 60
        self.seconds_rest = 5 * 60 
        self.seconds_left = self.seconds_focus
        self.is_resting = False
        self.current_period = 0      
        self.periods_total = 0     
        self.path = path



    def start_pomodoro(self, periods_total=4, rest_minutes=5):
        self.periods_total = int(periods_total)
        self.seconds_focus = int(self.seconds_focus)  
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
            if self.is_resting:
                self.is_resting = False
                self.seconds_left = self.seconds_focus
                return self.current_period < self.periods_total
            else:
                self.current_period += 1
                if self.current_period >= self.periods_total:
                    return False
                else:
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
            return f"Đang học (#{self.current_period }/{self.periods_total})"

    def save_time_done(self,time: None):
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
                "time have done" : time,
                "finished_at" : datetime.now().isoformat()
            })

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(time_done, f, indent=2, ensure_ascii=False)


class focus_manager:
    def __init__ (self,path):
        self.path= path
    def delete():
        pass
    def save():
        pass