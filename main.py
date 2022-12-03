# %%
from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button

from game.response_menu import ResponseMenu
from game.sliding_menu import SlidingMenu
from game.confirm_menu import ConfirmMenu

from game.debug import Debugger
from game.library import Library

from scene_builder import Scene
from region import Map
from setting import Setting

import pygame
import os, sys


class Main:
    """
    This will be the main module of the game.
    This runs the main menu of the game when played.
    """

    def __init__(self):
        # Setting up the debugger
        self.debug = Debugger()

        # Centering the game window on the screen
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        # Setting up the game
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        pygame.mouse.set_cursor(pygame.cursors.tri_left)

        # Setting up the data
        self.data = Library()
        self.screen = None
        self.is_full_screen = self.data.setting["full_screen"]
        self.clock = None
        self.initialize_game()

        self.volume_bgm = self.data.setting["bgm"]
        self.volume_sfx = self.data.setting["sfx"]

        self.mixer_meta_channel = pygame.mixer.Channel(0)
        self.mixer_buttons_channel = pygame.mixer.Channel(1)
        self.mixer_coins_channel = pygame.mixer.Channel(2)

        self.mixer_channels = [
            self.mixer_meta_channel,
            self.mixer_buttons_channel,
            self.mixer_coins_channel,
        ]

        pygame.mixer.music.set_volume(self.volume_bgm)
        for channel in self.mixer_channels:
            channel.set_volume(self.volume_sfx)

        self.show_studio_intro = self.data.meta["intro_show"]

        # Screen surface (for transitions)
        self.display_surface = pygame.Surface(
            (self.data.setting["game_width"], self.data.setting["game_height"])
        )
        self.display_surface.fill(self.data.colors["black"])
        self.display_surface.convert_alpha()

        # Menus
        self.sliding_menu = SlidingMenu(self)
        self.confirm_menu = ConfirmMenu(self)
        self.response_menu = ResponseMenu(self)

        # Setting up other windows
        self.scene_window = None
        if self.data.progress is not None:
            self.scene_window = Scene(self)
        self.setting_window = Setting(self)
        self.map_window = Map(self)

        # Sprites and sprite groups
        self.buttons = pygame.sprite.Group()
        self.new_game_button = Button(
            self,
            self.check_save_file,
            top_left_coordinates=(
                int(self.data.setting["game_width"] * 0.375),
                int(self.data.setting["game_height"] * 0.45),
            ),
            **{
                "idle": self.data.title_screen["new_game_button_idle"],
                "hovered": self.data.title_screen["new_game_button_hovered"],
            },
        )
        self.new_game_button.add(self.buttons)

        self.continue_button = Button(
            self,
            self.continue_game,
            top_left_coordinates=(
                int(self.data.setting["game_width"] * 0.375),
                int(self.data.setting["game_height"] * 0.57),
            ),
            **{
                "idle": self.data.title_screen["continue_button_idle"],
                "hovered": self.data.title_screen["continue_button_hovered"],
                "disabled": self.data.title_screen["continue_button_disabled"],
            },
        )
        self.continue_button.add(self.buttons)

        self.setting_button = Button(
            self,
            self.setting_callback,
            top_left_coordinates=(
                int(self.data.setting["game_width"] * 0.375),
                int(self.data.setting["game_height"] * 0.69),
            ),
            **{
                "idle": self.data.title_screen["setting_button_idle"],
                "hovered": self.data.title_screen["setting_button_hovered"],
            },
        )
        self.setting_button.add(self.buttons)

        self.exit_button = Button(
            self,
            self.exit_callback,
            top_left_coordinates=(
                int(self.data.setting["game_width"] * 0.375),
                int(self.data.setting["game_height"] * 0.81),
            ),
            **{
                "idle": self.data.title_screen["exit_button_idle"],
                "hovered": self.data.title_screen["exit_button_hovered"],
            },
        )
        self.exit_button.add(self.buttons)

        # Mouse related variable
        self.last_mouse_pos = None

        if self.show_studio_intro:
            self.present_intro()

        # Main loop
        self.debug.log("Memory after initialization:")
        self.debug.memory_log()

        self.running = True
        self.main_loop()

    def initialize_game(self):
        # Title
        pygame.display.set_caption(
            self.data.meta["title"] + " " + self.data.meta["version"]
        )
        self.debug.log(f"Game Title: {self.data.meta['title']}")
        self.debug.log(f"Game Version: {self.data.meta['version']}")

        # Icon
        pygame.display.set_icon(self.data.meta_images["icon"])

        # Setting the screen size
        if self.is_full_screen:
            self.screen = pygame.display.set_mode(
                (self.data.setting["game_width"], self.data.setting["game_height"]),
                pygame.FULLSCREEN | pygame.SCALED,
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.data.setting["game_width"], self.data.setting["game_height"])
            )
        self.debug.log(f"Display Width: {self.data.setting['game_width']}")
        self.debug.log(f"Display Height: {self.data.setting['game_height']}")

        # Setting the clock
        self.clock = pygame.time.Clock()

        self.debug.log(f"Game FPS: {self.data.setting['fps']}")

    def refresh_display(self):
        pygame.display.update()
        self.clock.tick(self.data.setting["fps"])

    def close_game(self):
        pygame.mixer.quit()
        pygame.quit()
        self.debug.close()
        sys.exit()

    def mouse_click_events(self, event):
        click_coordinates = event.pos

        # If the user clicked on left mouse button
        if event.button == 1:
            for button in self.buttons:
                button.check_clicked(click_coordinates)

        # If the user clicked on the right mouse button
        if event.button == 3:
            pass

        # If the user scrolls the mouse wheel upward
        if event.button == 4:
            pass

        # If the user scrolls the mouse wheel downward
        if event.button == 5:
            pass

    def mouse_drag_events(self, event):
        # This variable always saves the last mouse location to be used by the
        #   key_events() function, because we can't always get the location
        #   of the mouse if the only event is key press
        self.last_mouse_pos = event.pos

        # Making sure the user only holds one button at a time
        if event.buttons[0] + event.buttons[1] + event.buttons[2] == 1:
            # If the user is dragging the mouse with left mouse button
            if event.buttons[0] == 1:
                pass

            # If the user is dragging the mouse with the right mouse button
            if event.buttons[2] == 1:
                pass

        # Hovering through display check
        else:
            for button in self.buttons:
                button.check_hovered(self.last_mouse_pos)

    def key_events(self, keys):
        # If the user pressed the "del" key, (enter explanation here)
        if keys[pygame.K_DELETE]:
            pass

        # If the user pressed the "a" key, (enter explanation here)
        if keys[pygame.K_a]:
            pass

        # If the user pressed the "d" key, (enter explanation here)
        if keys[pygame.K_d]:
            pass

    def global_key_down_events(self, key):
        if key == pygame.K_F1:
            self.debug.log(f"F1 Trigger: Memory check")
            self.debug.memory_log()

    def check_save_file(self, *args):
        if self.data.progress == None:
            self.create_new_game()
        else:
            self.confirm_menu.set_message_and_callback(
                [
                    "Are you sure you want",
                    " to start a new game?",
                    "",
                    "All your progress will",
                    "be reset.",
                ],
                self.create_new_game,
            )
            self.confirm_menu.enable = True

    def create_new_game(self):
        self.debug.log("Create new game entered")
        self.data.create_new_save_file("buko_stall")

        if self.scene_window is None:
            self.scene_window = Scene(self)
        else:
            self.scene_window.reconstruct(self)
        self.scene_window.run()

    def continue_game(self, *args):
        self.debug.new_line()
        self.debug.log("Continue game entered")
        self.scene_window.run()

    def setting_callback(self, *args):
        self.setting_window.run()

    def exit_callback(self, *args):
        self.close_game()

    def present_intro(self):
        self.intro_transition = self.data.meta["intro_transition"]
        self.intro_duration = self.data.meta["intro_duration"]

        intro = True
        second = 0
        frame_count = 0
        alpha = 255
        increment = (255 / self.data.setting["fps"]) / self.intro_transition
        fade = "in"  # values: in, out, hold

        self.mixer_meta_channel.play(self.data.music["studio_intro"])
        while intro:
            # Screen rendering
            self.screen.blit(self.data.meta_images["studio"], (0, 0))
            self.display_surface.set_alpha(alpha)

            if fade == "in":
                alpha -= increment
                alpha = max(alpha, 0)
            elif fade == "out":
                alpha += increment
                alpha = min(alpha, 255)

            self.screen.blit(self.display_surface, (0, 0))

            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Closing the game properly
                    self.close_game()

            # Updating the display
            self.refresh_display()

            frame_count += 1
            if frame_count == self.data.setting["fps"]:
                frame_count = 0
                second += 1

                if fade == "in" and second >= self.intro_transition:
                    fade = "hold"
                    second = 0
                elif fade == "hold" and second >= self.intro_duration:
                    fade = "out"
                    second = 0
                elif fade == "out" and second >= self.intro_transition:
                    intro = False

    def main_loop(self):
        pygame.mixer.music.load(self.data.music["main_menu"])
        pygame.mixer.music.play(-1)

        while self.running:
            # Screen rendering
            self.screen.blit(self.data.title_screen["title_screen"], (0, 0))

            # Updating sprites
            self.buttons.update()

            # Checking if menus will be displaying
            self.confirm_menu.update()

            # Event processing
            for event in pygame.event.get():
                if self.confirm_menu.enable:
                    self.confirm_menu.handle_event(event)
                else:
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_click_events(event)
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_drag_events(event)
                    elif event.type == pygame.KEYDOWN:
                        self.global_key_down_events(event.key)

            # Key pressing events (holding keys applicable)
            keys = pygame.key.get_pressed()
            self.key_events(keys)

            # Final checks on the continue button for initial game exit to menu
            if self.data.progress is None:
                self.continue_button.set_disabled(True)
            else:
                self.continue_button.set_disabled(False)

            # Updating the display
            self.refresh_display()

        # Closing the game properly
        self.close_game()


if __name__ == "__main__":
    Main()

# %%
