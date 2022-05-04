from game.sprite.business import Business
from game.sprite.sprite_group import SpriteGroup
from game.sprite.scene_background import SceneBackground
from game.sprite.message import Message
from game.sprite.button import Button

from game.business_menu import BusinessMenu
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
        self.show_debug_info = True
        
        self.location = self.main.data.progress["last_location"]
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
            self.main.data.meta["time_amplify"],
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
            self.main.data.meta["crowd_spawn_timeout"]
        )
        # Memory monitoring
        self.footprint_counter = 0
        self.customers_spawned = 0
        self.memory_debug_id = pygame.USEREVENT + 3
        pygame.time.set_timer(
            self.memory_debug_id,
            self.main.data.meta["memory_log_timeout"]
        )
        # FPS Counter
        self.fps_previous_count = 0
        self.fps_counter = 0
        self.fps_counter_id = pygame.USEREVENT + 4
        pygame.time.set_timer(
            self.fps_counter_id,
            1000 # This is static, does not need to be modified
        )
        
        # Logging entry point
        self.main.debug.new_line()
        self.main.debug.log("Initialized scene")
        
        # Sprites and sprite groups
        self.general_sprites = SpriteGroup()
        self.ui_components = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Scene components
        self.background = SceneBackground(
            self.main.screen, 
            self.time, 
            **self.main.data.background
        )
        
        # Internal variables
        self.available_businesses = 0 # this will be used in limiting customer conversion rate
        self.business_data = {}
        self.business_menu = BusinessMenu(self.main, self.time, self.location)
        # Safe spot is somewhere in the middle so that the customers will
        #   go there first before going to the back layer of businesses
        #   to avoid rendering confusions or going through walls
        # This is location-specific
        self.safe_spot = self.main.data.location[self.location]["safe_spot"]
        self.object_limit = self.main.data.location[self.location]["object_limit"]
        
        for business_name in self.main.data.location[self.location]["businesses"]:
            if business_name == "street_food":
                business_name = self.main.data.progress["businesses"][self.location]["street_food"]["type"]
                data = "street_food"
            else:
                data = business_name
                
            scene_business = Business(
                self, business_name,
                self.business_callback,
                self.main.data.business[data],
                midbottom_coordinates=(
                    int(self.main.data.setting["game_width"] * self.main.data.business[data]["rel_midbottom_coordinates"][0]),
                    int(self.main.data.setting["game_height"] * self.main.data.business[data]["rel_midbottom_coordinates"][1])
                ), 
                collide_rect=self.main.data.business[data]["collide_rect"],
                **self.main.data.business_images[business_name]
            )
            self.business_data[business_name] = {}
            self.business_data[business_name]["meta"] = self.main.data.business[data]
            self.business_data[business_name]["object"] = scene_business
            scene_business.add(self.general_sprites)
        
        self.profile_holder = Button(
            self.main,
            self.profile_callback,
            top_left_coordinates=(10, 10),
            **{
                "idle" : self.main.data.scene["profile_holder_idle"],
                "outline" : self.main.data.scene["profile_holder_outline"]
            }
        )
        self.profile_holder.add(self.ui_components)
        
        self.profile_message = Message(
            self.main.screen, 
                [
                    self.time.get_date(), 
                    self.time.get_time(),
                    "Bank Balance:",
                    f"P{self.main.data.progress['cash']:18,.2f}"
                ], 
            self.main.data.small_font, 
            self.main.data.colors["orange"],
            top_left_coordinates=(165, 75)
        )
        self.profile_message.add(self.ui_components)
        
        self.debug_message = Message(
            self.main.screen,
            [""],
            self.main.data.small_font, 
            self.main.data.colors["white"],
            top_left_coordinates=(10, 545), # 545, 420 for ernest
            outline_thickness=1
        )
        
        # Buttons layering hierarchy (the top layer must be add first)
        self.profile_holder.add(self.buttons)
        self.main.sliding_menu.sliding_menu_button.add(self.buttons)
        # Loop out the businesses then add them after this line to make the buttons
        #   discovered first before the layer of businesses
        for key, business in self.business_data.items():
            business["object"].add(self.buttons)
            
        self.debug_message.add(self.ui_components)
        
        
    def reconstruct(self, main):
        # Logging entry point
        self.main.debug.new_line()
        self.main.debug.log("Reconstructing scene")
        
        self.main = main
        self.location = self.main.data.progress["last_location"]
        self.crowd_chance = self.main.data.crowd_statistics[self.location]
        self.customer_chance = self.main.data.customer_statistics[self.location]
        
        self.time.reconstruct(
            self.main.debug,
            self.main.data.progress["time"],
            self.main.data.setting["fps"],
            self.main.data.meta["time_amplify"],
            **self.callbacks
        )
        
        self.background.reconstruct(
            self.main.screen, 
            self.time, 
            **self.main.data.background
        )
        
        self.available_businesses = 0
        # self.business_data = {}
        self.business_menu.reconstruct(
            self.main, 
            self.time, 
            self.location
        )
        
        self.safe_spot = self.main.data.location[self.location]["safe_spot"]
        self.object_limit = self.main.data.location[self.location]["object_limit"]
        
        # if the new length is longer than the current length: 4 > 2 : 3
        #   use the new length as traversal index
        #       replace the current businesses with new ones
        #       add new index objects to fill the rest
        
        # if the new length is shorter than the current length: 2 < 4 : 1
        #   use the old length as traversal index
        #       take note of the new_business_index_limit: 1
        #       replace the current businesses with new ones until
        #           the new_business_index_limit is reached
        #       if it has been reached, disabled the succeeding businesses : 2, 3
        
        # if both lengths are equal: 4 = 4: 3
        #   use any length, doesn't matter 
        #       replace all businesses with new ones
        
        # To combine all these conditions
        #   use the longer index
        #       if the traversal index <= new_business_index_limit
        #           if the object is disabled, re-enable it first
        #           replace the current business with the new one
        #           if traversal_index > current_businesses_index_limit
        #               add new index to the business data and insert business
        #       if the traversal index > new_business_index_limit
        #           if traversal index <= current_businesses_index_limit
        #               disable the current business

        current_businesses_length = len(self.business_data)
        current_businesses_index_limit = current_businesses_length - 1
        current_business_keys = list(self.business_data.keys())
        
        new_businesses_length = len(self.main.data.location[self.location]["businesses"])
        new_business_index_limit = new_businesses_length - 1 # remember index starts at 0
        
        for traversal_index in range(max(current_businesses_length, new_businesses_length)):
            if traversal_index <= new_business_index_limit:
                # replace the current business with the new one
                business_name = self.main.data.location[self.location]["businesses"][traversal_index]
                if business_name == "street_food":
                    business_name = self.main.data.progress["businesses"][self.location]["street_food"]["type"]
                    data = "street_food"
                else:
                    data = business_name
                    
                if traversal_index > current_businesses_index_limit:
                    scene_business = Business(
                        self, business_name,
                        self.business_callback,
                        self.main.data.business[data],
                        midbottom_coordinates=(
                            int(self.main.data.setting["game_width"] * self.main.data.business[data]["rel_midbottom_coordinates"][0]),
                            int(self.main.data.setting["game_height"] * self.main.data.business[data]["rel_midbottom_coordinates"][1])
                        ), 
                        collide_rect=self.main.data.business[data]["collide_rect"],
                        **self.main.data.business_images[business_name]
                    )
                    self.business_data[business_name] = {}
                    self.business_data[business_name]["meta"] = self.main.data.business[data]
                    self.business_data[business_name]["object"] = scene_business
                    scene_business.add(self.general_sprites)
                else:
                    # transfer old key details to new key
                    if business_name not in current_business_keys:
                        self.business_data[business_name] = \
                            self.business_data.pop(
                                self.business_data[current_business_keys[traversal_index]])
                        
                    self.business_data[business_name]["meta"] = self.main.data.business[data]
                    self.business_data[business_name]["object"].reconstruct(
                        self, business_name,
                        self.business_callback,
                        self.main.data.business[data],
                        midbottom_coordinates=(
                            int(self.main.data.setting["game_width"] * self.main.data.business[data]["rel_midbottom_coordinates"][0]),
                            int(self.main.data.setting["game_height"] * self.main.data.business[data]["rel_midbottom_coordinates"][1])
                        ), 
                        collide_rect=self.main.data.business[data]["collide_rect"],
                        **self.main.data.business_images[business_name]
                    )
                    self.business_data[business_name]["object"].visible = True
            elif traversal_index > new_business_index_limit:
                # disable the current business
                # if traversal index <= current_businesses_index_limit
                #       disable the current business
                if traversal_index <= current_businesses_index_limit:
                    self.business_data[current_business_keys[traversal_index]]["object"].visible = False
            
        # Refreshing order of buttons after a possible new businesses appreared
        #   in the business_data dictionary object
        for button in self.buttons:
            button.remove(self.buttons)
        self.profile_holder.add(self.buttons)
        self.main.sliding_menu.sliding_menu_button.add(self.buttons)
        for key, business in self.business_data.items():
            business["object"].add(self.buttons)
        
        
    
    def time_callback_seconds(self, time_amplification):
        pass
        
    
    def time_callback_minute(self):
        self.profile_message.set_message([
            self.time.get_date(), 
            self.time.get_time(),
            "Bank Balance:",
            f"P{self.main.data.progress['cash']:18,.2f}"
        ])
        
    
    def time_callback_hour(self):
        self.main.debug.log("Hour callback")
        self.background.set_time(self.time)
        self.background.check_change()
        
    
    def time_callback_day(self):
        self.main.debug.log("Day callback")
        
        # TODO Update reports of each individual owned businesses
        
    
    def time_callback_month(self):
        self.main.debug.log("Month callback")
        
    
    def time_callback_year(self):
        self.main.debug.log("Year callback")
    
    
    def profile_callback(self, *args):
        print("Profile clicked")
        
    
    def business_callback(self, *args):
        self.business_menu.set_data(args[0])
        self.business_menu.enable = True
            
            
    def check_queues_if_full(self):
        self.available_businesses = 0
        for name, data in self.business_data.items():
            if len(data["object"].queue) < data["object"].queue_limit \
                and data["object"].business_state == "open":
                    self.available_businesses += 1
        
        if self.available_businesses == 0:
            return True
        return False
            
            
    def spawn_crowd_customer(self):
        npc_chance = random.randint(0, 100)
        if npc_chance <= self.crowd_chance[self.time.time.hour] \
                and len(self.general_sprites) < self.object_limit: 
            self.footprint_counter += 1 # TODO Deprecated
            npc_form = str(random.randint(0, len(self.main.data.crowd_spritesheets) - 2))
            is_businesses_full = self.check_queues_if_full()
            
            customer_chance = random.randint(0, 100)
            weighted_customer_chance = \
                self.customer_chance[self.time.time.hour] * \
                (self.available_businesses / len(self.business_data))
            if customer_chance <= int(weighted_customer_chance) and not is_businesses_full:
                self.customers_spawned += 1 # TODO For debugging only
                Customer(
                    self.main.screen, npc_form,
                    self.main.data.crowd_spritesheets[npc_form]["sheet"],
                    self.main.data.crowd_spritesheets[npc_form]["data"],
                    self.main.data.emojis,
                    self.main.data.setting["fps"],
                    self.safe_spot, **self.business_data
                ).add(self.general_sprites)
            else:
                NPC(
                    self.main.screen, npc_form, 
                    self.main.data.crowd_spritesheets[npc_form]["sheet"],
                    self.main.data.crowd_spritesheets[npc_form]["data"],
                    self.main.data.setting["fps"]
                ).add(self.general_sprites)
                
                                
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
            self.show_debug_info = not self.show_debug_info
            if self.show_debug_info:
                self.debug_message.add(self.ui_components)
                self.main.debug.log("Debug details shown")
            else:
                self.debug_message.kill()
                self.main.debug.log("Debug details hidden")
            
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
        self.main.debug.memory_log()
        self.main.debug.new_line()
        
        # Check if the sliding button is in the scene yet
        if self.buttons not in self.main.sliding_menu.sliding_menu_button.groups():
            self.main.sliding_menu.sliding_menu_button.add(self.buttons)
        
        self.running = True
        while self.running:
            # Rendering sprites
            self.background.update()
            self.general_sprites.draw(self.main.screen)
            self.ui_components.update()
            self.main.sliding_menu.update()
            
            # Menu overlays
            self.business_menu.update()
            
            # Event processing
            for event in pygame.event.get():
                if self.business_menu.enable:
                    self.business_menu.handle_event(event)
                elif not self.main.sliding_menu.is_tucked:
                    self.main.sliding_menu.handle_event(event)
                else:
                    if event.type == pygame.QUIT: 
                        self.running = False
                        self.close_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN: 
                        self.mouse_click_events(event)
                    elif event.type == pygame.MOUSEMOTION: 
                        self.mouse_drag_events(event)
                    elif event.type == pygame.KEYDOWN:
                        self.key_down_events(event.key)
                
                    # Key pressing events (holding keys applicable)
                    keys = pygame.key.get_pressed()
                    self.key_hold_events(keys)
                
                # Custom event timers
                if event.type == self.autosave_id:
                    self.update_data()
                    self.main.debug.log("Autosaved progress")
                elif event.type == self.crowd_spawner_id:
                    self.spawn_crowd_customer()
                elif event.type == self.memory_debug_id:
                    self.main.debug.log(f"[A] Objects in memory: {len(self.general_sprites)}")
                    self.main.debug.memory_log()
                elif event.type == self.fps_counter_id:
                    self.fps_previous_count = self.fps_counter
                    self.fps_counter = 0
                    
                    current_fps = self.main.data.setting["fps"]
                    if self.fps_previous_count <= int(current_fps * 0.5):
                        self.main.debug.log(f"CRITICAL: FPS Plummeted {self.fps_previous_count}/{current_fps}")
                        self.main.debug.memory_log()
                    elif self.fps_previous_count <= int(current_fps * 0.75):
                        self.main.debug.log(f"WARNING: FPS Dropped {self.fps_previous_count}/{current_fps}")
                        self.main.debug.memory_log()
                    elif self.fps_previous_count <= int(current_fps * 0.9):
                        self.main.debug.log(f"NOTICE: FPS Unstabled {self.fps_previous_count}/{current_fps}")
                        self.main.debug.memory_log()
            
            # FPS Counter increment
            self.fps_counter += 1
            
            # TODO DEBUGGING ONLY/ considering to turning into feature
            if self.show_debug_info:
                self.debug_message.set_message(
                    [
                        f"FPS: {self.fps_previous_count}/{self.main.data.setting['fps']}",
                        f"{self.main.debug.get_highest_usage()}",
                        f"{self.main.debug.get_memory_usage()}",
                        f"{self.main.debug.get_free_usage()}",
                        f"Location: {self.location}",
                        f"Total crowd spawned: {self.footprint_counter}",
                        f"Customers spawned: {self.customers_spawned}",
                        f"Objects/Max displayed: {len(self.general_sprites)}/{self.object_limit}"
                        # f"Tindahan: {len(self.business_data['sari_sari_store']['object'].queue)}/{self.business_data['sari_sari_store']['object'].queue_limit} Served customers: {self.business_data['sari_sari_store']['object'].served_count} Sales: P{self.main.data.progress['businesses'][self.location]['sari_sari_store']['sales']:,.2f}",
                        # f"Food cart: {len(self.business_data['food_cart']['object'].queue)}/{self.business_data['food_cart']['object'].queue_limit} Served customers: {self.business_data['food_cart']['object'].served_count} Sales: P{self.main.data.progress['businesses'][self.location]['food_cart']['sales']:,.2f}",
                        # f"Buko stall: {len(self.business_data['buko_stall']['object'].queue)}/{self.business_data['buko_stall']['object'].queue_limit} Served customers: {self.business_data['buko_stall']['object'].served_count} Sales: P{self.main.data.progress['businesses'][self.location]['street_food']['sales']:,.2f}",
                        # f"Ukay-ukay: {len(self.business_data['ukay_ukay']['object'].queue)}/{self.business_data['ukay_ukay']['object'].queue_limit} Served customers: {self.business_data['ukay_ukay']['object'].served_count} Sales: P{self.main.data.progress['businesses'][self.location]['ukay_ukay']['sales']:,.2f}",
                    ]
                )
            
            # Updating the display
            self.refresh_display()
        
    