from pygame.sprite import Sprite
from pygame.surface import Surface


class Message(Sprite):
    """
    This class will handle the displaying of message in the screen.
    """
    def __init__(self, screen: Surface, 
                 messages: list, font: dict, 
                 color: tuple, 
                 outline_color: tuple | None = None,
                 outline_thickness: int = 0,
                 center_coordinates=None,
                 top_left_coordinates=None):
        super().__init__()
        
        self.screen = screen
        
        self.messages = messages
        self.font = font["family"]
        self.size = font["size"]
        
        self.color = color
        if outline_color == None:
            # Default color
            self.outline_color = (0, 0, 0)
        else:
            self.outline_color = outline_color
        
        self.text_spacing = 3
        self.outline_thickness = outline_thickness
        
        self.image = None
        self.outline_image = None
        self.rect = None
        
        self.center_coordinates = center_coordinates
        self.top_left_coordinates = top_left_coordinates
        
        
    def update(self):
        for index, message in enumerate(self.messages):
            self.render_image(message)
            
            # testing with outline
            base_x = self.rect[0]
            base_y = self.rect[1] + (index * (self.text_spacing + self.size))
            
            if self.outline_image != None:
                self.screen.blit(self.outline_image, (base_x + self.outline_thickness, base_y))
                self.screen.blit(self.outline_image, (base_x, base_y + self.outline_thickness))
                self.screen.blit(self.outline_image, (base_x - self.outline_thickness, base_y))
                self.screen.blit(self.outline_image, (base_x, base_y - self.outline_thickness))
            
            self.screen.blit(self.image, (base_x, base_y))
        
        
    def set_message(self, messages: list):
        self.messages = messages
        
        
    def render_image(self, message: str):
        if self.outline_thickness > 0:
            self.outline_image = self.font.render(message, False, self.outline_color)
        
        self.image = self.font.render(message, False, self.color)
        self.rect = self.image.get_rect()
        
        if self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        