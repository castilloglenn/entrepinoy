from game.sprite.spritesheet import Spritesheet
import pygame
import random


class NPC(Spritesheet):
    """
    This class is has a spritesheet and basic movements like turning and moving
    at a certain speed.
    """
    def __init__(self, screen: pygame.Surface, name: str, 
                 spritesheet: pygame.Surface, meta_data: dict, 
                 fps: int, animation_rate: float, 
                 speed: int, direction: str,
                 mid_bottom_coordinates=None, 
                 center_coordinates=None, 
                 top_left_coordinates=None):
        super().__init__(screen, name, spritesheet, meta_data, 
                         fps, animation_rate, mid_bottom_coordinates, 
                         center_coordinates, top_left_coordinates)
        
        self.fps = fps
        self.speed = speed / fps
        self.speed_tick = 0
        self.direction = direction
        
        
    def update(self):
        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            absolute_movement = int(self.speed_tick)
            if self.direction == "left":
                self.rect.x -= absolute_movement
            elif self.direction == "right":
                self.rect.x += absolute_movement
            
            if self.rect.x <= 0:
                self.is_flipped = True
                self.direction = "right"
            elif self.rect.x + self.rect.width >= self.screen.get_width():
                self.is_flipped = False
                self.direction = "left"
            
            self.speed_tick -= absolute_movement
        
        super().update()
