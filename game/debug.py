from datetime import datetime


class Debugger():
    def __init__(self):
        self.time_format = datetime.today().strftime('%Y%m%d-%H%M%S%f')
        print(self.time_format)
        