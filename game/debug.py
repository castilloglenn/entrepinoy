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
        file_path = os.path.join(dirname, "debug", self.file_name)
        
        self.text_file = open(file_path, "w+")
        self.log("Debug started")
        self.log(f"Log Date: {datetime.today().strftime('%Y/%m/%d-%H:%M:%S')}\n")
        
        
    def close(self):
        self.log(f"\nDebug Closed at: {datetime.today().strftime('%Y/%m/%d-%H:%M:%S')}")
        self.text_file.close()
        
        
    def log(self, log_message: str):
        self.text_file.write(log_message + "\n")
            
