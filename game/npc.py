from game.sprite.spritesheet import Spritesheet
import pygame
import random

import gc


class NPC(Spritesheet):
    """
    This class is has a spritesheet and basic movements like turning and moving
    at a certain speed.
    """
    def __init__(self, screen: pygame.Surface, name: str, 
                 spritesheet: pygame.Surface, meta_data: dict, fps: int):
        self.min_speed = 60
        self.max_speed = 90
        
        self.min_animation_speed = 8
        self.max_animation_speed = 12
        
        self.speed_value = random.randint(self.min_speed, self.max_speed)
        self.speed_ratio = (self.speed_value - self.min_speed) / (self.max_speed - self.min_speed)
        
        self.animation_scale = self.max_animation_speed - self.min_animation_speed
        self.animation_rate = (self.max_animation_speed - (self.animation_scale * self.speed_ratio)) / 100
        
        print(f"Speed: {self.speed_value}, Animation: {self.animation_rate}")
        
        super().__init__(screen, name, spritesheet, meta_data, 
                         fps, self.animation_rate)
        
        self.fps = fps
        self.speed = self.speed_value / fps
        self.speed_tick = 0
        self.direction = random.choice(["left", "right"])
        
        self.crowd_top = int(self.screen.get_height() * 0.75)
        self.crowd_bottom = int(self.screen.get_height() * 0.81)
        
        if self.direction == "left":
            self.rect.midbottom = (
                self.screen.get_width() + self.rect.width,
                random.randint(self.crowd_top, self.crowd_bottom)
            )
        elif self.direction == "right":
            self.is_flipped = True
            self.rect.midbottom = (
                0 - self.rect.width,
                random.randint(self.crowd_top, self.crowd_bottom)
            )
        
        
    def update(self):
        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            absolute_movement = int(self.speed_tick)
            if self.direction == "left":
                self.rect.x -= absolute_movement
            elif self.direction == "right":
                self.rect.x += absolute_movement
            
            if self.rect.x <= 0 - self.rect.width and self.direction == "left":
                self.free()
            elif self.rect.x >= self.screen.get_width() + self.rect.width and self.direction == "right":
                self.free()
            
            self.speed_tick -= absolute_movement
        
        super().update()
    
