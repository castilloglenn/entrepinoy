from datetime import datetime
from wmi import WMI
import os


class Debugger():
    """
    Handles all the recording of necessary data from the game to a text file.
    """
    def __init__(self):
        self.w = WMI('.')
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
        self.log(f"Debug closed")
        
        
    def log(self, log_message: str):
        time = datetime.today().strftime('[%H:%M:%S:%f')[:-3] + "] "
        with open(self.file_path, "a+") as text_file:
            text_file.write(time + log_message + "\n")
            
            
    def new_line(self):
        with open(self.file_path, "a+") as text_file:
            text_file.write("\n")


    def memory_log(self):
        """
        Source: https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
        Explanation: 
            Need a code that can give me the current memory usage of the program so I can monitor
            it and give adjustments and refactorings if necessary.
        """
        result = self.w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
        memory = int(result[0].WorkingSet) / 1000000
        self.log(f"Memory Usage: {memory:,.2f}MB")
