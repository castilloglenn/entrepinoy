from datetime import datetime
import os


class Debugger():
    def __init__(self):
        self.save_only_previous_log = True
        
        if self.save_only_previous_log:
            self.file_name = "previous_log.txt"
        else:
            self.file_name = datetime.today().strftime("%Y%m%d-%H%M%S%f.txt")
            
        dirname = os.path.dirname(__file__)
        self.file_path = os.path.join(dirname, "debug", self.file_name)
        
        if self.save_only_previous_log:
            open(self.file_path, "w+").close()
        
        self.log("Debug started")
        self.new_line()
        
        
    def close(self):
        self.new_line()
        self.log(f"Debug closed")
        
        
    def log(self, log_message: str):
        time = datetime.today().strftime('[%H:%M:%S:%f')[:-3] + "] "
        with open(self.file_path, "a+") as text_file:
            text_file.write(time + log_message + "\n")
            
    def new_line(self):
        with open(self.file_path, "a+") as text_file:
            text_file.write("\n")
