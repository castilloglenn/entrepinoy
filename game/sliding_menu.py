from game.sprite.button import Button
import pygame


class SlidingMenu():
    # TODO THIS WHOLE CLASS
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
        
        self.update_endpoint()
        
        self.sliding_menu_button = Button(
            self.main, self.switch_state,
            top_left_coordinates=(
                self.sliding_menu_rect.x,
                self.sliding_menu_rect.y + self.trigger_button_y
            ),
            **{
                "idle" : self.main.data.meta_images["sliding_menu_button_idle"],
                "hovered" : self.main.data.meta_images["sliding_menu_button_hovered"]
            }
        )
        self.sliding_menu_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        # MENU ICON BUTTONS
        self.map_button = Button(
            self.main, self.trigger_map,
            top_left_coordinates=(
                self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
                self.sliding_menu_rect.y + (self.sliding_menu_rect.width * 0.074)
            ),
            **{
                "idle" : self.main.data.meta_images["map_button_idle"],
                "outline" : self.main.data.meta_images["map_button_outline"],
                "disabled" : self.main.data.meta_images["map_button_disabled"],
                "tooltip" : ["Go to map"]
            }
        )
        self.map_button.add(self.objects, self.hoverable_buttons, self.buttons)
        
        
    def trigger_map(self, *args):
        print("Map button clicked")
        
        
    def update_endpoint(self):
        if self.is_tucked:
            self.sliding_menu_rect.x = self.hidden_endpoint
        elif not self.is_tucked:
            self.sliding_menu_rect.x = self.visible_endpoint
            
    
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
        
        
        
        
        