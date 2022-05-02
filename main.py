from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button

from game.response_menu import ResponseMenu
from game.sliding_menu import SlidingMenu
from game.confirm_menu import ConfirmMenu

from game.debug import Debugger
from game.library import Library

from scene_builder import Scene

import pygame
import os, sys


class Main():
    """
    This will be the main module of the game.
    This runs the main menu of the game when played.
    """
    def __init__(self):
        # Setting up the debugger
        self.debug = Debugger()
        
        # Centering the game window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = "1"
        
        # Setting up the game
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_cursor(pygame.cursors.tri_left)
        
        # Setting up the data
        self.data = Library()
        self.screen = None
        self.clock = None
        self.initialize_game()
        
        # Screen surface (for transitions)
        self.display_surface = pygame.Surface(
            (self.data.setting["game_width"], 
             self.data.setting["game_height"])
        )
        self.display_surface.fill(self.data.colors["black"])
        self.display_surface.convert_alpha()
            
        # Menus
        self.sliding_menu = SlidingMenu(self)
        self.confirm_menu = ConfirmMenu(self)
        self.response_menu = ResponseMenu(self)
        
        # Setting up other windows
        self.scene_window = Scene(self)
        
        # Sprites and sprite groups
        self.buttons = pygame.sprite.Group()
        self.new_game_button = Button(
            self.screen, 
            self.check_save_file,
            center_coordinates=
                (self.data.horizontal_center, 
                int(self.data.setting["game_height"] * 0.65)),
            **{
                "idle" : self.data.title_screen["new_game_idle"],
                "outline" : self.data.title_screen["new_game_hovered"],
            }
        )
        self.new_game_button.add(self.buttons)
        
        self.continue_button = Button(
            self.screen, 
            self.continue_game,
            center_coordinates=
                (self.data.horizontal_center, 
                int(self.data.setting["game_height"] * 0.82)),
            **{
                "idle" : self.data.title_screen["continue_idle"],
                "outline" : self.data.title_screen["continue_hovered"],
            }
        )
        self.continue_button_included = False
        if self.data.progress is not None:
            self.continue_button.add(self.buttons)
        
        # Mouse related variable
        self.last_mouse_pos = None
        
        # Introduction TODO temporarily disabled
        # self.intro_duration = self.data.meta["intro_duration"]
        # self.intro_transition = self.data.meta["intro_transition"]
        # self.present_intro()
        
        # Main loop
        self.debug.log("Memory after initialization:")
        self.debug.memory_log()
        
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
        pygame.display.set_icon(self.data.meta_images["icon"])
        
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
                
                
    def global_key_down_events(self, key):
        if key == pygame.K_F1:
            self.debug.log(f"F1 Trigger: Memory check")
            self.debug.memory_log()
        
    
    def check_save_file(self, *args):
        if self.data.progress == None:
            self.create_new_game()
        else:
            self.confirm_menu.set_message_and_callback(
                ["Are you sure you want",
                " to start a new game?", "",
                "All your progress will", 
                "be reset."],
                self.create_new_game
            )
            self.confirm_menu.enable = True
        
        
    def create_new_game(self):
        self.debug.log("Create new game entered")
        self.data.create_new_save_file("buko_stall")
        
        self.scene_window.reset()
        self.scene_window.run()
        
        
    def continue_game(self, *args):
        self.debug.new_line()
        self.debug.log("Continue game entered")
        self.scene_window.run()
        
        
    def present_intro(self):
        intro = True
        second = 0
        frame_count = 0
        alpha = 255
        increment = (255 / self.data.setting["fps"]) / self.intro_transition
        fade = "in" # values: in, out, hold
        
        while intro:
            # Screen rendering
            self.screen.blit(self.data.meta_images["studio"], (0, 0))
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
        while self.running:
            # Screen rendering
            self.screen.blit(self.data.title_screen["bg"], (0, 0))
            
            # Updating sprites
            self.buttons.update()
            
            # Checking if menus will be displaying
            self.confirm_menu.update()
            
            # Event processing
            for event in pygame.event.get():
                if self.confirm_menu.enable:
                    self.confirm_menu.handle_event(event)
                else:
                    if event.type == pygame.QUIT: 
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN: 
                        self.mouse_click_events(event)
                    elif event.type == pygame.MOUSEMOTION: 
                        self.mouse_drag_events(event)
                    elif event.type == pygame.KEYDOWN:
                        self.global_key_down_events(event.key)
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_events(keys)
            
            # Final checks on the continue button for initial game exit to menu
            if self.data.progress is not None and not self.continue_button_included:
                self.continue_button_included = True
                self.continue_button.add(self.buttons)
            
            # Updating the display
            self.refresh_display()
        
        # Closing the game properly
        self.close_game()


if __name__ == "__main__":
    Main()
