import pygame

from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.slider import Slider


class Setting():
    """
    Window to display the game setting and let the user configure it
    """
    def __init__(self, main):
        self.main = main
        self.running = False
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.draggable_buttons = pygame.sprite.Group()
        
        self.background = self.main.data.meta_images["window_background"].convert_alpha()
        self.ui_background_reference = MenuBackground(
            self.main.screen, 0.75,
            image=self.main.data.meta_images["menu_background"])
        self.ui_background = self.ui_background_reference.image
        self.ui_background_rect = self.ui_background_reference.rect
        
        self.business_title_message = Message(
            self.main.screen, 
            ["Setting"],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.ui_background_rect.width * 0.085) + self.ui_background_rect.x,
                int(self.ui_background_rect.height * 0.09) + self.ui_background_rect.y
            )
        )
        self.bgm_message = Message(
            self.main.screen, 
            ["BGM"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.ui_background_rect.width * 0.085) + self.ui_background_rect.x,
                int(self.ui_background_rect.height * 0.24) + self.ui_background_rect.y
            )
        )
        self.bgm_slider = Slider(
            self.main, "bgm",
            top_left_coordinates=(
                int(self.ui_background_rect.width * 0.166) + self.ui_background_rect.x,
                int(self.ui_background_rect.height * 0.2) + self.ui_background_rect.y
            )
        )
        self.sfx_message = Message(
            self.main.screen, 
            ["SFX"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.ui_background_rect.width * 0.085) + self.ui_background_rect.x,
                int(self.ui_background_rect.height * 0.38) + self.ui_background_rect.y
            )
        )
        self.sfx_slider = Slider(
            self.main, "sfx",
            top_left_coordinates=(
                int(self.ui_background_rect.width * 0.166) + self.ui_background_rect.x,
                int(self.ui_background_rect.height * 0.34) + self.ui_background_rect.y
            )
        )
        
        
        # Object additions
        self.business_title_message.add(self.objects)
        self.bgm_message.add(self.objects)
        self.sfx_message.add(self.objects)
        self.bgm_slider.add(self.objects, self.draggable_buttons)
        self.sfx_slider.add(self.objects, self.draggable_buttons)
                
                                
    def mouse_click_events(self, event):
        click_coordinates = event.pos
        
        # If the user clicked on left mouse button
        if event.button == 1: 
            for button in self.buttons:
                button.check_clicked(click_coordinates)

        # If the user clicked on the right mouse button
        if event.button == 3: 
            pass

        # If the user scrolls the mouse wheel upward
        if event.button == 4:  
            pass

        # If the user scrolls the mouse wheel downward
        if event.button == 5: 
            pass


    def mouse_drag_events(self, event):
        # This variable always saves the last mouse location to be used by the
        #   key_events() function, because we can't always get the location
        #   of the mouse if the only event is key press
        self.last_mouse_pos = event.pos

        # Making sure the user only holds one button at a time
        if event.buttons[0] + event.buttons[1] + event.buttons[2] == 1:
            # If the user is dragging the mouse with left mouse button
            if event.buttons[0] == 1:
                has_dragged = False
                for button in self.draggable_buttons:
                    if has_dragged:
                        button.undrag()
                    elif button.check_dragged(self.last_mouse_pos):
                        has_dragged = True

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1: pass
            
        # Hovering through display check
        else:
            for button in self.hoverable_buttons:
                button.check_hovered(self.last_mouse_pos)
            
            self.undrag_buttons()
                
                
    def key_down_events(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        
        elif key == pygame.K_F1:
            pass
            
        elif key == pygame.K_F2:
            pass
            
        elif key == pygame.K_F3:
            pass
            
        elif key == pygame.K_F4:
            pass


    def key_hold_events(self, keys):
        # If the user pressed the "del" key, (enter explanation here)
        if keys[pygame.K_DELETE]: 
            pass

        # If the user pressed the "a" key, (enter explanation here)
        if keys[pygame.K_a]: 
            pass

        # If the user pressed the "d" key, (enter explanation here)
        if keys[pygame.K_d]: 
            pass
        
    
    def undrag_buttons(self):
        for button in self.draggable_buttons:
            button.undrag()
        
        
    def run(self):
        self.running = True
        while self.running:
            # Screen rendering
            self.main.screen.blit(self.background, (0, 0))
            self.main.screen.blit(self.ui_background, self.ui_background_rect)
            
            # Updating sprites
            self.objects.update()
            
            # Event processing
            for event in pygame.event.get():
                if self.main.confirm_menu.enable:
                    self.main.confirm_menu.handle_event(event)
                else:
                    if event.type == pygame.QUIT: 
                        self.running = False
                        self.main.close_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN: 
                        self.mouse_click_events(event)
                    elif event.type == pygame.MOUSEMOTION: 
                        self.mouse_drag_events(event)
                    elif event.type == pygame.KEYDOWN:
                        self.key_down_events(event.key)
                    # For windwos with draggable buttons like sliders
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.undrag_buttons()
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_hold_events(keys)
            
            # Updating the display
            self.main.refresh_display()

        
