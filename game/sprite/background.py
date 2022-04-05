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
                "image" : data.background["early_morning"],
                "time" : (3, 5)
            },
            {
                "image" : data.background["morning"],
                "time" : (5, 9)
            },
            {
                "image" : data.background["noon"],
                "time" : (9, 15)
            },
            {
                "image" : data.background["afternoon"],
                "time" : (15, 18)
            },
            {
                "image" : data.background["night"],
                "time" : (18, 21)
            },
            {
                "image" : data.background["midnight"],
                "time" : (21, 3)
            }
        ]
        
        self.time = time.time
        self.previous_hour = self.time.hour
        
        self.screen = screen
        self.image = None
        self.rect = None
        
        self.initialize = True
        self.update()
        
        
    def update(self):
        if self.initialize or self.time.hour != self.previous_hour:
            self.initialize = False
            self.previous_hour = self.time.hour
            
            is_midnight = True
            for background in self.backgrounds:
                if background["time"][0] >= self.previous_hour and \
                   background["time"][1] < self.previous_hour:
                       self.image = background["image"]
                       is_midnight = False
                       break
            
            if is_midnight:
                self.image = background[5]["image"]
                
            self.rect = self.image.get_rect()

        self.screen.blit(self.image, self.rect)
        