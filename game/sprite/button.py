from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect


class Button(Sprite):
    """
    Base class for constructing basic buttons with functionality and different
    states when hovered.
    """
    def __init__(self, screen, callback_function, 
                 top_left_coordinates=None, 
                 center_coordinates=None, 
                 midbottom_coordinates=None,
                 collide_rect : tuple[float]=None,
                 **states):
        """
        Button interface to construct a hoverable button with function.

        Args:
            screen (pygame.Surface): The screen in which the button will appear onto
            callback_function (function): Python function to run when the button is clicked
            top_left_coordinates (_type_, optional): x and y coordinates for the top-left of the button. Defaults to None.. Defaults to None.
            center_coordinates (tuple, optional): x and y coordinates for the center of the button. Defaults to None.. Defaults to None.
            collide_rect (tuple[float], optional): relative percentage of the box where it is hoverable. 
                may input in percentages, (0.5, 0.5) means 50% smaller box is the hoverable range of the
                button/background. Defaults to None.
        """
        super().__init__()
        
        # Debugging
        self.show_bound = False
        self.bound_color = (255, 255, 255)
        self.bound_opacity = 128
        
        self.visible = True
        self.screen = screen
        self.state = "idle"
        self.callback = callback_function
        
        self.idle = states["idle"].convert_alpha()
        try:
            self.hovered = states["hovered"].convert_alpha()
        except KeyError:
            self.hovered = states["idle"].convert_alpha()
            self.outline = states["outline"].convert_alpha()
            self.hovered.blit(self.outline, (0, 0))
        
        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates
        
        self.image = self.idle
        self.rect = self.image.get_rect()
        self.collide_rect = None
        
        if self.top_left_coordinates != None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates != None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates != None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)
        
        # Collide rect refers to the inner rectangle of the button to where
        #   specifically the triggers function inside the box, this avoids
        #   triggering hover and callback function when targeting the transparent
        #   points inside the button/background
        self.collide_rect_rel = collide_rect
        if collide_rect == None:
            self.collide_rect_rel = (0, 0, 1, 1)
            
        self.collide_x = self.rect.x + self.rect.width * self.collide_rect_rel[0]
        self.collide_y = self.rect.y + self.rect.height * self.collide_rect_rel[1]
        self.collide_width = self.rect.width * self.collide_rect_rel[2]
        self.collide_height = self.rect.height * self.collide_rect_rel[3]
        
        # Screen surface (for displaying hitbox)
        self.hitbox = Surface((self.collide_width, self.collide_height))
        self.hitbox.fill(self.bound_color)
        self.hitbox.convert_alpha()
        self.hitbox.set_alpha(self.bound_opacity)
        
        self.set_image_and_rect()
        
        
    def update(self):
        if self.visible:
            self.collide_x = self.rect.x + self.rect.width * self.collide_rect_rel[0]
            self.collide_y = self.rect.y + self.rect.height * self.collide_rect_rel[1]
            self.screen.blit(self.image, self.rect)
        
            if self.show_bound:
                self.screen.blit(self.hitbox, (self.collide_x, self.collide_y)) 
            
        
    def set_image_and_rect(self):
        if self.state == "idle":
            self.image = self.idle
        elif self.state == "hovered":
            self.image = self.hovered
        
        self.rect = self.image.get_rect()
        if self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates != None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)
            
        self.collide_rect = Rect(
            self.collide_x, self.collide_y,
            self.collide_width, self.collide_height
        )
            
            
    def check_hovered(self, hover_coordinates):
        # Return booleans to prevent overlapping buttons to react the same
        if self.collide_rect.collidepoint(hover_coordinates):
            self.state = "hovered"
            self.set_image_and_rect()
            return True
        else:
            self.state = "idle"
            self.set_image_and_rect()
            return False
        
    
    def check_clicked(self, click_coordinates):
        if self.collide_rect.collidepoint(click_coordinates) and self.visible:
            self.callback(self)
        
        # Return booleans to prevent overlapping buttons to react the same
            return True
        return False
    
    
    def set_callback(self, new_callback):
        self.callback = new_callback
        
            