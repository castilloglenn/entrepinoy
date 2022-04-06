import pygame

class Button(pygame.sprite.Sprite):
    """
    Base class for constructing basic buttons with functionality and different
    states when hovered.
    """
    def __init__(self, screen, idle_image, 
                 hovered_image, center_coordinates, 
                 callback_function):
        super().__init__()
        
        self.screen = screen
        self.state = "idle"
        self.visible = True
        
        self.idle = idle_image
        self.hovered = hovered_image
        self.center_coordinates = center_coordinates
        
        self.image = None
        self.rect = None
        
        self.set_image_and_rect()
        self.callback = callback_function
        
        
    def update(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)
        
        
    def set_image_and_rect(self):
        if self.state == "idle":
            self.image = self.idle
        elif self.state == "hovered":
            self.image = self.hovered
        
        self.rect = self.image.get_rect()
        self.rect.center = self.center_coordinates
            
            
    def check_hovered(self, hover_coordinates):
        if self.rect.collidepoint(hover_coordinates):
            self.state = "hovered"
        else:
            self.state = "idle"
        
        self.set_image_and_rect()
        
    
    def check_clicked(self, click_coordinates):
        if self.rect.collidepoint(click_coordinates):
            self.callback()
            