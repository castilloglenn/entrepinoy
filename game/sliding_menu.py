from game.sprite.button import Button

from game.mission_menu import MissionMenu
from game.achievement_menu import AchievementMenu
from game.part_time_menu import PartTimeMenu
from game.news_menu import NewsMenu
from game.bank_menu import BankMenu
from game.stock_menu import StockMenu
from game.crypto_menu import CryptoMenu
from game.info_menu import InformationMenu

import pygame


class SlidingMenu:
    """
    This menu will provide different access to other game modules such as:
    - Region Map
    - Mission
    - Information
    - Bank
    - Part Time
    - Achievement
    - News
    - Crypto
    - Stock
    - Return to Main Menu
    - Setting
    """

    def __init__(self, main):
        self.enable = True
        self.is_tucked = True
        self.is_moving = False
        self.control_dim = True

        self.main = main
        self.callback = None

        # Menu's
        self.menu_initialized = False
        self.mission_menu = None
        self.achievement_menu = None
        self.part_time_menu = None
        self.news_menu = None
        self.bank_menu = None
        self.stock_menu = None
        self.crypto_menu = None
        self.info_menu = None

        self.has_active_module = False
        self.modules = [
            self.mission_menu,
            self.achievement_menu,
            self.part_time_menu,
            self.news_menu,
            self.bank_menu,
            self.stock_menu,
            self.crypto_menu,
            self.info_menu,
        ]

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        # Screen objects
        self.frame_length = 1 / self.main.data.setting["fps"]
        self.dim_max_intensity = 128  # 0-255 color opacity
        self.dim_intensity = 0  # initial state
        self.trigger_button_width = 44
        self.trigger_button_y = 128
        self.travel_speed_per_second = 900
        self.travel_speed_per_frame = self.travel_speed_per_second * self.frame_length

        self.sliding_menu_image = self.main.data.meta_images[
            "sliding_menu"
        ].convert_alpha()
        self.sliding_menu_rect = self.sliding_menu_image.get_rect()
        self.sliding_menu_rect.y = int(
            (self.main.screen.get_rect().height - self.sliding_menu_rect.height) / 2
        )

        self.hidden_endpoint = (
            self.main.screen.get_rect().width - self.trigger_button_width
        )
        self.visible_endpoint = (
            self.main.screen.get_rect().width - self.sliding_menu_rect.width
        )

        self.travel_steps_count = (
            self.hidden_endpoint - self.visible_endpoint
        ) / self.travel_speed_per_frame
        self.dim_speed_per_frame = self.dim_max_intensity / self.travel_steps_count

        self.sliding_menu_button = Button(
            self.main,
            self.switch_state,
            **{
                "idle": self.main.data.meta_images["sliding_menu_button_idle"],
                "hovered": self.main.data.meta_images["sliding_menu_button_hovered"],
            },
        )

        # MENU ICON BUTTONS
        self.map_button = Button(
            self.main,
            self.map_callback,
            **{
                "idle": self.main.data.meta_images["map_button_idle"],
                "outline": self.main.data.meta_images["map_button_outline"],
                "disabled": self.main.data.meta_images["map_button_disabled"],
                "tooltip": ["Region Map"],
            },
        )
        self.mission_button = Button(
            self.main,
            self.mission_callback,
            **{
                "idle": self.main.data.meta_images["mission_button_idle"],
                "outline": self.main.data.meta_images["mission_button_outline"],
                "disabled": self.main.data.meta_images["mission_button_disabled"],
                "tooltip": ["Missions"],
            },
        )
        self.information_button = Button(
            self.main,
            self.information_callback,
            **{
                "idle": self.main.data.meta_images["information_icon_idle"],
                "outline": self.main.data.meta_images["information_icon_outline"],
                "tooltip": ["Tutorial"],
            },
        )

        self.bank_button = Button(
            self.main,
            self.bank_callback,
            **{
                "idle": self.main.data.meta_images["bank_button_idle"],
                "outline": self.main.data.meta_images["bank_button_outline"],
                "disabled": self.main.data.meta_images["bank_button_disabled"],
                "tooltip": ["Bank"],
            },
        )
        self.part_time_button = Button(
            self.main,
            self.part_time_callback,
            **{
                "idle": self.main.data.meta_images["part_time_idle"],
                "outline": self.main.data.meta_images["part_time_outline"],
                "disabled": self.main.data.meta_images["map_button_disabled"],
                "tooltip": ["Part Time"],
            },
        )

        self.news_button = Button(
            self.main,
            self.news_callback,
            **{
                "idle": self.main.data.meta_images["news_button_idle"],
                "outline": self.main.data.meta_images["news_button_outline"],
                "disabled": self.main.data.meta_images["news_button_disabled"],
                "tooltip": ["News"],
            },
        )
        self.crypto_button = Button(
            self.main,
            self.crypto_callback,
            **{
                "idle": self.main.data.meta_images["crypto_button_idle"],
                "outline": self.main.data.meta_images["crypto_button_outline"],
                "disabled": self.main.data.meta_images["crypto_button_disabled"],
                "tooltip": ["Crypto", "Market"],
            },
        )
        self.stock_button = Button(
            self.main,
            self.stock_callback,
            **{
                "idle": self.main.data.meta_images["stock_button_idle"],
                "outline": self.main.data.meta_images["stock_button_outline"],
                "disabled": self.main.data.meta_images["stock_button_disabled"],
                "tooltip": ["Stock", "Market"],
            },
        )

        self.achievement_button = Button(
            self.main,
            self.achievement_callback,
            **{
                "idle": self.main.data.meta_images["achievement_button_idle"],
                "outline": self.main.data.meta_images["achievement_button_outline"],
                "disabled": self.main.data.meta_images["achievement_button_disabled"],
                "tooltip": ["Achievements"],
            },
        )
        self.setting_button = Button(
            self.main,
            self.setting_callback,
            **{
                "idle": self.main.data.meta_images["setting_button_idle"],
                "outline": self.main.data.meta_images["setting_button_outline"],
                "disabled": self.main.data.meta_images["setting_button_disabled"],
                "tooltip": ["Setting"],
            },
        )
        self.main_menu_button = Button(
            self.main,
            self.main_menu_callback,
            **{
                "idle": self.main.data.meta_images["main_menu_button_idle"],
                "outline": self.main.data.meta_images["main_menu_button_outline"],
                "disabled": self.main.data.meta_images["map_button_disabled"],
                "tooltip": ["Return to", "main menu"],
            },
        )

        # TODO This measures attribute is for reference only
        self.measures = {
            "x_base": 0.1730,
            "y_base": 0.0625,
            "x_gap": 0.2695,
            "y_gap": 0.2300,
        }

        self.update_endpoint()

    def initialize_modules(self):
        self.mission_menu = MissionMenu(self.main)
        self.achievement_menu = AchievementMenu(self.main)
        self.part_time_menu = PartTimeMenu(self.main)
        self.news_menu = NewsMenu(self.main)
        self.bank_menu = BankMenu(self.main)
        self.stock_menu = StockMenu(self.main)
        self.crypto_menu = CryptoMenu(self.main)
        self.info_menu = InformationMenu(self.main)

        self.modules = [
            self.mission_menu,
            self.achievement_menu,
            self.part_time_menu,
            self.news_menu,
            self.bank_menu,
            self.stock_menu,
            self.crypto_menu,
            self.info_menu,
        ]

        self.menu_initialized = True

    def show_module(self):
        self.switch_state()
        self.control_dim = False
        self.has_active_module = True

    def map_callback(self, *args):
        self.switch_state()
        self.main.map_window.run()

    def mission_callback(self, *args):
        self.mission_menu.set_data()
        self.mission_menu.enable = True
        self.show_module()

    def information_callback(self, *args):
        self.info_menu.set_data()
        self.info_menu.enable = True
        self.show_module()

    def bank_callback(self, *args):
        self.bank_menu.set_data()
        self.bank_menu.enable = True
        self.show_module()

    def part_time_callback(self, *args):
        self.part_time_menu.set_data()
        self.part_time_menu.enable = True
        self.show_module()

    def news_callback(self, *args):
        self.news_menu.set_data()
        self.news_menu.enable = True
        self.show_module()

    def crypto_callback(self, *args):
        self.crypto_menu.set_data()
        self.crypto_menu.enable = True
        self.show_module()

    def stock_callback(self, *args):
        self.stock_menu.set_data()
        self.stock_menu.enable = True
        self.show_module()

    def achievement_callback(self, *args):
        self.achievement_menu.set_data()
        self.achievement_menu.enable = True
        self.show_module()

    def setting_callback(self, *args):
        self.main.setting_window.run()

    def main_menu_callback(self, *args):
        self.tuck()
        self.main.scene_window.update_data()

        if self.main.scene_window.running:
            self.main.scene_window.running = False

        if self.main.map_window.running:
            self.main.map_window.running = False

        self.main.debug.log("Autosaved progress before going to main menu")
        self.main.debug.log("Exited scene via Sliding Menu")

    def tuck(self):
        if not self.is_tucked:
            self.is_moving = False
            self.is_tucked = True
            self.dim_intensity = 0
            self.update_endpoint()

            for button in self.buttons:
                button.x_coordinate_offset = 0
                button.set_image_and_rect()

    def update_endpoint(self):
        if self.is_tucked:
            self.sliding_menu_rect.x = self.hidden_endpoint
        elif not self.is_tucked:
            self.sliding_menu_rect.x = self.visible_endpoint

        self.sliding_menu_button.top_left_coordinates = (
            self.sliding_menu_rect.x,
            self.sliding_menu_rect.y + self.trigger_button_y,
        )
        # 0,0
        self.map_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625),
        )
        # 0,1
        self.mission_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625),
        )
        # 0,2
        self.achievement_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.0625),
        )
        # 1,0
        self.part_time_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925),
        )
        # 1,1
        self.news_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925),
        )
        # 1,2
        self.bank_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.2925),
        )
        # 2,0
        self.stock_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524),
        )
        # 2,1
        self.crypto_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524),
        )
        # 2,2
        self.setting_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.712),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.524),
        )
        # 3,0
        self.main_menu_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.173),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.754),
        )
        # 3,1
        self.information_button.top_left_coordinates = (
            self.sliding_menu_rect.x + (self.sliding_menu_rect.width * 0.4425),
            self.sliding_menu_rect.y + (self.sliding_menu_rect.height * 0.754),
        )
        # 3,2

        # Clearing the sprite groups before adding the objects back to it
        for obj in self.objects:
            obj.kill()
            del obj
        self.objects.empty()

        self.sliding_menu_button.add(self.objects, self.hoverable_buttons, self.buttons)

        self.map_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.mission_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.information_button.add(self.objects, self.hoverable_buttons, self.buttons)

        self.bank_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.part_time_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.achievement_button.add(self.objects, self.hoverable_buttons, self.buttons)

        self.news_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.crypto_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.stock_button.add(self.objects, self.hoverable_buttons, self.buttons)

        self.setting_button.add(self.objects, self.hoverable_buttons, self.buttons)
        self.main_menu_button.add(self.objects, self.hoverable_buttons, self.buttons)

        for button in self.buttons:
            button.set_image_and_rect()

    def switch_state(self, *args):
        self.is_moving = True

    def pass_event_to_modules(self, event):
        # Sliding menu modules
        for module in self.modules:
            if module.enable:
                module.handle_event(event)

    def handle_event(self, event):
        if not self.enable:
            self.close()
            return

        if event.type == pygame.QUIT:
            # Closing the game properly
            self.main.close_game()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.switch_state()

        elif event.type == pygame.MOUSEMOTION:
            for button in self.hoverable_buttons:
                button.check_hovered(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if (
                    not self.sliding_menu_rect.collidepoint(mouse_pos)
                    and not self.is_tucked
                ):
                    self.switch_state()

                for button in self.buttons:
                    button.check_clicked(mouse_pos)

    def update_sliding(self):
        if self.is_moving or not self.is_tucked:
            # Screen dimming
            if self.control_dim:
                self.main.display_surface.set_alpha(self.dim_intensity)
            else:
                self.main.display_surface.set_alpha(0)
            self.main.screen.blit(self.main.display_surface, (0, 0))

        if self.is_moving:
            if self.is_tucked:
                # then the section is moving left to show, increase dim
                coordinate_change = self.sliding_menu_rect.x - max(
                    self.sliding_menu_rect.x - self.travel_speed_per_frame,
                    self.visible_endpoint,
                )

                self.sliding_menu_rect.x -= int(coordinate_change)
                for obj in self.objects:
                    obj.x_coordinate_offset -= int(coordinate_change)
                    obj.set_image_and_rect()

                self.dim_intensity = min(
                    self.dim_intensity + self.dim_speed_per_frame,
                    self.dim_max_intensity,
                )

                if self.sliding_menu_rect.x <= self.visible_endpoint:
                    self.is_moving = False
                    self.is_tucked = False
            else:  # the body is shown
                # then the section is moving right to hide itself, decrease dim
                coordinate_change = (
                    min(
                        self.sliding_menu_rect.x + self.travel_speed_per_frame,
                        self.hidden_endpoint,
                    )
                    - self.sliding_menu_rect.x
                )

                self.sliding_menu_rect.x += int(coordinate_change)
                for obj in self.objects:
                    obj.x_coordinate_offset += int(coordinate_change)
                    obj.set_image_and_rect()

                self.dim_intensity = max(
                    self.dim_intensity - self.dim_speed_per_frame, 0
                )

                if self.sliding_menu_rect.x >= self.hidden_endpoint:
                    self.is_moving = False
                    self.is_tucked = True
        else:
            self.control_dim = True

    def update(self):
        if not self.enable or not self.menu_initialized:
            return

        self.update_sliding()
        self.main.screen.blit(self.sliding_menu_image, self.sliding_menu_rect)
        self.objects.update()

        for button in self.buttons:
            button.display_tooltips()

        # Sliding Menu Modules
        for module in self.modules:
            if module.enable:
                module.update()

    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()

    def close(self):
        self.clear()
        self.enable = False
