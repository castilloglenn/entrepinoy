from datetime import datetime
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
        self.customer_statistics = self.get_dict_from_json("library", "customer_statistics.json")
        self.meta = self.get_dict_from_json("config", "meta.json")
        self.setting = self.get_dict_from_json("config", "settings.json")
        
        # Checking the save data
        try:
            self.progress = self.get_dict_from_json("progress", "progress.json")
        except FileNotFoundError:
            self.progress = None
        
        # Fonts
        self.small_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 10),
            "size" : 10
        }
        self.medium_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 25),
            "size" : 25
        }
        
        # Images 
        self.meta_images = {
            "icon" : self.get_image("meta", "game_icon.png"),
            "studio" : self.get_image("meta", "studio.png"),
            "menu_background" : self.get_image("meta", "menu_background.png"),
            "confirm_button_idle" : self.get_image("meta", "confirm_button_idle.png"),
            "confirm_button_hovered" : self.get_image("meta", "confirm_button_hovered.png"),
            "cancel_button_idle" : self.get_image("meta", "cancel_button_idle.png"),
            "cancel_button_hovered" : self.get_image("meta", "cancel_button_hovered.png")
        }
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
            "profile_holder_outline" : self.get_image("scene", "profile_holder_outline.png")
        }
        self.crowd_spritesheets = {
            "-1" : {
                "sheet" : self.get_image("test", "test.png"),
                "data" : self.get_dict_from_spritesheet("test", "test.json")
            },
            "0" : {
                "sheet" : self.get_image("crowd", "0.png"),
                "data" : self.get_dict_from_spritesheet("crowd", "0.json")
            },
            "1" : {
                "sheet" : self.get_image("crowd", "1.png"),
                "data" : self.get_dict_from_spritesheet("crowd", "1.json")
            },
            "2" : {
                "sheet" : self.get_image("crowd", "2.png"),
                "data" : self.get_dict_from_spritesheet("crowd", "2.json")
            },
        }
        self.business_images = {
            "buko_stall" : {
                # "idle" : self.get_image("business", "buko_stall_idle.png"),
                "closed" : None,
                "outline" : None,
                "employee": {
                    "spritesheet" : None,
                    "json" : None
                }
            },
            "fish_ball_stand" : {
                # "idle" : self.get_image("business", "fish_ball_stand_idle.png"),
                "closed" : None,
                "outline" : None,
                "employee": {
                    "spritesheet" : None,
                    "json" : None
                }
            },
            "sorbetes" : {
                # "idle" : self.get_image("business", "sorbetes_idle.png"),
                "closed" : None,
                "outline" : None,
                "employee": {
                    "spritesheet" : None,
                    "json" : None
                }
            },
            "sari_sari_store" : {
                "idle" : self.get_image("business", "sari_sari_store_idle.png"),
                "closed" : self.get_image("business", "sari_sari_store_closed.png"),
                "outline" : self.get_image("business", "sari_sari_store_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "sari_sari_store_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "sari_sari_store_employee.json")
                }
            },
            "ukay_ukay" : {
                # "idle" : self.get_image("business", "ukay_ukay_idle.png"),
                # "closed" : self.get_image("business", "ukay_ukay_closed.png"),
                "outline" : None,
                "employee": {
                    "spritesheet" : None,
                    "json" : None
                }
            },
            "food_cart" : {
                # "idle" : self.get_image("business", "food_cart_idle.png"),
                # "hovered" : self.get_image("business", "food_cart_hovered.png"),
                "closed" : None,
                "outline" : None,
                "employee": {
                    "spritesheet" : None,
                    "json" : None
                }
            }
        }
        
        # Common Coordinates (converted to integers)
        self.vertical_center = int(self.setting["game_height"] / 2)
        self.horizontal_center = int(self.setting["game_width"] / 2)
        
        # Colors
        self.colors = {
            "black" : (0, 0, 0),
            "white" : (255, 255, 255),
            "orange" : (249, 154, 77)
        }
    
    
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
            
    
    def create_new_save_file(self):
        self.progress = {
            "time": datetime.strftime(datetime.now(), "%Y/%m/%d, %H:%M:%S.%f"),
            "last_login": "",
            "cash": 5000.0000000000000
        }
        self.set_dict_to_json("progress", "progress.json", self.progress)


# if __name__ == "__main__":
#     test = Library()
#     test_data = {
#         "time" : "2022/04/05, 18:50:40"
#     }
#     test.set_dict_to_json("progress", "progress.json", test_data)
