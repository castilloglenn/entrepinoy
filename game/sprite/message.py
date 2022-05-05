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
                 add_background = False,
                 center_coordinates=None,
                 top_left_coordinates=None,
                 mid_bottom_coordinates=None):
        super().__init__()
        
        self.screen = screen
        
        self.messages = messages
        self.opacity = 255
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
        self.add_background = add_background
        
        self.image = None
        self.outline_image = None
        self.rect = None
        
        self.center_coordinates = center_coordinates
        self.top_left_coordinates = top_left_coordinates
        self.mid_bottom_coordinates = mid_bottom_coordinates
        
        # self.update()
        
        
    def update(self):
        for index, message in enumerate(self.messages):
            self.render_image(message)
            
            base_x = self.rect[0]
            base_y = self.rect[1] + (index * (self.text_spacing + self.size))
            
            if self.outline_image != None:
                for outline in range(self.outline_thickness):
                    self.screen.blit(self.outline_image, (base_x + (outline + 1), base_y))
                    self.screen.blit(self.outline_image, (base_x, base_y + (outline + 1)))
                    self.screen.blit(self.outline_image, (base_x - (outline + 1), base_y))
                    self.screen.blit(self.outline_image, (base_x, base_y - (outline + 1)))
            
            self.screen.blit(self.image, (base_x, base_y))
        
        
    def set_message(self, messages: list):
        self.messages = messages
        
        
    def set_opacity(self, opacity: int):
        # First time I will be using assert statements!
        assert opacity <= 255, "opacity must not exceed 255"
        assert opacity >= 0, "opacity must be zero or above"
        self.opacity = opacity
        
        
    def render_image(self, message: str):
        if self.outline_thickness > 0:
            self.outline_image = self.font.render(message, False, self.outline_color)
            self.outline_image.set_alpha(self.opacity)
        
        self.image = self.font.render(message, False, self.color)
        self.rect = self.image.get_rect()
        
        if self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.mid_bottom_coordinates is not None:
            self.rect.midtop = self.mid_bottom_coordinates
            
        self.image.set_alpha(self.opacity)
        