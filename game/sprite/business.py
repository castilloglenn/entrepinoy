from game.sprite.button import Button
import pygame
import copy

from pprint import pprint


class Business(Button):
    """
    This class handles the business interface in the scene.
    It controls its attributes and the states when it is open or closed.
    """
    def __init__(self, screen, name, fps,
                 callback_function, serve_button,
                 business_data,
                 top_left_coordinates=None, 
                 center_coordinates=None, 
                 collide_rect=None,
                 **states):
        super().__init__(screen,
            callback_function, 
            top_left_coordinates=top_left_coordinates, 
            center_coordinates=center_coordinates,
            collide_rect=collide_rect,
            **states)
        
        self.name = name
        self.states = states
        self.outline = self.states["outline"].convert_alpha()
        
        # Business attributes
        self.business_data = business_data
        self.served_count = 0
        self.sales_stash = 0
        
        self.employee_spritesheet = self.states["employee"]["spritesheet"]
        self.employee_json = self.states["employee"]["json"]
        self.serve_button_relative_location = (0.5, 0.5)
        
        self.employee_frames = []
        self.employee_index = 0

        self.fps = fps
        self.frame_length = 1 / self.fps
        self.frame_counter = 0
        
        self.seconds_counter = 0
        self.serving_cooldown = 1
        
        # This speed controls when to switch from sprite animation to the
        #   next animation in the spritesheet
        self.animate_speed = self.fps * 0.12
        self.animation_tick = 0
        
        # Parsing all the sprites contained in the spritesheet
        for frame_name, content in self.employee_json['frames'].items():
            self.name_keyword = frame_name.replace("_employee_1.png", "")
            break
            
        for index in range(len(self.employee_json['frames'])):
            self.employee_frames.append(self.fetch_sprite(f'{self.name_keyword}_employee_{index + 1}.png'))
            
        # Setting the standing animation for the sprite
        self.standby_image = self.employee_frames.pop()
        self.business_state = "open"
        self.has_employee = False
        self.is_standby = True
        self.is_serving = False
        
        self.queue = []
        self.queue_limit = 5
        
        super().update()
        
        # Setting up pop-up buttons
        self.serve_button = serve_button
        self.serve_button.set_callback(self.serve_customer)
    
    
    def update(self):
        if self.has_employee and not self.is_standby and self.is_serving:
            self.animation_tick += 1
            if self.animation_tick >= self.animate_speed:
                self.animation_tick = 0
                self.employee_index = (self.employee_index + 1) % len(self.employee_frames)
                
                self.idle = self.employee_frames[self.employee_index]
                self.hovered = self.employee_frames[self.employee_index].copy()
                self.hovered.blit(self.outline, (0, 0))
                
                if self.employee_index == len(self.employee_frames) - 1:
                    self.is_serving = False
                    self.is_standby = True
                    
                    self.update_business_images()
                    self.serve_customer()
                    
        elif self.has_employee and self.is_standby and not self.is_serving \
            and len(self.queue) > 0:
                if self.queue[0].is_standing:
                    self.frame_counter += self.frame_length
                    if int(self.frame_counter) >= 1:
                        self.frame_counter -= 1
                        self.seconds_counter += 1
                        
                        # Automatic serving when employees is present
                        if self.seconds_counter >= self.serving_cooldown:
                            self.seconds_counter = 0
                            self.set_serve_animation()
                    
        else:
            self.update_business_images()
          
        self.set_image_and_rect()
        super().update()
        
        # Checks for the manual serving button
        if len(self.queue) > 0 and not self.has_employee:
            if self.queue[0].is_standing:
                # self.business_data["rel_serve_coordinates"]
                if self.business_data["placement"] == "front":
                    new_center = (
                        self.rect.center[0],
                        self.screen.get_rect().height * 0.43
                    )
                elif self.business_data["placement"] == "back":
                    new_center = (
                        self.rect.center[0],
                        self.screen.get_rect().height * 0.3
                    )
                
                self.serve_button.rect.center = new_center
                self.serve_button.visible = True
            else:
                self.serve_button.visible = False
        else:
            self.serve_button.visible = False
        
        self.serve_button.update()
        
        
    def set_serve_animation(self):
        # Trigger one full sprite animation then trigger serve command
        #   and makes the first customer leave
        if len(self.queue) > 0 and self.has_employee and self.queue[0].is_standing:
            self.is_standby = False
            self.is_serving = True
        
        
    def set_business_state(self, new_state: str):
        # Open or close
        self.business_state = new_state
        self.update_business_images()
        self.set_image_and_rect()
    
    
    def check_hovered(self, hover_coordinates):
        if self.serve_button.check_hovered(hover_coordinates) \
            and self.serve_button.visible:
                self.state = "idle"
                self.set_image_and_rect()
                return True
        else:
            self.state = "hovered"
            self.set_image_and_rect()
            return super().check_hovered(hover_coordinates)
        
    
    def check_clicked(self, click_coordinates):
        if self.serve_button.check_clicked(click_coordinates) \
            and self.serve_button.visible:
                return True
        else:
            return super().check_clicked(click_coordinates)
        
        
    def update_business_images(self):
        if self.business_state == "open":
            if self.has_employee and self.is_standby:
                self.idle = self.standby_image.convert_alpha()
                self.hovered = self.standby_image.convert_alpha()
            else:
                self.idle = self.states["idle"].convert_alpha()
                self.hovered = self.states["idle"].convert_alpha()
            
        elif self.business_state == "closed":
            self.is_standby = True
            
            self.clear_queue()
            self.idle = self.states["closed"].convert_alpha()
            self.hovered = self.states["closed"].convert_alpha()
            
        self.hovered.blit(self.outline, (0, 0))
        
    
    def serve_customer(self, *args):
        if len(self.queue) == 0:
            return
        
        if self.queue[0].is_standing:
            self.served_count += 1
            self.queue.pop(0).leave()
            for customer in self.queue:
                customer.queue_move(-1)
                
    
    def clear_queue(self):
        # Free the queue
        for customer in self.queue:
            customer.leave()
        self.queue = []
            
            
    def fetch_sprite(self, name):
        sprite = self.employee_json['frames'][name]['frame']
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        image.blit(self.employee_spritesheet,(0, 0),(x, y, width, height))
        self.rect = image.get_rect()
        return image.convert_alpha()
    
    
    # TODO Debug only
    def switch_animation(self, hover_coordinates):
        if self.collide_rect.collidepoint(hover_coordinates) and not self.is_serving:
            self.has_employee = not self.has_employee
            self.update_business_images()
            self.set_image_and_rect()
