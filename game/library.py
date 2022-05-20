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
        #   config folder
        self.meta = self.get_dict_from_json("config", "meta.json")
        self.setting = self.get_dict_from_json("config", "settings.json")
        #   library folder
        self.business = self.get_dict_from_json("library", "business.json")
        self.category = self.get_dict_from_json("library", "category.json")
        self.crowd_statistics = self.get_dict_from_json("library", "crowd_statistics.json")
        self.customer_statistics = self.get_dict_from_json("library", "customer_statistics.json")
        self.location = self.get_dict_from_json("library", "location.json")
        
        # Checking the save data
        try:
            self.progress = self.get_dict_from_json("progress", "progress.json")
        except FileNotFoundError:
            self.progress = None
        
        # Images 
        self.meta_images = {
            "icon" : self.get_image("meta", "game_icon.png"),
            "studio" : self.get_image("meta", "studio.png"),
            
            "menu_background" : self.get_image("meta", "menu_background.png"),
            "window_background" : self.get_image("meta", "window_background.png"),
            
            "toggler_on" : self.get_image("meta", "toggler_on.png"),
            "toggler_off" : self.get_image("meta", "toggler_off.png"),
            
            "back_button_idle" : self.get_image("meta", "back_button_idle.png"),
            "back_button_hovered" : self.get_image("meta", "back_button_hovered.png"),
            
            "slider" : self.get_image("meta", "slider.png"),
            "slider_knob_idle" : self.get_image("meta", "slider_knob_idle.png"),
            "slider_knob_dragged" : self.get_image("meta", "slider_knob_dragged.png"),
            "sliding_menu" : self.get_image("meta", "sliding_menu.png"),
            
            "confirm_button_idle" : self.get_image("meta", "confirm_button_idle.png"),
            "confirm_button_hovered" : self.get_image("meta", "confirm_button_hovered.png"),
            
            "cancel_button_idle" : self.get_image("meta", "cancel_button_idle.png"),
            "cancel_button_hovered" : self.get_image("meta", "cancel_button_hovered.png"),
            
            "sliding_menu_button_idle" : self.get_image("meta", "sliding_menu_button_idle.png"),
            "sliding_menu_button_hovered" : self.get_image("meta", "sliding_menu_button_hovered.png"),
            
            "map_button_idle" : self.get_image("meta", "map_icon_idle.png"),
            "map_button_disabled" : self.get_image("meta", "map_icon_disabled.png"),
            "map_button_outline" : self.get_image("meta", "map_icon_outline.png"),
            
            "mission_button_idle" : self.get_image("meta", "mission_icon_idle.png"),
            "mission_button_disabled" : self.get_image("meta", "mission_icon_disabled.png"),
            "mission_button_outline" : self.get_image("meta", "mission_icon_outline.png"),
            
            "crypto_button_idle" : self.get_image("meta", "crypto_icon_idle.png"),
            "crypto_button_disabled" : self.get_image("meta", "crypto_icon_disabled.png"),
            "crypto_button_outline" : self.get_image("meta", "crypto_icon_outline.png"),
            
            "achievement_button_idle" : self.get_image("meta", "achievement_icon_idle.png"),
            "achievement_button_disabled" : self.get_image("meta", "achievement_icon_disabled.png"),
            "achievement_button_outline" : self.get_image("meta", "achievement_icon_outline.png"),
            
            "setting_button_idle" : self.get_image("meta", "setting_icon_idle.png"),
            "setting_button_disabled" : self.get_image("meta", "setting_icon_disabled.png"),
            "setting_button_outline" : self.get_image("meta", "setting_icon_outline.png"),
            
            "news_button_idle" : self.get_image("meta", "news_icon_idle.png"),
            "news_button_disabled" : self.get_image("meta", "news_icon_disabled.png"),
            "news_button_outline" : self.get_image("meta", "news_icon_outline.png"),
            
            "stock_button_idle" : self.get_image("meta", "stocks_icon_idle.png"),
            "stock_button_disabled" : self.get_image("meta", "stocks_icon_disabled.png"),
            "stock_button_outline" : self.get_image("meta", "stocks_icon_outline.png"),
            
            "home_icon_idle" : self.get_image("meta", "home_icon_idle.png"),
            "home_icon_disabled" : self.get_image("meta", "home_icon_disabled.png"),
            "home_icon_outline" : self.get_image("meta", "home_icon_outline.png")
        }
        self.title_screen = {
            "title_screen" : self.get_image("title_screen", "title_screen.png"),
            
            "new_game_button_idle" : self.get_image("title_screen", "new_game_button_idle.png"),
            "new_game_button_hovered" : self.get_image("title_screen", "new_game_button_hovered.png"),
            
            "continue_button_idle" : self.get_image("title_screen", "continue_button_idle.png"),
            "continue_button_hovered" : self.get_image("title_screen", "continue_button_hovered.png"),
            "continue_button_disabled" : self.get_image("title_screen", "continue_button_disabled.png"),
            
            "setting_button_idle" : self.get_image("title_screen", "setting_button_idle.png"),
            "setting_button_hovered" : self.get_image("title_screen", "setting_button_hovered.png"),
            
            "exit_button_idle" : self.get_image("title_screen", "exit_button_idle.png"),
            "exit_button_hovered" : self.get_image("title_screen", "exit_button_hovered.png")
        }
        self.background = {
            "test_location" : {
                "midnight" : self.get_image("scene", "midnight.png"),
                "early_morning" : self.get_image("scene", "early_morning.png"),
                "morning" : self.get_image("scene", "morning.png"),
                "noon" : self.get_image("scene", "noon.png"),
                "afternoon" : self.get_image("scene", "afternoon.png"),
                "night" : self.get_image("scene", "night.png")
            },
            "location_a" : {
                "midnight" : self.get_image("scene", "location_a_midnight.png"),
                "early_morning" : self.get_image("scene", "location_a_early_morning.png"),
                "morning" : self.get_image("scene", "location_a_morning.png"),
                "noon" : self.get_image("scene", "location_a_noon.png"),
                "afternoon" : self.get_image("scene", "location_a_afternoon.png"),
                "night" : self.get_image("scene", "location_a_night.png")
            }
        }
        self.scene = {
            "profile_holder_idle" : self.get_image("scene", "profile_holder_idle.png"),
            "profile_holder_outline" : self.get_image("scene", "profile_holder_outline.png"),
            
            "serve_button_idle" : self.get_image("scene", "serve_button_idle.png"),
            "serve_button_hovered" : self.get_image("scene", "serve_button_hovered.png"),
            
            "collect_sales_button_idle" : self.get_image("scene", "collect_sales_button_idle.png"),
            "collect_sales_button_hovered" : self.get_image("scene", "collect_sales_button_hovered.png"),
            "collect_sales_button_disabled" : self.get_image("scene", "collect_sales_button_disabled.png"),
            
            "upgrades_button_idle" : self.get_image("scene", "upgrades_button_idle.png"),
            "upgrades_button_hovered" : self.get_image("scene", "upgrades_button_hovered.png"),
            "upgrades_button_disabled" : self.get_image("scene", "upgrades_button_disabled.png"),
            
            "hire_employee_button_idle" : self.get_image("scene", "hire_employee_button_idle.png"),
            "hire_employee_button_hovered" : self.get_image("scene", "hire_employee_button_hovered.png"),
            "hire_employee_button_disabled" : self.get_image("scene", "hire_employee_button_disabled.png"),
            
            "purchase_business_button_idle" : self.get_image("scene", "purchase_business_button_idle.png"),
            "purchase_business_button_hovered" : self.get_image("scene", "purchase_business_button_hovered.png"),
            "purchase_business_button_disabled" : self.get_image("scene", "purchase_business_button_disabled.png"),
            
            "sell_business_button_idle" : self.get_image("scene", "sell_business_button_idle.png"),
            "sell_business_button_hovered" : self.get_image("scene", "sell_business_button_hovered.png"),
            "sell_business_button_disabled" : self.get_image("scene", "sell_business_button_disabled.png"),
            
            "start_business_button_idle" : self.get_image("scene", "start_business_button_idle.png"),
            "start_business_button_hovered" : self.get_image("scene", "start_business_button_hovered.png"),
            "start_business_button_disabled" : self.get_image("scene", "start_business_button_disabled.png")
        }
        self.emojis = {
            "happy_emoji" : self.get_image("scene", "happy_emoji.png"),
            "angry_emoji" : self.get_image("scene", "angry_emoji.png")
        }
        self.crowd_spritesheets = {
            "-1" : {
                "sheet" : self.get_image("test", "test.png"),
                "data" : self.get_dict_from_spritesheet("test", "test.json")
            }
        }
        for crowd_index in range(0, 19): # 18 is the last number
            string_index = str(crowd_index)
            self.crowd_spritesheets[string_index] = {
                "sheet" : self.get_image("crowd", f"{string_index}.png"),
                "data" : self.get_dict_from_spritesheet("crowd", f"{string_index}.json")
            }
        self.vehicle_spritesheets = {}
        for vehicle_index in range(0, 4): # 3 is the last number
            string_index = str(vehicle_index)
            self.vehicle_spritesheets[string_index] = {
                "sheet" : self.get_image("vehicle", f"{string_index}.png"),
                "data" : self.get_dict_from_spritesheet("vehicle", f"{string_index}.json")
            }
            
        self.business_images = {
            "buko_stall" : { # 100% complete
                "idle" : self.get_image("business", "buko_stall_idle.png"),
                "closed" : self.get_image("business", "buko_stall_closed.png"),
                "outline" : self.get_image("business", "buko_stall_closed_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "buko_stall_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "buko_stall_employee.json")
                }
            },
            "fish_ball_stand" : {
                "idle" : self.get_image("business", "fish_ball_stand_idle.png"),
                "closed" : self.get_image("business", "fish_ball_stand_closed.png"),
                "outline" : self.get_image("business", "fish_ball_stand_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "buko_stall_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "buko_stall_employee.json")
                }
            },
            "sorbetes" : {
                "idle" : self.get_image("business", "sorbetes_idle.png"),
                "closed" : self.get_image("business", "sorbetes_closed.png"),
                "outline" : self.get_image("business", "sorbetes_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "buko_stall_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "buko_stall_employee.json")
                }
            },
            "sari_sari_store" : { # 100% complete
                "idle" : self.get_image("business", "sari_sari_store_idle.png"),
                "closed" : self.get_image("business", "sari_sari_store_closed.png"),
                "outline" : self.get_image("business", "sari_sari_store_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "sari_sari_store_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "sari_sari_store_employee.json")
                }
            },
            "ukay_ukay" : {
                "idle" : self.get_image("business", "ukay_ukay_idle.png"),
                "closed" : self.get_image("business", "ukay_ukay_closed.png"),
                "outline" : self.get_image("business", "ukay_ukay_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "ukay_ukay_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "ukay_ukay_employee.json")
                }
            },
            "food_cart" : {
                "idle" : self.get_image("business", "food_cart_idle.png"),
                "closed" : self.get_image("business", "food_cart_closed.png"),
                "outline" : self.get_image("business", "food_cart_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "food_cart_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "food_cart_employee.json")
                }
            },
            "test_business_a" : { # 100% complete
                "idle" : self.get_image("business", "sari_sari_store_idle.png"),
                "closed" : self.get_image("business", "sari_sari_store_closed.png"),
                "outline" : self.get_image("business", "sari_sari_store_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "sari_sari_store_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "sari_sari_store_employee.json")
                }
            },
            "test_business_b" : {
                "idle" : self.get_image("business", "ukay_ukay_idle.png"),
                "closed" : self.get_image("business", "ukay_ukay_closed.png"),
                "outline" : self.get_image("business", "ukay_ukay_outline.png"),
                "employee": {
                    "spritesheet" : self.get_image("business", "ukay_ukay_employee.png"),
                    "json" : self.get_dict_from_spritesheet("business", "ukay_ukay_employee.json")
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
            "orange" : (249, 154, 77),
            "yellow" : (255, 215, 0),
            "brown" : (54, 35, 35)
        }
        
        # Music BG and SFX
        self.music = {
            "main_menu" : self.get_bgm("Cool-Menu-Loop.mp3"),
            "studio_intro" : self.get_sfx("SynthChime1.mp3"),
            "button_hovered" : self.get_sfx("UI_Quirky20.mp3"),
            "button_clicked" : self.get_sfx("UI-Quirky_37.mp3"),
            "earn_coins" : self.get_sfx("Coins2.mp3")
        }
        
        # Fonts
        self.small_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 10),
            "size" : 10
        }
        self.medium_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 18),
            "size" : 16
        }
        self.large_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 25),
            "size" : 25
        }
        self.title_font = {
            "family" : self.get_font("PixelEmulator-xq08.ttf", 40),
            "size" : 40
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
            
            
    def get_sfx(self, music_name):
        dirname = os.path.dirname(__file__)
        music_path = os.path.join(dirname, "..", "assets", "music", "sfx", music_name)
        return pygame.mixer.Sound(music_path)
            
            
    def get_bgm(self, music_name):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, "..", "assets", "music", "bgm", music_name)
    

    def get_font(self, font_name: str, size: int):
        dirname = os.path.dirname(__file__)
        font_path = os.path.join(dirname, "..", "assets", "fonts", font_name)
        return pygame.font.Font(font_path, size)
    
    
    def set_dict_to_json(self, folder_name: str, json_name: str, data: dict):
        dirname = os.path.dirname(__file__)
        json_path = os.path.join(dirname, folder_name, json_name)

        with open(json_path, "w+") as json_file:
            json.dump(data, json_file, indent=4)
            
    
    def create_new_save_file(self, starter):
        self.progress = {
            "time": datetime.strftime(datetime.now(), "%Y/%m/%d, %H:%M:%S.%f"),
            "last_login": "",
            "last_location" : "location_a",
            "cash": 5000.0000000000000,
    
            "businesses": {
                "location_a": {
                    "street_food": {
                        "date_acquired": datetime.strftime(datetime.now(), "%Y/%m/%d, %H:%M:%S.%f"),
                        "type": starter,
                        "ownership": True,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    },
                    "sari_sari_store": {
                        "date_acquired": "",
                        "ownership": False,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    },
                    "ukay_ukay": {
                        "date_acquired": "",
                        "ownership": False,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    },
                    "food_cart": {
                        "date_acquired": "",
                        "ownership": False,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    }
                },
                "test_location": {
                    "test_business_a": {
                        "date_acquired": "",
                        "ownership": False,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    },
                    "test_business_b": {
                        "date_acquired": "",
                        "ownership": False,
                        "is_open": False,
                        "open_until": "",
                        "has_employee": False,
                        "sales": 0.0,
                        "lifetime_sales": 0.0,
                        "last_profit" : 0.0,
                        "lifetime_profit" : 0.0,
                        "last_visited" : ""
                    }
                }
            }
        }
        
        self.set_dict_to_json("progress", "progress.json", self.progress)


# if __name__ == "__main__":
#     test = Library()
#     test_data = {
#         "time" : "2022/04/05, 18:50:40"
#     }
#     test.set_dict_to_json("progress", "progress.json", test_data)
