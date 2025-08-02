class Task():
    def __init__(self,title,done,time,deadline):
        self.title= title
        self.done = done
        self.time= time
        self.deadline= deadline

    def to_dict(self):
        return {
            self.title,
            self.done,
            self.time,
            self.deadline
        }
    @staticmethod
    def from_dict(diction):
        return Task(
            diction["title"],
            diction["done"],
            diction["time"],
            diction["deadline"]
        )