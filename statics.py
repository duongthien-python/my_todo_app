from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import json

class static:
    def __init__(self,frame,path):
        self.path=path
        self.frame= frame
        self.data={}
        self.length=0
        self.widget=0
        self.take_data()

    def set_up(self):
        pass

    def take_data(self):
        with open(self.path,"r",encoding="utf-8") as f:
            try:
                raw= json.load(f)
                for item in raw:
                    time= (item["periods_done"] * 25)/60 if "periods_done" in item else item["time have done"]/60
                    day= datetime.fromisoformat(item["finished_at"]).date()
                    if day in self.data.keys():
                        self.data[day]+= time
                    else:
                        self.data[day]= time 
            except json.JSONDecodeError :
                print("file not found or something went wrong ")
    
    def dict_to_list(self):
        day = []
        time = []

        for data in sorted(self.data):
            day.append(data.strftime("%d %m"))
            time.append(self.data[data])
        self.length= len(day)
        return day, time


    def making_bar(self):
        if self.widget:
            self.widget.destroy()

        day, time = self.dict_to_list()
        day = day[-14:] 
        time = time[-14:]

        fig = Figure(figsize=(12,6), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(day, time)
        ax.set_title("Last 14 days")
        ax.set_ylabel("Hours studied")
        ax.set_xlabel("Date")
        # ax.plot(0,0,label="")
        # ax.legend(
        #     loc='best',
        #     fontsize=10,
        #     frameon=True,      # Có khung bao quanh
        #     shadow=True,       # Đổ bóng
        #     facecolor='white', # Màu nền
        #     edgecolor='black'  # Màu viền
        # )
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill="both", expand=True, side="top")

