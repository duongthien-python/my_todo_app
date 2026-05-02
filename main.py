from UI import UI
import os
from Manager import Manager
import sys

def get_path(list_files):
    path_files={}
    for filename in list_files: 
        if getattr(sys, 'frozen', False):
            # Đang chạy từ file .exe đã build
            base_path = os.path.dirname(sys.executable)
        else:
            # Đang chạy file .py trực tiếp
            base_path = os.path.dirname(os.path.abspath(__file__))
        path_files[filename]=os.path.join(base_path, filename)
    return path_files



# Ví dụ:
list_files=["todo.json","static.json"]
path = get_path(list_files)

if __name__ == "__main__":
    manager = Manager(path["todo.json"])
    app = UI(manager,path)

    