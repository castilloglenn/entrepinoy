from game.sprite.sprite_group import SpriteGroup
from game.sprite.scene_background import SceneBackground
from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button
from game.npc import NPC

from game.library import Library
from game.debug import Debugger
from game.time import Time

import pygame
import random


class Scene():
    """
    This will present the current location including: Stores, Time, Background
    and the controller menu
    """
    
    def __init__(self, main):
        # Settings up the scene
        self.main = main
        self.location = "location_a" # TODO test location
        self.crowd_chance = self.main.data.crowd_statistics[self.location]
        
        # Setting up the clock
        self.callbacks = {
            "second" : self.time_callback_seconds,
            "minute" : self.time_callback_minute,
            "hour" : self.time_callback_hour,
            "day" : self.time_callback_day,
            "month" : self.time_callback_month,
            "year" : self.time_callback_year
        }
        self.time = Time(
            self.main.debug,
            self.main.data.progress["time"],
            self.main.data.setting["fps"],
            self.main.data.setting["time_amplify"],
            **self.callbacks
        )
        
        # CUSTOM EVENTS
        # Setting up the autosave feature
        self.autosave_id = pygame.USEREVENT + 1
        pygame.time.set_timer(
            self.autosave_id, 
            self.main.data.setting["autosave_timeout"]
        )
        # Crowd spawner
        self.crowd_spawner_id = pygame.USEREVENT + 2
        pygame.time.set_timer(
            self.crowd_spawner_id,
            500
        )
        # Memory monitoring
        self.footprint_counter = 0
        self.memory_debug_id = pygame.USEREVENT + 3
        pygame.time.set_timer(
            self.memory_debug_id,
            60000
        )
        
        # Logging entry point
        self.main.debug.new_line()
        self.main.debug.log("Entered scene")
        
        # Sprites and sprite groups
        self.general_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.crowd = SpriteGroup()
        self.background = SceneBackground(
            self.main.screen, 
            self.time, 
            **self.main.data.background
        )
        
        # Scene components
        self.profile_holder = Button(
            self.main.screen,
            self.main.data.scene["profile_holder_idle"],
            self.main.data.scene["profile_holder_hovered"],
            self.profile_callback,
            top_left_coordinates=(10, 10)
        )
        self.profile_message = Message(
            self.main.screen, 
                [
                    self.time.get_date(), 
                    self.time.get_time(),
                    "Cash:",
                    f"P{self.main.data.progress['cash']:15,.2f}"
                ], 
            self.main.data.small_font, 
            self.main.data.colors["orange"],
            top_left_coordinates=(160, 75)
        )
        self.background.add(self.general_sprites)
        self.profile_holder.add(self.general_sprites, self.buttons)
        self.profile_message.add(self.general_sprites)
        
        # Main loop
        self.running = False
        
        
    def reset(self):
        self.time.set_time(self.main.data.progress["time"])
    
    
    def time_callback_seconds(self, time_amplification):
        pass
        
    
    def time_callback_minute(self):
        self.profile_message.set_message([
            self.time.get_date(), 
            self.time.get_time(),
            "Cash:",
            f"P{self.main.data.progress['cash']:15,.2f}"
        ])
        
    
    def time_callback_hour(self):
        self.main.debug.log("Hour callback")
        self.background.set_time(self.time)
        self.background.check_change()
        
    
    def time_callback_day(self):
        self.main.debug.log("Day callback")
        
    
    def time_callback_month(self):
        self.main.debug.log("Month callback")
        
    
    def time_callback_year(self):
        self.main.debug.log("Year callback")
    
    
    def profile_callback(self):
        self.main.debug.log("Profile clicked")
                
                                
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
                
                
    def key_down_events(self, key):
        self.main.global_key_down_events(key)
        if key == pygame.K_F1:
            self.main.debug.log(f"Objects in memory: {len(self.general_sprites)}")
        elif key == pygame.K_F2:
            self.main.debug.log("Exited scene via F2-shortcut")
            self.update_data()
            self.main.debug.log("Autosaved progress before exit")  
            self.running = False


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
        
    
    def refresh_display(self):
        self.main.refresh_display()
        self.time.tick()
        
    
    def update_data(self):
        # Update the json data from the main class
        self.main.data.progress["time"] = self.time.get_full()
        
        # Saving the json to the save file
        self.main.data.set_dict_to_json(
            "progress", "progress.json",
            self.main.data.progress
        )
        
        
    def close_game(self):
        self.update_data()
        self.main.debug.log("Autosaved progress before exit")
        self.main.close_game()
        
        
    def run(self):
        self.main.debug.log(f"Initial memory and object statistics:")
        self.main.debug.log(f"Total crowd objects: {len(self.general_sprites)}")
        self.main.debug.memory_log()
        self.main.debug.new_line()
        
        self.running = True
        while self.running:
            # Rendering sprites
            self.general_sprites.update()
            self.crowd.draw(self.main.screen)
            
            self.main.data.progress["cash"] += 1
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                    self.close_game()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    self.mouse_click_events(event)
                elif event.type == pygame.MOUSEMOTION: 
                    self.mouse_drag_events(event)
                elif event.type == pygame.KEYDOWN:
                    self.key_down_events(event.key)
                
                # Custom event timers
                elif event.type == self.autosave_id:
                    self.update_data()
                    self.main.debug.log("Autosaved progress")
                elif event.type == self.crowd_spawner_id:
                    random_value = random.randint(0, 100)
                    if random_value <= self.crowd_chance[self.time.time.hour]:
                        self.footprint_counter += 1
                        npc_form = str(random.randint(0, 1))
                        NPC(
                            self.main.screen, npc_form, 
                            self.main.data.crowd_spritesheets[npc_form]["sheet"],
                            self.main.data.crowd_spritesheets[npc_form]["data"],
                            self.main.data.setting["fps"]
                        ).add(self.general_sprites, self.crowd)
                elif event.type == self.memory_debug_id:
                    self.main.debug.log(f"[A] Objects in memory: {len(self.general_sprites)}")
                    self.main.debug.memory_log()
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_hold_events(keys)
            
            # Updating the display
            self.refresh_display()
        
    