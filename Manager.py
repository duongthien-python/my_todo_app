import json
import os
from Task import Task 
from datetime import datetime

class Manager:
    def __init__(self, path):
        self.vars= []
        self.path = path
        self.tasks = []

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        task = Task(
                            title=item["title"],
                            done=item.get("done", False),
                            time=datetime.fromisoformat(item["time"]),
                            deadline=datetime.fromisoformat(item["deadline"])
                        )
                        self.tasks.append(task)
                except json.JSONDecodeError:
                    print("⚠️ File rỗng hoặc sai định dạng, bắt đầu mới.")

    def save(self,tasks=None):
        if tasks is None:
            tasks= self.tasks
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([{
                "title": t.title,
                "done": t.done,
                "time": t.time.isoformat(),
                "deadline": t.deadline.isoformat()
            } for t in tasks], f, indent=2, ensure_ascii=False)

    def add(self, task):
        task=Task.from_dict(task)
        self.tasks.append(task)
        self.save()

    def delete(self):
        self.tasks = [task for task in self.tasks if not task.done]
        self.save()

    
    



