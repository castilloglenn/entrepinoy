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
                 fps: int, animation_rate: float, speed: int):
        super().__init__(screen, name, spritesheet, meta_data, 
                         fps, animation_rate)
        
        self.fps = fps
        self.speed = speed / fps
        self.speed_tick = 0
        self.direction = random.choice(["left", "right"])
        
        self.crowd_top = int(self.screen.get_height() * 0.75)
        self.crowd_bottom = int(self.screen.get_height() * 0.82)
        
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
                self.kill()
            elif self.rect.x >= self.screen.get_width() + self.rect.width and self.direction == "right":
                self.kill()
            
            self.speed_tick -= absolute_movement
        
        super().update()
