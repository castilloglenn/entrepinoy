from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame import SRCALPHA, transform


class Spritesheet(Sprite):
    """
    This class handles the spritesheet of a moving object in a screen display.
    """
    def __init__(self, screen: Surface,
                 name: str, spritesheet: Surface, 
                 meta_data: dict, fps: int, animation_rate: float, 
                 mid_bottom_coordinates=None,
                 center_coordinates=None,
                 top_left_coordinates=None):
        super().__init__()
        
        self.name = name
        self.screen = screen
        self.sprite_sheet = spritesheet
        self.data = meta_data

        # This list holds all the sprites gathered from the spritesheet
        self.sprites = []
        self.sprite_index = 0

        # This speed controls when to switch from sprite animation to the
        #   next animation in the spritesheet
        self.animate_speed = fps * animation_rate
        self.animation_tick = 0

        # Parsing all the sprites contained in the spritesheet
        for index in range(len(self.data['frames'])):
            self.sprites.append(self.fetch_sprite(f'{self.name}_{index + 1}.png'))
        
        # Setting the standing animation for the sprite
        self.is_standing = False
        self.standing_sprite = self.sprites.pop()
            
        self.image = self.sprites[self.sprite_index]
        self.rect = self.image.get_rect()
        
        # Setting the position
        self.mid_bottom_coordinates = mid_bottom_coordinates
        self.center_coordinates = center_coordinates
        self.top_left_coordinates = top_left_coordinates
        self.is_flipped = False
        
        if self.mid_bottom_coordinates is not None:
            self.rect.midbottom = self.mid_bottom_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates


    def fetch_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = Surface((width, height), SRCALPHA, 32)
        image.blit(self.sprite_sheet,(0, 0),(x, y, width, height))
        self.rect = image.get_rect()
        return image.convert_alpha()


    def update(self):
        if self.is_standing:
            if self.is_flipped:
                self.image = transform.flip(self.standing_sprite, True, False)
            else:
                self.image = self.standing_sprite
        else:
            self.animation_tick += 1
            if self.animation_tick >= self.animate_speed:
                self.animation_tick = 0
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                
                if self.is_flipped:
                    self.image = transform.flip(self.sprites[self.sprite_index], True, False)
                else:
                    self.image = self.sprites[self.sprite_index]
            
        # Prevents the self-blitting due to the custom sprite group handles
        #   which sprite blits first based on their y-coordinates
        # self.screen.blit(self.image, self.rect)
        
        
    def free(self):
        print(f"freed coords: {self.rect} direction: {self.direction}")
        self.kill()
