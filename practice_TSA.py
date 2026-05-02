import os, sys
class Practice:
    def __init__(self):
        self.done=False
        self.phrase=1
        self.duration=[60,30,60]
        self.seconds_left= self.duration[0]
    
    def tick(self):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            return True
        if self.seconds_left==0 and self.phrase<3:
            self.phrase+=1
            self.seconds_left= (self.duration[self.phrase-1] + 5) *60
            return True
        else:
            return False
            
    def save_data(self,path):
        if getattr(sys, 'frozen', False):
            # Đang chạy từ file .exe đã build
            base_path = os.path.dirname(sys.executable)
        else:
            # Đang chạy file .py trực tiếp
            base_path = os.path.dirname(os.path.abspath(__file__))
            path=os.path.join(base_path,path)
        
    