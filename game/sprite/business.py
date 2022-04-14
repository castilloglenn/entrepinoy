from game.sprite.button import Button
import pygame


class Business(Button):
    """
    This class handles the business interface in the scene.
    It controls its attributes and the states when it is open or closed.
    """
    def __init__(self, screen, name, 
                 callback_function, 
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
        self.business_state = "open"
        self.has_employee = False
        self.queue = []
        self.queue_limit = 5
        
        
    def set_business_state(self, new_state: str):
        self.business_state = new_state
        
        if self.business_state == "open":
            self.idle = self.states["idle"].convert_alpha()
            self.hovered = self.states["idle"].convert_alpha()
            
        elif self.business_state == "closed":
            # Free the queue
            self.queue = []
            
            self.idle = self.states["closed"].convert_alpha()
            self.hovered = self.states["closed"].convert_alpha()
        
        self.hovered.blit(self.outline, (0, 0))
        self.set_image_and_rect()
        
    
    def set_employee_state(self, new_state: bool):
        self.has_employee = new_state
        
    
    def serve_customer(self):
        if len(self.queue) == 0:
            return
        
        if self.queue[0].is_standing:
            self.queue.pop(0).served_and_leave()
            for customer in self.queue:
                customer.queue_move(-1)
            
            
    def fetch_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        image.blit(self.sprite_sheet,(0, 0),(x, y, width, height))
        self.rect = image.get_rect()
        return image.convert_alpha()
            
