from game.sprite.background import Background
from game.sprite.button import Button
from game.library import Library
from game.debug import Debugger
from game.time import Time
import pygame



class Scene():
    """
    This will present the current location including: Stores, Time, Background
    and the controller menu
    """
    
    def __init__(self, main):
        # Settings up the scene
        self.main = main
        
        # Sprites and sprite groups
        self.general_sprites = pygame.sprite.Group()
        self.time = Time(
            self.main.data.progress["time"],
            self.main.data.setting["fps"],
            self.main.data.setting["time_amplify"]
        )
        
        self.running = True
        self.run()
                
                                
    def mouse_click_events(self, event):
        click_coordinates = event.pos
        
        # If the user clicked on left mouse button
        if event.button == 1: 
            # for button in self.buttons:
            #     button.check_clicked(click_coordinates)
            pass
            
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
            if event.buttons[0] == 1: pass

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1: pass
            
        # Hovering through display check
        else:
            # for button in self.buttons:
            #     button.check_hovered(self.last_mouse_pos)
            pass


    def key_events(self, keys):
        # If the user pressed the "del" key, (enter explanation here)
        if keys[pygame.K_DELETE]: 
            pass

        # If the user pressed the "a" key, (enter explanation here)
        if keys[pygame.K_a]: 
            pass

        # If the user pressed the "d" key, (enter explanation here)
        if keys[pygame.K_d]: 
            pass
        
    
    def refresh_display(self):
        self.main.refresh_display()
        self.time.tick()
        
        
    def run(self):
        while self.running:
            # Screen rendering
            self.main.screen.fill(self.main.data.white)
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                    self.main.close_game()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.mouse_click_events(event)
                if event.type == pygame.MOUSEMOTION: 
                    self.mouse_drag_events(event)
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_events(keys)
            
            # Updating the display
            self.refresh_display()
        
    