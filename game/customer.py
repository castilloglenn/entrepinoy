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
        # Randomly selecting businesses
        while True:
            self.business_target = businesses[random.choice(keys)]
            if len(self.business_target["object"].queue) < self.business_target["object"].queue_limit:
                self.queue_number = len(self.business_target["object"].queue)
                self.business_target["object"].queue.append(self)
                break
        
        # Customer attributes
        self.is_served = False
        self.is_exiting = False
        self.safe_spot = safe_spot
        
        # Generating points for the customer to traverse across the scene
        self.target_points = []
        self.target_index = 0
        self.business_queue_space = 20
        self.business_queue_horizontal_space = int(self.rect.width * 0.75)
        self.queue_horizontal_space = self.business_queue_horizontal_space * self.queue_number
        
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
        
        # Setting the exit points
        self.exit_points = list(reversed(self.target_points))
            
        # Adding the queuing point of the business
        self.business_queuing_point_start = self.business_target["object"].rect.x + \
            int(self.business_target["object"].rect.width * self.business_target["meta"]["queuing_point"])
        self.business_queuing_position = self.get_queuing_position()
        self.target_points.append((
            self.business_queuing_position,
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
        
        
    def get_queuing_position(self):
        self.queue_horizontal_space = self.business_queue_horizontal_space * self.queue_number
        if self.business_target["meta"]["queue_direction"] == "left":
            return self.business_queuing_point_start - self.queue_horizontal_space
        elif self.business_target["meta"]["queue_direction"] == "right":
            return self.business_queuing_point_start + self.queue_horizontal_space
    
    
    def update(self):
        if self.is_exiting:
            super().update()
            return
        
        if self.business_target["object"].business_state == "closed":
            self.served_and_leave()
        
        super().animate()
        if self.is_standing:
            if self.business_target["meta"]["queue_direction"] == "left":
                self.direction = "right"
                self.is_flipped = True
            
            if self.queue_number > 0:
                current_queue = self.business_target["object"].queue
                person_ahead_of_line = current_queue[self.queue_number - 1]
                persons_rect = person_ahead_of_line.rect
                
                is_in_queue = persons_rect.midbottom[1] == self.rect.midbottom[1]
                is_in_front = abs(persons_rect.x - self.rect.x) <= self.queue_horizontal_space
                    
                if not person_ahead_of_line.is_standing and not is_in_queue and not is_in_front:
                    queue_holder = current_queue[self.queue_number]
                    current_queue[self.queue_number] = current_queue[self.queue_number - 1]
                    current_queue[self.queue_number - 1] = queue_holder
                    
                    person_ahead_of_line.queue_move(1)
                    self.queue_move(-1)
            return
        
        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            absolute_movement = int(self.speed_tick)
            try:
                target_point = self.target_points[self.target_index]
                if self.rect.midbottom == target_point:
                    self.target_index += 1
                    
                self.target_slope = self.get_slope(self.current_position_in_float, self.target_points[self.target_index])
            except IndexError:
                if self.is_served:
                    self.is_exiting = True
                    self.speed_tick = 0
                    return
                elif not self.is_served:
                    self.is_standing = True
            self.previous_position_in_float = copy.deepcopy(self.current_position_in_float)
            
            total_increment = [0, 0]
            for increments in range(absolute_movement):
                total_increment[0] += self.target_slope[0]
                total_increment[1] += self.target_slope[1]
                
                assumed_position = copy.deepcopy(self.current_position_in_float)
                assumed_position[0] += total_increment[0]
                assumed_position[1] += total_increment[1]
                assumed_position = tuple(assumed_position)
                
                if assumed_position == target_point:
                    break
                
            self.current_position_in_float[0] += total_increment[0]
            self.current_position_in_float[1] += total_increment[1]
            
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
            
            self.speed_tick -= absolute_movement
            
        
    def served_and_leave(self):
        if not self.is_served and self.is_standing:
            self.is_served = True
            self.is_standing = False
            
            self.target_points = self.exit_points
            self.target_index = 0
        
    
    def queue_move(self, relative_position: int):
        self.is_standing = False
        
        self.queue_number += relative_position
        self.business_queuing_position = self.get_queuing_position()
        
        self.target_points.append((
            self.business_queuing_position,
            self.business_target["object"].rect.y +
            self.business_target["object"].rect.height +
            self.business_queue_space
        ))
        