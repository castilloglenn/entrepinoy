from pprint import pprint
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
                meta_data: dict, 
                emojis: dict,
                fps: int, 
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
        self.happy_emoji = emojis["happy_emoji"].convert_alpha()
        self.angry_emoji = emojis["angry_emoji"].convert_alpha()
        self.show_emoji = False
        self.emoji_timeout = 5
        self.on_queue = False
        self.is_standing = False
        self.is_served = False
        self.exit_switch = False
        self.is_exiting = False
        self.safe_spot = safe_spot
        
        # Waiting attributes
        self.fps = fps
        self.frame_length = 1 / self.fps
        self.frame_counter = 0
        self.seconds_counter = 0
        self.temper_in_queue = random.randint(5, 10)
        self.temper_reached = False
        
        # Generating points for the customer to traverse across the scene
        self.target_points = []
        self.target_index = 0
        self.business_queue_space = 10
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
        
        
    def check_self_if_in_queue(self):
        return self.business_target["object"].queue[self.queue_number] is not self


    def check_business_if_open(self):
        return self.business_target["object"].business_state == "open"

    def check_business_if_queue_is_empty(self):
        return len(self.business_target["object"].queue) != 0
            
            
    def animate_queue(self):
        try:
            if self.check_self_if_in_queue():
                self.leave()
            else:
                self.on_queue = True
                
            if self.is_standing and self.check_business_if_open() and self.check_business_if_queue_is_empty():
                if self.business_target["meta"]["queue_direction"] == "left":
                    self.direction = "right"
                    self.is_flipped = True
                else:
                    self.direction = "left"
                    self.is_flipped = False
                
                if self.queue_number > 0:
                    current_queue = self.business_target["object"].queue
                    person_ahead_of_line = current_queue[self.queue_number - 1]
                    is_in_line = person_ahead_of_line.rect.midbottom[1] == self.rect.midbottom[1]
                        
                    if not person_ahead_of_line.is_standing and not is_in_line:
                        queue_holder = current_queue[self.queue_number]
                        current_queue[self.queue_number] = current_queue[self.queue_number - 1]
                        current_queue[self.queue_number - 1] = queue_holder
                        
                        person_ahead_of_line.queue_move(1)
                        self.queue_move(-1)
                return False
            else:
                self.leave()
        except IndexError:
            self.leave()
        
        return True

            
    def animate_movement(self):
        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            absolute_movement = int(self.speed_tick)
            try:
                target_point = self.target_points[self.target_index]
                if self.rect.midbottom == target_point:
                    self.target_index += 1
                    
                self.target_slope = self.get_slope(
                    self.current_position_in_float, 
                    self.target_points[self.target_index]
                )
                
            except IndexError:
                if self.is_served:
                    self.is_exiting = True
                    self.speed_tick = 0
                elif not self.is_served:
                    self.is_standing = True
                return
                    
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
    
    
    def update(self):
        if self.is_exiting:
            super().update()
            return
        
        super().animate()
        if self.animate_queue():
            self.animate_movement()
            
            
    def serve(self):
        self.is_served = True
        self.leave()
            
        
    def leave(self):
        if self.is_standing:
            self.is_standing = False
            self.show_emoji = True
            
            if not self.exit_switch:
                self.on_queue = False
                self.exit_switch = True
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
        
        self.adjust_coordinates()
            
    
    def adjust_coordinates(self):
        if len(self.target_points) > len(self.exit_points) + 1:
            self.final_destination = copy.deepcopy(self.target_points[-1])
            self.target_points = copy.deepcopy(self.target_points[:len(self.exit_points)])
            self.target_points.append(self.final_destination)
            
            if self.target_index > len(self.exit_points) - 1:
                self.target_index = len(self.target_points) - 1
                