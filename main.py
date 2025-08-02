from UI import UI
import os
from Manager import Manager
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

todo_path = get_path("todo.json")

if __name__ == "__main__":
    manager = Manager(todo_path)
    app = UI(manager)


