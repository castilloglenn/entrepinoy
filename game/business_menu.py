from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
import pygame


class BusinessMenu():
    """
    This class will handle menu that is related to businesses when they are
    clicked. This will contain the details, buttons to manage the business
    and the profits and loss statistics.
    """
    def __init__(self, main):
        self.main = main
        self.screen = self.main.screen
        self.data = None
        
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
            self.main.data.medium_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.05) + self.canvas_rect.y
            )
        )
        
        
    def set_data(self, data):
        self.data = data
        
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()
        
        self.background.add(self.objects, self.buttons)
        self.business_title_message.set_message([self.data.name])
        self.business_title_message.add(self.objects)
        
        
    def run(self):
        # Screen dimming
        self.main.display_surface.set_alpha(128)
        self.screen.blit(self.main.display_surface, (0, 0)) 
        
        self.background.enable = True
        while self.background.enable:
            self.objects.update()
            
            # Event processing
            for event in pygame.event.get():
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
            
            # Updating the display
            self.main.refresh_display()
