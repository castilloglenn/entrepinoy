from game.sprite.button import Button
import pygame


class SlidingMenu():
    """
    This class displays a confirmation menu when certain actions have been taken.
    """
    def __init__(self, main):
        self.enable = True
        self.is_tucked = True
        self.is_moving = False
        
        self.main = main
        self.callback = None
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Screen objects
        self.frame_length = 1 / self.main.data.setting["fps"]
        self.dim_max_intensity = 128        # 0-255 color opacity
        self.dim_intensity = 0              # initial state
        self.trigger_button_width = 44     
        self.trigger_button_y = 128        
        self.travel_speed_per_second = 900  
        self.travel_speed_per_frame = \
             self.travel_speed_per_second * self.frame_length
        
        self.sliding_menu_image = self.main.data.meta_images["sliding_menu"].convert_alpha()
        self.sliding_menu_rect = self.sliding_menu_image.get_rect()
        self.sliding_menu_rect.y = \
            int((self.main.screen.get_rect().height - self.sliding_menu_rect.height) / 2)
        
        self.hidden_endpoint = self.main.screen.get_rect().width - self.trigger_button_width
        self.visible_endpoint = self.main.screen.get_rect().width - self.sliding_menu_rect.width
        
        self.travel_steps_count = (self.hidden_endpoint - self.visible_endpoint) / self.travel_speed_per_frame
        self.dim_speed_per_frame = self.dim_max_intensity / self.travel_steps_count
        
        self.sliding_menu_button = Button(
            self.main, self.switch_state,
            **{
                "idle" : self.main.data.meta_images["sliding_menu_button_idle"],
                "hovered" : self.main.data.meta_images["sliding_menu_button_hovered"]
            }
        )
        
        # MENU ICON BUTTONS
        self.map_button = Button(
            self.main, self.map_callback,
            **{
                "idle" : self.main.data.meta_images["map_button_idle"],
                "outline" : self.main.data.meta_images["map_button_outline"],
                "disabled" : self.main.data.meta_images["map_button_disabled"],
                "tooltip" : ["City Map"]
            }
        )
        self.mission_button = Button(
            self.main, self.mission_callback,
            **{
                "idle" : self.main.data.meta_images["mission_button_idle"],
                "outline" : self.main.data.meta_images["mission_button_outline"],
                "disabled" : self.main.data.meta_images["mission_button_disabled"],
                "tooltip" : ["Missions"]
            }
        )
        self.event_button = Button(
            self.main, self.event_callback,
            **{
                "idle" : self.main.data.meta_images["events_button_idle"],
                "outline" : self.main.data.meta_images["events_button_outline"],
                "disabled" : self.main.data.meta_images["events_button_disabled"],
                "tooltip" : ["Events"]
            }
        )
        
        self.bank_button = Button(
            self.main, self.bank_callback,
            **{
                "idle" : self.main.data.meta_images["bank_button_idle"],
                "outline" : self.main.data.meta_images["bank_button_outline"],
                "disabled" : self.main.data.meta_images["bank_button_disabled"],
                "tooltip" : ["Bank"]
            }
        )
        self.part_time_button = Button(
            self.main, self.part_time_callback,
            **{
                "idle" : self.main.data.meta_images["part_time_idle"],
                "outline" : self.main.data.meta_images["part_time_outline"],
                "disabled" : self.main.data.meta_images["map_button_disabled"],
                "tooltip" : ["Part Time"]
            }
        )
        self.my_room_button = Button(
            self.main, self.my_room_callback,
            **{
                "idle" : self.main.data.meta_images["home_button_idle"],
                "outline" : self.main.data.meta_images["home_button_outline"],
                "disabled" : self.main.data.meta_images["home_button_disabled"],
                "tooltip" : ["My Room"]
            }
        )
        
        self.news_button = Button(
            self.main, self.news_callback,
            **{
                "idle" : self.main.data.meta_images["news_button_idle"],
                "outline" : self.main.data.meta_images["news_button_outline"],
                "disabled" : self.main.data.meta_images["news_button_disabled"],
                "tooltip" : ["News"]
            }
        )
        self.crypto_button = Button(
            self.main, self.crypto_callback,
            **{
                "idle" : self.main.data.meta_images["crypto_button_idle"],
                "outline" : self.main.data.meta_images["crypto_button_outline"],
                "disabled" : self.main.data.meta_images["crypto_button_disabled"],
                "tooltip" : [
                    "Crypto",
                    "Market"
                ]
            }
        )
        self.stock_button = Button(
            self.main, self.stock_callback,
            **{
                "idle" : self.main.data.meta_images["stock_button_idle"],
                "outline" : self.main.data.meta_images["stock_button_outline"],
                "disabled" : self.main.data.meta_images["stock_button_disabled"],
                "tooltip" : [
                    "Stock", 
                    "Market"
                ]
            }
        )
        
        self.achievement_button = Button(
            self.main, self.achievement_callback,
            **{
                "idle" : self.main.data.meta_images["achievement_button_idle"],
                "outline" : self.main.data.meta_images["achievement_button_outline"],
                "disabled" : self.main.data.meta_images["achievement_button_disabled"],
                "tooltip" : ["Achievements"]
            }
        )
        self.setting_button = Button(
            self.main, self.setting_callback,
            **{
                "idle" : self.main.data.meta_images["setting_button_idle"],
                "outline" : self.main.data.meta_images["setting_button_outline"],
                "disabled" : self.main.data.meta_images["setting_button_disabled"],
                "tooltip" : ["Setting"]
            }
        )
        self.main_menu_button = Button(
            self.main, self.main_menu_callback,
            **{
                "idle" : self.main.data.meta_images["main_menu_button_idle"],
                "outline" : self.main.data.meta_images["main_menu_button_outline"],
                "disabled" : self.main.data.meta_images["map_button_disabled"],
                "tooltip" : [
                    "Return to", 
                    "main menu"
                ]
            }
        )
        
        # TODO This measures attribute is for reference only
        self.measures = {
            "x_base" : 0.1730,
            "y_base" : 0.0625,
            "x_gap" : 0.2695,
            "y_gap" : 0.2300
        }
        
        self.update_endpoint()
        
        
    def map_callback(self, *args):
        location = self.main.data.progress["last_location"]
        if location == "location_a":
            self.main.data.progress["last_location"] = "test_location"
        elif location == "test_location":
            self.main.data.progress["last_location"] = "location_a"
        
        self.tuck()
        self.main.scene_window.update_data()
        self.main.scene_window.reconstruct(self.main)
        
        
    def mission_callback(self, *args):
        print("Mission button clicked")
        
        
    def event_callback(self, *args):
        print("Event button clicked")
        
        
    def bank_callback(self, *args):
        print("Bank button clicked")
        
        
    def part_time_callback(self, *args):
        print("Part Time button clicked")
        
        
    def my_room_callback(self, *args):
        print("Residence button clicked")
        
        
    def news_callback(self, *args):
        print("News button clicked")
        
        
    def crypto_callback(self, *args):
        print("Crypto button clicked")
        
        
    def stock_callback(self, *args):
        print("Stocks button clicked")
        
        
    def achievement_callback(self, *args):
        print("Achievements button clicked")
        
        
    def setting_callback(self, *args):
        self.main.setting_window.run()
        
        
    def main_menu_callback(self, *args):
        self.tuck()
        self.main.scene_window.update_data()
        self.main.scene_window.running = False
        self.main.debug.log("Autosaved progress before going to main menu")  
        self.main.debug.log("Exited scene via Sliding Menu")
        
    
    def tuck(self):
        if not self.is_tucked:
            self.is_moving = False
            self.is_tucked = True
            self.dim_intensity = 0
            self.update_endpoint()
            
            for button in self.buttons:
                button.x_coordinate_offset = 0
                button.set_image_and_rect()
        
        
    def update_endpoint(self):
        if self.is_tucked:
            self.sliding_menu_rect.x = self.hidden_endpoint
        elif not self.is_tucked:
            self.sliding_menu_rect.x = self.visible_endpoint
        
        self.sliding_menu_button.top_left_coordinates = (
            self.sliding_menu_rect.x,
            self.sliding_menu_rect.y + self.trigger_button_y
        )
        self.map_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625)
        )
        self.mission_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625)
        )
        self.event_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625)
        )
        self.bank_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925)
        )
        self.part_time_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925)
        )
        self.my_room_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925)
        )
        self.news_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524)
        )
        self.crypto_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524)
        )
        self.stock_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524)
        )
        self.achievement_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.754)
        )
        self.setting_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.754)
        )
        self.main_menu_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.754)
        )
        
        # Clearing the sprite groups before adding the objects back to it
        for obj in self.objects:
            obj.kill()
            del obj
        self.objects.empty()
        
        self.sliding_menu_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        self.map_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.mission_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.event_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        self.bank_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.part_time_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.my_room_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        self.news_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.crypto_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.stock_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        self.achievement_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.setting_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.main_menu_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        for button in self.buttons:
            button.set_image_and_rect()
            
    
    def switch_state(self, *args):
        self.is_moving = True
        
        
    def handle_event(self, event):
        if not self.enable:
            self.close()
            return
    
        if event.type == pygame.QUIT: 
            # Closing the game properly
            self.main.close_game()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.switch_state()
                
        elif event.type == pygame.MOUSEMOTION: 
            for button in self.hoverable_buttons:
                button.check_hovered(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                
                if not self.sliding_menu_rect.collidepoint(mouse_pos) and not self.is_tucked:
                    self.switch_state()
                
                for button in self.buttons:
                    button.check_clicked(mouse_pos)
        
        
    def update(self):
        if not self.enable:
            return
        
        # Screen dimming
        self.main.display_surface.set_alpha(self.dim_intensity)
        self.main.screen.blit(self.main.display_surface, (0, 0))
        
        if self.is_moving:
            if self.is_tucked:
                # then the section is moving left to show, increase dim
                coordinate_change = \
                    self.sliding_menu_rect.x - \
                    max(
                        self.sliding_menu_rect.x - self.travel_speed_per_frame,
                        self.visible_endpoint
                    )
                
                self.sliding_menu_rect.x -= int(coordinate_change)
                for obj in self.objects:
                    obj.x_coordinate_offset -= int(coordinate_change)
                    obj.set_image_and_rect()
                    
                self.dim_intensity = min(
                    self.dim_intensity + self.dim_speed_per_frame, 
                    self.dim_max_intensity)
                
                if self.sliding_menu_rect.x <= self.visible_endpoint:
                    self.is_moving = False
                    self.is_tucked = False
            else: # the body is shown
                # then the section is moving right to hide itself, decrease dim
                coordinate_change = \
                    min(
                        self.sliding_menu_rect.x + self.travel_speed_per_frame,
                        self.hidden_endpoint
                    ) - self.sliding_menu_rect.x
                
                self.sliding_menu_rect.x += int(coordinate_change)
                for obj in self.objects:
                    obj.x_coordinate_offset += int(coordinate_change)
                    obj.set_image_and_rect()
                
                self.dim_intensity = max(
                    self.dim_intensity - self.dim_speed_per_frame, 0)
                
                if self.sliding_menu_rect.x >= self.hidden_endpoint:
                    self.is_moving = False
                    self.is_tucked = True
        
        self.main.screen.blit(self.sliding_menu_image, self.sliding_menu_rect)
        self.objects.update()
        
        for button in self.buttons:
            button.display_tooltips()
        
    
    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()
        
        
    def close(self):
        self.clear()
        self.enable = False
        
        
        
        
        