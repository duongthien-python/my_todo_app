from datetime import datetime
import json
import os

class Counting_UP:
    def __init__(self, path):
        self.path = path
        self.time_done = 0

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        if hasattr(self, 'start_time'):
            self.time_done += (datetime.now() - self.start_time).total_seconds()
            self.time_done = round(float(self.time_done/60), 2)  # Convert to minutes and truncate
            del self.start_time
    
    def get_time_done(self):
        return (datetime.now() - self.start_time).total_seconds()
    
    
    def save_time_done(self,time: None):
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                time_Done = json.load(f)
        except json.JSONDecodeError:
            time_Done = []
        time_Done.append({
            "time have done": self.time_done,
            "finished_at": datetime.now().isoformat()
        })

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(time_Done, f, indent=2, ensure_ascii=False)