import pygame


class Slider(pygame.sprite.Sprite):
    """
    class to simulate slider option and get inputs 0-100
    """
    def __init__(self, main, label,
                 top_left_coordinates=None, 
                 center_coordinates=None, 
                 midbottom_coordinates=None,):
        super().__init__()

        self.main = main
        self.label = label
        if label == "bgm":
            self.value = self.main.data.setting["bgm"]
        if label == "sfx":
            self.value = self.main.data.setting["sfx"]
        self.state = "idle" # or dragged
        
        self.image = self.main.data.meta_images["slider"].convert_alpha()
        self.knob_idle = self.main.data.meta_images["slider_knob_idle"].convert_alpha()
        self.knob_dragged = self.main.data.meta_images["slider_knob_dragged"].convert_alpha()
        self.knob_image = self.knob_idle
        
        self.rect = self.image.get_rect()
        self.knob_rect = self.knob_idle.get_rect()
        
        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates
        
        self.is_held = False
        self.half_knob = int(self.knob_rect.width / 2)
        self.last_coordinates = None
        self.y_center = None
        self.ratio_start = None
        self.ratio_end = None
        self.ratio_diff = None
        
        self.set_image_and_rect()
        
    
    def update(self):
        self.main.screen.blit(self.image, self.rect)
        self.main.screen.blit(self.knob_image, self.knob_rect)
        
        if self.is_held:
            drag_x = self.last_coordinates[0]
            if drag_x >= self.rect.x and drag_x <= self.rect.x + self.rect.width:
                if drag_x < self.ratio_start:
                    drag_x = self.ratio_start
                elif drag_x > self.ratio_end:
                    drag_x = self.ratio_end
                
                self.knob_rect.center = (drag_x, self.y_center)
                self.value = round((drag_x - self.ratio_start) / self.ratio_diff, 2)
                self.update_data()
            
            self.set_image_and_rect()
            
        
    def set_image_and_rect(self):
        if self.state == "idle":
            self.knob_image = self.knob_idle
        elif self.state == "dragged":
            self.knob_image = self.knob_dragged
        
        self.update_rect()
        
        
    def update_rect(self):
        if self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates is not None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)
            
        self.y_center = self.rect.center[1]
        self.ratio_start = self.rect.x + self.half_knob
        self.ratio_end = self.rect.x + (self.rect.width - self.half_knob)
        self.ratio_diff = self.ratio_end - self.ratio_start
        
        self.knob_rect.center = (self.ratio_start + int(self.ratio_diff * self.value)
                                 , self.y_center)
        
        
    def check_dragged(self, drag_coordinates):
        self.last_coordinates = drag_coordinates
        if self.is_held:
            return True
        
        if self.knob_rect.collidepoint(drag_coordinates):
            if self.state != "dragged":
                self.state = "dragged"
                
            self.is_held = True
            return True
        
        self.is_held = False
        self.undrag()
        return False
            
            
    def update_data(self):
        if self.label == "bgm":
            self.main.data.setting["bgm"] = self.value
            pygame.mixer.music.set_volume(self.value)
        elif self.label == "sfx":
            self.main.data.setting["sfx"] = self.value
            for channel in self.main.mixer_channels:
                channel.set_volume(self.value)
        
        self.main.data.set_dict_to_json("config", "settings.json", self.main.data.setting)
        
        
    def undrag(self):
        if self.state != "idle":
            self.state = "idle"
            self.set_image_and_rect()
        self.is_held = False
        self.update()
        