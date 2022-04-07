from tkinter import Toplevel
import pygame

class Button(pygame.sprite.Sprite):
    """
    Base class for constructing basic buttons with functionality and different
    states when hovered.
    """
    def __init__(self, screen, idle_image, 
                 hovered_image, callback_function, 
                 top_left_coordinates=None, 
                 center_coordinates=None):
        """
        Button interface to construct a hoverable button with function.

        Args:
            screen (pygame.Surface): The screen in which the button will appear onto
            idle_image (pygame.Image): Image of the button when it is idle
            hovered_image (pygame.Image): Image of the button when the cursor hovers onto it
            callback_function (function): Python function to run when the button is clicked
            top_left_coordinates (tuple, optional): x and y coordinates for the top-left of the button. Defaults to None.
            center_coordinates (tuply, optional): x and y coordinates of the center of the button. Defaults to None.
        """
        super().__init__()
        
        self.screen = screen
        self.state = "idle"
        self.visible = True
        
        self.idle = idle_image.convert_alpha()
        self.hovered = hovered_image.convert_alpha()
        
        self.center_coordinates = center_coordinates
        self.top_left_coordinates = top_left_coordinates
        
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
        if self.top_left_coordinates is None:
            self.rect.center = self.center_coordinates
        elif self.center_coordinates is None:
            self.rect.topleft = self.top_left_coordinates
        else:
            self.rect = (0, 0)
            
    def check_hovered(self, hover_coordinates):
        if self.rect.collidepoint(hover_coordinates):
            self.state = "hovered"
        else:
            self.state = "idle"
        
        self.set_image_and_rect()
        
    
    def check_clicked(self, click_coordinates):
        if self.rect.collidepoint(click_coordinates):
            self.callback()
            