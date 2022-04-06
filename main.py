from game.sprite.button import Button
from game.debug import Debugger
from game.library import Library

from scene import Scene

import pygame
import os, sys





class Main():
    """
    This will be the main module of the game.
    This runs the main menu of the game when played.
    """

    def __init__(self):
        # Centering the game window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Setting up the game
        pygame.init()
        pygame.mixer.init()
        self.debug = Debugger()
        self.data = Library()
        self.screen = None
        self.clock = None
        self.initialize_game()
        
        # Screen surface (for transitions)
        self.display_surface = pygame.Surface(
            (self.data.setting["game_width"], 
             self.data.setting["game_height"])
        )
        self.display_surface.fill(self.data.black)
        self.display_surface.convert_alpha()
        
        # Sprites and sprite groups
        self.buttons = pygame.sprite.Group()
        self.new_game_button = Button(
            self.screen, 
            self.data.title_screen["new_game_idle"],
            self.data.title_screen["new_game_hovered"],
                (
                    self.data.horizontal_center, 
                    int(self.data.setting["game_height"] * 0.65)
                ),
            self.create_new_game
        )
        self.continue_button = Button(
            self.screen, 
            self.data.title_screen["continue_idle"],
            self.data.title_screen["continue_hovered"],
                (
                    self.data.horizontal_center, 
                    int(self.data.setting["game_height"] * 0.85)
                ),
            self.continue_game
        )
        
        self.new_game_button.add(self.buttons)
        self.continue_button.add(self.buttons)
        
        # Mouse related variable
        self.last_mouse_pos = None
        
        # Introduction TODO temporarily disabled
        # self.intro_duration = self.data.meta["intro_duration"]
        # self.intro_transition = self.data.meta["intro_transition"]
        # self.present_intro()
        
        # Main loop
        self.running = True
        self.main_loop()
        
        
    def initialize_game(self):
        # Title
        pygame.display.set_caption(
            self.data.meta["title"] + " " +
            self.data.meta["version"]
        )
        self.debug.log(f"Game Title: {self.data.meta['title']}")
        self.debug.log(f"Game Version: {self.data.meta['version']}")
        
        # Icon
        pygame.display.set_icon(self.data.icon)
        
        # Setting the screen size
        self.screen = pygame.display.set_mode(
            (self.data.setting["game_width"],
            self.data.setting["game_height"])
        )
        self.debug.log(f"Display Width: {self.data.setting['game_width']}")
        self.debug.log(f"Display Height: {self.data.setting['game_height']}")
        
        # Setting the clock
        self.clock = pygame.time.Clock()
        self.debug.log(f"Game FPS: {self.data.setting['fps']}")
        
    
    def refresh_display(self):
        pygame.display.update()
        self.clock.tick(self.data.setting["fps"])
        
        
    def close_game(self):
        pygame.mixer.quit()
        pygame.quit()
        self.debug.close()
        sys.exit()
                
                                
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
            if event.buttons[0] == 1: pass

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1: pass
            
        # Hovering through display check
        else:
            for button in self.buttons:
                button.check_hovered(self.last_mouse_pos)


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
        
        
    def create_new_game(self):
        self.debug.log("Create new game entered")
        Scene(self)
        
        
    def continue_game(self):
        self.debug.log("Continue game entered")
        
        
    def present_intro(self):
        intro = True
        second = 0
        frame_count = 0
        alpha = 255
        increment = (255 / self.data.setting["fps"]) / self.intro_transition
        fade = "in" # values: in, out, hold
        
        while intro:
            # Screen rendering
            self.screen.fill(self.data.white)
            self.screen.blit(self.data.studio, (0, 0))
            self.display_surface.set_alpha(alpha)
            
            if fade == "in":
                alpha -= increment
                alpha = max(alpha, 0)
            elif fade == "out":
                alpha += increment
                alpha = min(alpha, 255)
                
            self.screen.blit(self.display_surface, (0, 0)) 
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    # Closing the game properly
                    self.close_game()
            
            # Updating the display
            self.refresh_display()
            
            frame_count += 1
            if frame_count == self.data.setting["fps"]:
                frame_count = 0
                second += 1
                
                if fade == "in" and second >= self.intro_transition:
                    fade = "hold"
                    second = 0
                elif fade == "hold" and second >= self.intro_duration:
                    fade = "out"
                    second = 0
                elif fade == "out" and second >= self.intro_transition:
                    intro = False
        
        
    def main_loop(self):
        self.debug.new_line()
        while self.running:
            # Screen rendering
            self.screen.fill(self.data.white)
            self.screen.blit(self.data.title_screen["bg"], (0, 0))
            
            # Updating sprites
            self.buttons.update()
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.mouse_click_events(event)
                if event.type == pygame.MOUSEMOTION: 
                    self.mouse_drag_events(event)
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_events(keys)
            
            # Updating the display
            self.refresh_display()
        
        # Closing the game properly
        self.close_game()


if __name__ == "__main__":
    Main()
