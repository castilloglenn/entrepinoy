from game.npc import NPC
import pygame
import random
import copy


class Customer(NPC):
    """
    This class handles the behaviors of a customer in the game.
    """
    def __init__(self, screen: 
                pygame.Surface, name: str, 
                spritesheet: pygame.Surface, 
                meta_data: dict, fps: int, 
                safe_spot: tuple[float],
                **businesses):
        super().__init__(screen, name, spritesheet, meta_data, fps)
        
        keys = list(businesses.keys())
        self.business_target = businesses[random.choice(keys)]
        self.safe_spot = safe_spot
        
        # Generating points for the customer to traverse across the scene
        self.target_points = []
        self.target_index = 0
        self.business_queue_space = 20
        
        # 2D Movement variables
        self.target_slope = ()
        self.previous_position_in_float = []
        self.current_position_in_float = [
            float(self.rect.midbottom[0]), 
            float(self.rect.midbottom[1]),
        ]
        
        # Initial stopping point
        self.target_points.append((
            random.randint(
                self.rect.width,
                self.screen.get_width()
            ), self.rect.midbottom[1])
        )
        
        # Checking if the target is behind or front
        if self.business_target["meta"]["placement"] == "back":
            self.target_points.append((
                int(self.screen.get_width() * self.safe_spot[0]),
                int(self.screen.get_height() * self.safe_spot[1])
            ))
            
        # Adding the queuing point of the business
        self.target_points.append((
            self.business_target["object"].rect.x +
                int(self.business_target["object"].rect.width *
                    self.business_target["meta"]["queuing_point"]),
            self.business_target["object"].rect.y +
            self.business_target["object"].rect.height +
            self.business_queue_space
        ))
        
        self.target_slope = self.get_slope(self.current_position_in_float, self.target_points[self.target_index])
        
        
    def get_slope(self, current_position, target_position):
        x = abs(target_position[0] - current_position[0])
        y = abs(target_position[1] - current_position[1])
        
        if y > x:
            sx = x / y
            sy = y / y
        else:
            sx = x / x
            sy = y / x
        
        if current_position[0] > target_position[0]:
            sx = -sx
        if current_position[1] > target_position[1]:
            sy = -sy
        
        return (sx, sy)
    
    
    def update(self):          
        super().animate()
        if self.standing:
            return
        
        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            try:
                if self.rect.midbottom == self.target_points[self.target_index]:
                    self.target_index += 1
                    
                self.target_slope = self.get_slope(self.current_position_in_float, self.target_points[self.target_index])
            except IndexError:
                self.standing = True
            self.previous_position_in_float = copy.deepcopy(self.current_position_in_float)
            
            self.current_position_in_float[0] += self.target_slope[0]
            self.current_position_in_float[1] += self.target_slope[1]
            
            if int(self.previous_position_in_float[0]) != int(self.current_position_in_float[0]) or \
                int(self.previous_position_in_float[1]) != int(self.current_position_in_float[1]):
                    difference = (
                        round(self.current_position_in_float[0]) - round(self.previous_position_in_float[0]),
                        round(self.current_position_in_float[1]) - round(self.previous_position_in_float[1])
                    )
                    
                    if difference[0] > 0:
                        self.direction = "right"
                        self.is_flipped = True
                    elif difference[0] < 0:
                        self.direction = "left"
                        self.is_flipped = False
                    
                    current_midbottom = list(self.rect.midbottom)
                    current_midbottom[0] += difference[0]
                    current_midbottom[1] += difference[1]
                    
                    self.rect.midbottom = tuple(current_midbottom)
            
        
        
        
        