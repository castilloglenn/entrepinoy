import pygame
import json
import os


class Library():
    """
    The library contains all the data from the json folder with the same name.
    This includes the images in the assets folder, organized in dictionary type.
    This includes the most usable data like colors and basic calculations.
    """
    def __init__(self):
        # JSON data
        self.business = self.get_dict_from_json("library", "business.json")
        self.category = self.get_dict_from_json("library", "category.json")
        self.crowd_statistics = self.get_dict_from_json("library", "crowd_statistics.json")
        self.meta = self.get_dict_from_json("config", "meta.json")
        self.setting = self.get_dict_from_json("config", "settings.json")
        self.progress = self.get_dict_from_json("progress", "progress.json")
        
        # Fonts
        self.paragraph_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 10),
            "size" : 10
        }
        
        # Images 
        self.icon = self.get_image("meta", "game_icon.png")
        self.studio = self.get_image("meta", "studio.png")
        
        self.title_screen = {
            "bg" : self.get_image("title_screen", "bg.png"),
            "new_game_idle" : self.get_image("title_screen", "new_game_button_idle.png"),
            "new_game_hovered" : self.get_image("title_screen", "new_game_button_hovered.png"),
            "continue_idle" : self.get_image("title_screen", "continue_button_idle.png"),
            "continue_hovered" : self.get_image("title_screen", "continue_button_hovered.png")
        }
        self.background = {
            "midnight" : self.get_image("scene", "midnight.png"),
            "early_morning" : self.get_image("scene", "early_morning.png"),
            "morning" : self.get_image("scene", "morning.png"),
            "noon" : self.get_image("scene", "noon.png"),
            "afternoon" : self.get_image("scene", "afternoon.png"),
            "night" : self.get_image("scene", "night.png")
        }
        self.scene = {
            "profile_holder_idle" : self.get_image("scene", "profile_holder_idle.png"),
            "profile_holder_hovered" : self.get_image("scene", "profile_holder_hovered.png")
        }
        self.spritesheets = {
            "test" : {
                "sheet" : self.get_image("test", "test.png"),
                "data" : self.get_dict_from_spritesheet("test", "test.json")
            }
        }
        
        # Common Coordinates (converted to integers)
        self.vertical_center = int(self.setting["game_height"] / 2)
        self.horizontal_center = int(self.setting["game_width"] / 2)
        
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.orange = (249, 154, 77)
    
    
    def get_dict_from_json(self, folder_name: str, json_name: str):
        dirname = os.path.dirname(__file__)
        json_path = os.path.join(dirname, folder_name, json_name)

        with open(json_path) as json_file:
            json_dict = json.load(json_file)
        
        return json_dict
    
    
    def get_dict_from_spritesheet(self, folder_name: str, json_name: str):
        dirname = os.path.dirname(__file__)
        json_path = os.path.join(dirname, "..", "assets", "images", folder_name, json_name)

        with open(json_path) as json_file:
            json_dict = json.load(json_file)
        
        return json_dict
        
    
    def get_image(self, folder_name: str,image_name: str):
        dirname = os.path.dirname(__file__)
        image_path = os.path.join(dirname, "..", "assets", "images", folder_name, image_name)
        return pygame.image.load(image_path)
    

    def get_font(self, font_name: str, size: int):
        dirname = os.path.dirname(__file__)
        font_path = os.path.join(dirname, "..", "assets", "fonts", font_name)
        return pygame.font.Font(font_path, size)
    
    
    def set_dict_to_json(self, folder_name: str, json_name: str, data: dict):
        dirname = os.path.dirname(__file__)
        json_path = os.path.join(dirname, folder_name, json_name)

        with open(json_path, "w+") as json_file:
            json.dump(data, json_file, indent=4)


# if __name__ == "__main__":
#     test = Library()
#     test_data = {
#         "time" : "2022/04/05, 18:50:40"
#     }
#     test.set_dict_to_json("progress", "progress.json", test_data)
