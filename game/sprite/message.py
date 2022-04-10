from pygame.sprite import Sprite
from pygame.surface import Surface


class Message(Sprite):
    """
    This class will handle the displaying of message in the screen.
    """
    def __init__(self, screen: Surface, 
                 messages: list, font: dict, 
                 color: tuple, 
                 center_coordinates=None,
                 top_left_coordinates=None):
        super().__init__()
        
        self.screen = screen
        
        self.messages = messages
        self.font = font["family"]
        self.size = font["size"]
        self.color = color
        self.text_spacing = 3
        
        self.image = None
        self.rect = None
        
        self.center_coordinates = center_coordinates
        self.top_left_coordinates = top_left_coordinates
        
        
    def update(self):
        for index, message in enumerate(self.messages):
            self.render_image(message)
            self.screen.blit(
                self.image, 
                (self.rect[0], 
                 self.rect[1] 
                 + (index * (self.text_spacing + self.size)))
            )
        
        
    def set_message(self, messages: list):
        self.messages = messages
        
        
    def render_image(self, message: str):
        self.image = self.font.render(message, False, self.color)
        self.rect = self.image.get_rect()
        
        if self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        