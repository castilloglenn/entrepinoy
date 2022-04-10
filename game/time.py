from datetime import datetime, timedelta


class Time():
    """
    This class handles the time of the game.
    """
    def __init__(self, debug, start_time: str, 
                 fps: int, amplify: int, 
                 **callbacks):
        """
        Time class manipulates in-game time.

        Args:
            start_time (str): initial time setting from JSON
            fps (int): frames per second set
            amplify (int): time amplification versus real life time
        """
        # Time formatting
        self.format = "%Y/%m/%d, %H:%M:%S.%f"
        self.date_display_format = "%B %d, %Y"
        self.time_display_format = "%I:%M %p"
        self.increment = 86400 / amplify / fps
        
        # Recording of data
        debug.new_line()
        debug.log(
            f"\nTime amplification: \n"
            f"1 second in real life = {86400 / amplify:,.2f} second(s) in-game\n"
            f"{amplify / 60:,.2f} minutes in real life = 1 day in game")
        
        # Parse time
        self.time = datetime.strptime(start_time, self.format)
        
        # Time manager
        self.time_difference = 0
        self.previous_time = {}
        self.callbacks = callbacks
        self.update_previous_time()

        
    def tick(self):
        previous_tick_time = self.time
        self.time = self.time + timedelta(seconds=self.increment)
        
        if self.time.second != previous_tick_time.second:
            self.time_difference = self.time - previous_tick_time
            
            if self.previous_time["second"]["value"] != self.time.second:
                self.previous_time["second"]["function"](self.time_difference)
                
            if self.previous_time["minute"]["value"] != self.time.minute:
                self.previous_time["minute"]["function"]()
                
            if self.previous_time["hour"]["value"] != self.time.hour:
                self.previous_time["hour"]["function"]()
                
            if self.previous_time["day"]["value"] != self.time.day:
                self.previous_time["day"]["function"]()
                
            if self.previous_time["month"]["value"] != self.time.month:
                self.previous_time["month"]["function"]()
                
            if self.previous_time["year"]["value"] != self.time.year:
                self.previous_time["year"]["function"]()
                
            self.update_previous_time()
        
        
    def get_date(self):
        return datetime.strftime(self.time, self.date_display_format)
        
    
    def get_time(self):
        return datetime.strftime(self.time, self.time_display_format)
    

    def get_full(self):
        return datetime.strftime(self.time, self.format)
    
    
    def set_time(self, new_time):
        self.time = datetime.strptime(new_time, self.format)
    
    
    def update_previous_time(self):
        self.previous_time = {
            "second" : {
                "value" : self.time.second,
                "function" : self.callbacks["second"]
            },
            "minute" : {
                "value" : self.time.minute,
                "function" : self.callbacks["minute"]
            },
            "hour" : {
                "value" : self.time.hour,
                "function" : self.callbacks["hour"]
            },
            "day" : {
                "value" : self.time.day,
                "function" : self.callbacks["day"]
            },
            "month" : {
                "value" : self.time.month,
                "function" : self.callbacks["month"]
            },
            "year" : {
                "value" : self.time.year,
                "function" : self.callbacks["year"]
            },
        }


# if __name__ == "__main__":
#     Time("2022/04/05, 19:27:40.987123", 60, 300)
    