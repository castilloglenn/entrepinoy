import pygame
import json
import os


class Library():
    """
    The library contains all the data from the json folder with the same name.
    """
    def __init__(self):
        # JSON data
        self.business = self.get_dict_from_json("library", "business.json")
        self.meta = self.get_dict_from_json("config", "meta.json")
        self.setting = self.get_dict_from_json("config", "settings.json")
        
        # Images
        self.icon = self.get_image("game_icon.png")
        
        # Colors
        self.black = (0, 0, 0)
    
    
    def get_dict_from_json(self, folder_name: str, json_name: str):
        dirname = os.path.dirname(__file__)
        json_path = os.path.join(dirname, "..", folder_name, json_name)

        with open(json_path) as json_file:
            json_dict = json.load(json_file)
            return json_dict
        
    
    def get_image(self, image_name: str):
        dirname = os.path.dirname(__file__)
        image_path = os.path.join(dirname, "..", "assets", "images", image_name)
        return pygame.image.load(image_path)


