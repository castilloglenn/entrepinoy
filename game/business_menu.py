from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button
import pygame

from pprint import pprint


class BusinessMenu():
    """
    This class will handle menu that is related to businesses when they are
    clicked. This will contain the details, buttons to manage the business
    and the profits and loss statistics.
    """
    def __init__(self, main, location):
        self.enable = False
        
        self.main = main
        self.screen = self.main.screen
        self.data = None
        self.location = location
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Screen objects
        self.background = MenuBackground(
            self.screen, 0.75,
            image=self.main.data.meta_images["menu_background"])
        
        self.canvas_rect = self.background.rect
        self.business_title_message = Message(
            self.screen, 
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.05) + self.canvas_rect.y
            )
        )
        self.business_tier_and_size = Message(
            self.screen, 
            [""],
            self.main.data.small_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.11) + self.canvas_rect.y
            )
        )
        self.collect_sales_button = Button(
            self.screen,
            self.collect_sales_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.71) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["collect_sales_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["collect_sales_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["collect_sales_button_disabled"].convert_alpha()
            }
        )
        
        # Screen dimming
        self.main.display_surface.set_alpha(128)
        
        
    def get_sales(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"]
    
    
    def clear_sales(self):
        self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"] = 0
        
        
    def collect_sales_button_callback(self, *args):
        self.collect_sales_button.set_is_disabled(True)
        self.main.data.progress["cash"] += self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"]
        self.clear_sales()
        
        
    def set_button_states(self):
        if self.get_sales() <= 0:
            self.collect_sales_button.set_is_disabled(True)
        else:
            self.collect_sales_button.set_is_disabled(False)
            
            
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        self.set_button_states()
        
        
    def set_data(self, data):
        self.data = data
        
        self.clear()
        self.background.add(self.objects, self.buttons)
        
        # Data set
        self.business_title_message.set_message([self.data.business_data["name"]])
        self.business_tier_and_size.set_message([
            f"Tier {self.main.data.category[self.data.name_code]['tier']} - "
            f"{self.main.data.category[self.data.name_code]['size']} Business"
        ])
        
        # Object add
        self.business_title_message.add(self.objects)
        self.business_tier_and_size.add(self.objects)
        self.collect_sales_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
        self.set_button_states()
        self.background.enable = True
        
        pprint(self.data)
        pprint(self.main.data.progress)
        
    
    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()
        
        
    def handle_event(self, event):
        if not self.enable:
            return
    
        if event.type == pygame.QUIT: 
            # Closing the game properly
            self.main.close_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.background.enable = False
        elif event.type == pygame.MOUSEMOTION: 
            for button in self.hoverable_buttons:
                button.check_hovered(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    button.check_clicked(mouse_pos)
        
        if not self.background.enable:
            self.close()
        
        
    def update(self):
        if not self.enable:
            return
        
        if self.background.enable:
            # Updating the data
            self.update_data()
            
            self.screen.blit(self.main.display_surface, (0, 0)) 
            self.objects.update()
        
        
    def close(self):
        self.clear()
        self.enable = False
