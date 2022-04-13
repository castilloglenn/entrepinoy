from game.sprite.business import Business
from game.sprite.sprite_group import SpriteGroup
from game.sprite.scene_background import SceneBackground
from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button
from game.customer import Customer
from game.npc import NPC

from game.library import Library
from game.debug import Debugger
from game.time import Time

from datetime import datetime
from pprint import pprint
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
        self.customer_chance = self.main.data.customer_statistics[self.location]
        
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
        self.main.debug.log("Initialized scene")
        
        # Sprites and sprite groups
        self.general_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.crowd = SpriteGroup()
        
        # Scene components
        self.background = SceneBackground(
            self.main.screen, 
            self.time, 
            **self.main.data.background
        )
        self.background.add(self.general_sprites)
        
        # Internal variables
        self.business_data = {}
        # Safe spot is somewhere in the middle so that the customers will
        #   go there first before going to the back layer of businesses
        #   to avoid rendering confusions or going through walls
        # This is location-specific
        self.safe_spot = (0.5, 0.675)
        self.crowd_limit = 50
        
        # TODO business_1 will deprecate soon when dynamic scene builder is completed
        self.business_1 = Business(
            self.main.screen, 
            "sari_sari_store",
            self.business_1_callback,
            center_coordinates=(
                int(self.main.data.setting["game_width"] * 0.37),
                int(self.main.data.setting["game_height"] * 0.35)
            ), 
            collide_rect=(0.77, 1),
            **self.main.data.business_images["sari_sari_store"]
        )
        self.business_data["sari_sari_store"] = {}
        self.business_data["sari_sari_store"]["meta"] = self.main.data.business["sari_sari_store"]
        self.business_data["sari_sari_store"]["object"] = self.business_1
        self.business_1.add(self.general_sprites)
        pprint(self.business_data)
        
        self.profile_holder = Button(
            self.main.screen,
            self.profile_callback,
            top_left_coordinates=(10, 10),
            **{
                "idle" : self.main.data.scene["profile_holder_idle"],
                "outline" : self.main.data.scene["profile_holder_outline"]
            }
        )
        self.profile_holder.add(self.general_sprites)
        
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
        self.profile_message.add(self.general_sprites)
        
        # Buttons layering hierarchy (the top layer must be add first)
        self.profile_holder.add(self.buttons)
        self.business_1.add(self.buttons)
        
        # Main loop
        self.running = False
        
        
    def reset(self):
        self.location = "location_a" # TODO test location
        self.crowd_chance = self.main.data.crowd_statistics[self.location]
        self.time.set_time(self.main.data.progress["time"])
    
    
    def time_callback_seconds(self, time_amplification):
        # self.main.data.progress["cash"] += 1
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
        
    
    def business_1_callback(self):
        state = self.business_1.business_state
        if state == "open":
            self.business_1.set_business_state("closed")
        elif state == "closed":
            self.business_1.set_business_state("open")
            
            
    def check_queues_if_full(self):
        for name, data in self.business_data.items():
            if len(data["object"].queue) < data["object"].queue_limit:
                return False
        return True
            
            
    def spawn_crowd_customer(self):
        npc_chance = random.randint(0, 100) 
        if npc_chance <= self.crowd_chance[self.time.time.hour] \
                and len(self.crowd) < self.crowd_limit: 
            self.footprint_counter += 1 # TODO Deprecated
            npc_form = str(random.randint(0, 2))
            is_businesses_full = self.check_queues_if_full()
            
            customer_chance = random.randint(0, 100) 
            if customer_chance <= self.customer_chance[self.time.time.hour] \
                and not is_businesses_full:
                Customer(
                    self.main.screen, npc_form,
                    self.main.data.crowd_spritesheets[npc_form]["sheet"],
                    self.main.data.crowd_spritesheets[npc_form]["data"],
                    self.main.data.setting["fps"],
                    self.safe_spot, **self.business_data
                ).add(self.general_sprites, self.crowd)
            else:
                NPC(
                    self.main.screen, npc_form, 
                    self.main.data.crowd_spritesheets[npc_form]["sheet"],
                    self.main.data.crowd_spritesheets[npc_form]["data"],
                    self.main.data.setting["fps"]
                ).add(self.general_sprites, self.crowd)
                
                                
    def mouse_click_events(self, event):
        click_coordinates = event.pos
        
        # If the user clicked on left mouse button
        if event.button == 1: 
            for button in self.buttons:
                # Adding halting statement to prevent other buttons to
                #   react the same way/overlap reactions
                if button.check_clicked(click_coordinates):
                    break
            
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
            overlapped = False
            for button in self.buttons:
                # Adding halting statement to prevent other buttons to
                #   react the same way/overlap reactions
                if overlapped:
                    button.state = "idle"
                    button.set_image_and_rect()
                elif button.check_hovered(self.last_mouse_pos):
                    overlapped = True
                
                
    def key_down_events(self, key):
        self.main.global_key_down_events(key)
        
        if key == pygame.K_F1:
            self.main.debug.log(f"Objects in memory: {len(self.general_sprites)}")
            
        elif key == pygame.K_F2:
            self.main.debug.log("Exited scene via F2-shortcut")
            self.update_data()
            self.main.debug.log("Autosaved progress before exit")  
            self.running = False
            
        elif key == pygame.K_F3:
            self.business_data["sari_sari_store"]["object"].serve_customer()


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
        self.main.data.progress["last_login"] = datetime.strftime(
            datetime.now(), self.time.format)
        
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
                    self.spawn_crowd_customer()
                elif event.type == self.memory_debug_id:
                    self.main.debug.log(f"[A] Objects in memory: {len(self.general_sprites)}")
                    self.main.debug.memory_log()
                
            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_hold_events(keys)
            
            # Updating the display
            self.refresh_display()
        
    