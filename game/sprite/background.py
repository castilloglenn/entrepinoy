import pygame

from game.time import Time

class Background(pygame.sprite.Sprite):
    """
    This sprite handles the appropriate background for a specific time of in-game day.
    """
    def __init__(self, screen: pygame.Surface, time: Time, **data):
        """
        Background of the scene in the game.

        Args:
            screen (pygame.Surface): Display for the background to update
            time (Time): Time class to get the specific time to update the background
        """
        super().__init__()
        
        # Different backgrounds
        self.backgrounds = [
            {
                "image" : data["early_morning"],
                "time" : (3, 5)
            },
            {
                "image" : data["morning"],
                "time" : (5, 9)
            },
            {
                "image" : data["noon"],
                "time" : (9, 15)
            },
            {
                "image" : data["afternoon"],
                "time" : (15, 18)
            },
            {
                "image" : data["night"],
                "time" : (18, 21)
            },
            {
                "image" : data["midnight"],
                "time" : (21, 3)
            }
        ]
        
        self.time = time.time
        
        self.screen = screen
        self.image = None
        self.rect = None
        
        self.initialize = True
        self.check_change()
        
        
    def update(self):
        self.screen.blit(self.image, self.rect)
        
    
    def set_time(self, time: Time):
        self.time = time.time
        
    
    def check_change(self):
        self.current_hour = self.time.hour
        
        is_midnight = True
        for background in self.backgrounds:
            inc_start_time = background['time'][0]
            exc_end_time = background['time'][1]
            
            if self.current_hour >= inc_start_time and self.current_hour < exc_end_time:
                self.image = background["image"]
                is_midnight = False
                break
        
        if is_midnight:
            self.image = self.backgrounds[5]["image"]
            
        self.rect = self.image.get_rect()
            