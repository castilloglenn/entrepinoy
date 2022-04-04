from black import main
from game.library import Library
import pygame
import os, sys



class Main():
    """
    This will be the main module of the game.
    """

    def __init__(self):
        # Setting up the game
        self.data = Library()
        self.screen = None
        self.clock = None
        self.initialize_game()
        
        # Centering the game window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Sprites and sprite groups
        self.all_sprites = pygame.sprite.Group()
        
        # Main loop
        self.running = True
        self.main_loop()
        
        
    def initialize_game(self):
        pygame.init()
        pygame.mixer.init()
        
        # Title
        pygame.display.set_caption(
            self.data.meta["title"] + " " +
            self.data.meta["version"]
        )
        
        # Icon
        pygame.display.set_icon(self.data.icon)
        
        # Setting the screen size
        self.screen = pygame.display.set_mode(
            (self.data.setting["game_width"],
            self.data.setting["game_height"])
        )
        
        # Setting the clock
        self.clock = pygame.time.Clock()
        
    
    def refresh_display(self):
        pygame.display.update()
        self.clock.tick(self.data.setting["fps"])
        
        
    def close_game(self):
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()
        
        
    def input_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                self.mouse_click_events(event)
                
            if event.type == pygame.MOUSEMOTION: 
                self.mouse_drag_events(event)
                
                                
    def mouse_click_events(self, event):
        # If the user clicked on left mouse button
        if event.button == 1: 
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
            # relativeLocation = getRelativeLocation(event.pos)

            # If the user is dragging the mouse with left mouse button
            if event.buttons[0] == 1: pass

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1: pass


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
        
        
    def main_loop(self):
        while self.running:
            # Screen rendering
            self.screen.blit
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                self.input_events(event)
                
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_events(keys)
                
            # Updating sprites TODO can change
            self.all_sprites.update()
            
            # Updating the display
            self.refresh_display()
        
        # Closing the game properly
        self.close_game()


if __name__ == "__main__":
    Main()
