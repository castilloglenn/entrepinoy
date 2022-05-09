import pygame


class Toggler(pygame.sprite.Sprite):
    """
    class to simulate toggle button
    """
    def __init__(self, main, label,
                 top_left_coordinates=None, 
                 center_coordinates=None, 
                 midbottom_coordinates=None,):
        super().__init__()

        self.main = main
        self.label = label
        self.value = None
        
        self.image = None
        self.rect = None
        
        self.on_image = self.main.data.meta_images["toggler_on"].convert_alpha()
        self.off_image = self.main.data.meta_images["toggler_off"].convert_alpha()
        
        if self.label == "full_screen":
            self.value = self.main.data.setting["full_screen"]
                
        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates
            
        self.set_image_and_rect()
        
    
    def update(self):
        self.main.screen.blit(self.image, self.rect)
            
        
    def set_image_and_rect(self):
        if self.value:
            self.image = self.on_image
        else:
            self.image = self.off_image
        
        self.rect = self.image.get_rect()
        
        if self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates is not None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)
        
        
    def check_clicked(self, click_coordinates):
        if self.rect.collidepoint(click_coordinates):
            self.main.mixer_coins_channel.play(self.main.data.music["button_clicked"])
            self.value = not self.value
            self.set_image_and_rect()
            self.update_data()
            
            return True
        return False
            
            
    def update_data(self):
        if self.label == "full_screen":
            self.main.data.setting["full_screen"] = self.value
            
            if self.value:
                self.main.screen = pygame.display.set_mode(
                    (self.main.data.setting["game_width"],
                    self.main.data.setting["game_height"]), 
                    pygame.FULLSCREEN | pygame.SCALED
                )
            else:
                self.main.screen = pygame.display.set_mode(
                    (self.main.data.setting["game_width"],
                    self.main.data.setting["game_height"])
                )
                
            self.main.data.set_dict_to_json("config", "settings.json", self.main.data.setting)
        