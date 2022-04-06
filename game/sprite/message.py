import pygame


class Message(pygame.sprite.Sprite):
    """
    This class will handle the displaying of message in the screen.
    """
    def __init__(self, screen: pygame.Surface, 
                 messages: list, font: dict, 
                 color: tuple, coordinates: tuple):
        """
        Handling message display on the screen

        Args:
            screen (pygame.Surface): pygame display for the message to displayed at
            message (str): message to display
            font (dict): pygame font to be used
            color (tuple): 3-integer tuple from 0 to 255 RGB value
            coordinates (tuple): x, y coordinates on the screen
        """
        super().__init__()
        
        self.screen = screen
        
        self.messages = messages
        self.font = font["family"]
        self.size = font["size"]
        self.color = color
        self.text_spacing = 3
        
        self.image = None
        self.rect = None
        self.coordinates = coordinates
        
        
    def update(self):
        for index, message in enumerate(self.messages):
            self.render_image(message)
            self.screen.blit(
                self.image, 
                (self.coordinates[0], 
                 self.coordinates[1] 
                 + (index * (self.text_spacing + self.size)))
            )
        
        
    def set_message(self, messages: list):
        self.messages = messages
        
        
    def render_image(self, message: str):
        self.image = self.font.render(message, False, self.color)
        self.rect = self.image.get_rect()
        