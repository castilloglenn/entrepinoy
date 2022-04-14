from datetime import datetime
import psutil
import os


class Debugger():
    """
    Handles all the recording of necessary data from the game to a text file.
    """
    def __init__(self):
        self.highest_memory = 0
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
        self.memory_log()
        self.new_line()
        
        
    def close(self):
        self.new_line()
        self.memory_log()
        self.log(f"Debug closed")
        
        
    def log(self, log_message: str):
        time = datetime.today().strftime('[%H:%M:%S:%f')[:-3] + "] "
        with open(self.file_path, "a+") as text_file:
            text_file.write(time + log_message + "\n")
            
            
    def new_line(self):
        with open(self.file_path, "a+") as text_file:
            text_file.write("\n")


    def memory_log(self):
        self.log(self.get_memory_usage())
        self.log(self.get_free_usage())
        self.log(self.get_highest_usage())
        
        
    def get_memory_usage(self):
        current_usage = psutil.Process().memory_info().rss / (1024 * 1024)
        if current_usage > self.highest_memory:
            self.highest_memory = current_usage
            
        virtual_mem = psutil.virtual_memory()
        percent = virtual_mem.percent
        return f"Memory Usage: {current_usage:,.2f}MB ({percent}%)"
    
    def get_free_usage(self):
        free = psutil.virtual_memory().free / 1024 / 1024
        return f"Free Memory: {free:,.2f}MB"
        
        
    def get_highest_usage(self):
        return f"Highest Usage: {self.highest_memory:,.2f}MB"
