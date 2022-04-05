from datetime import datetime, timedelta


class Time():
    """
    This class handles the time of the game.
    """
    def __init__(self, start_time: str, fps: int, amplify: int):
        """
        Time class manipulates in-game time.

        Args:
            start_time (str): initial time setting from JSON
            fps (int): frames per second set
            amplify (int): time amplification versus real life time
        """
        # Time formatting
        self.format = "%Y/%m/%d, %H:%M:%S.%f"
        self.increment = 86400 / amplify / fps
        
        # Parse time
        self.time = datetime.strptime(start_time, self.format)

        
    def tick(self):
        self.time = self.time + timedelta(seconds=self.increment)
        print(self.time)


# if __name__ == "__main__":
#     Time("2022/04/05, 19:27:40.987123", 60, 300)
    