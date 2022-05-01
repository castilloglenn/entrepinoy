from game.sprite.message import Message
from game.sprite.button import Button
import pygame


class SlidingMenu():
    # TODO THIS WHOLE CLASS
    """
    This class displays a confirmation menu when certain actions have been taken.
    """
    def __init__(self, main):
        self.enable = False
        
        self.main = main
        self.callback = None
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Screen objects
        self.background = MenuBackground(
            self.main.screen, 0.40,
            image=self.main.data.meta_images["menu_background"])
        
        self.canvas_rect = self.background.rect
        self.confirmation_message = Message(
            self.main.screen, 
            ["No message has been set"],
            self.main.data.medium_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            center_coordinates=(
                int(self.canvas_rect.width * 0.50) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.175) + self.canvas_rect.y
            )
        )
        
        self.confirm_button = Button(
            self.main.screen, self.confirm,
            center_coordinates=(
                int(self.canvas_rect.width * 0.32) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.77) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.meta_images["confirm_button_idle"],
                "outline" : self.main.data.meta_images["confirm_button_hovered"]
            }
        )
        
        self.cancel_button = Button(
            self.main.screen, self.cancel,
            center_coordinates=(
                int(self.canvas_rect.width * 0.73) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.77) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.meta_images["cancel_button_idle"],
                "outline" : self.main.data.meta_images["cancel_button_hovered"]
            },
        )
        
        
        