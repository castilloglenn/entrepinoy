from typing import *

from game.sprite.message import Message

import pygame


class Transition:
    def __init__(
        self,
        main,
        transition_length: float,
        duration_length: float,
        display_image: pygame.Surface,
        fade_current_frame: bool = False,
        hold_sfx: pygame.mixer.Sound = None,
        unfade_sfx: pygame.mixer.Sound = None,
        center_message: Optional[list] = None,
    ) -> None:
        """Quickly display a transition, this will automatically close upon the
        completion of its animation span.

        Args:
            main (Main): The main class instance
            transition_length (float): the time it takes from being transparent
                to opaque and vice versa.
            duration_length (float): the time it takes to display the image in-
                between the transition periods.
            display_image (pygame.Surface): The image to display in the window.
                Must be full-sized and span across the whole display.
            fade_current_frame (bool, optional): Specifies if the current frame
                comes from a certain window towards another window. Defaults
                initially to False due to the Studio Intro usage, then
                defaults to False.
            hold_sfx (pygame.mixer.Sound, optional): Sound to be played as the
                transition begins. Defaults to None.
            unfade_sfx (pygame.mixer.Sound, optional): Sound to be played as the
                new window's unfading transition begins. Defaults to None.
            center_message (Optional[list]): Optional message to be displayed in
                the center of the window. Defaults to None.
        """
        # State management (Simplified Enum implementation)
        self.FADE_IN = 0
        self.HOLD = 1
        self.FADE_OUT = 2
        self.UNFADE = 3
        self.FINISHED = 4
        self.STATE = self.FADE_IN  # Initial state (At intro)

        # Instance variables
        self.main = main
        self.transition_length = transition_length
        self.duration_length = duration_length
        self.display_image = display_image
        self.fade_current_frame = fade_current_frame
        self.hold_sfx = hold_sfx
        self.unfade_sfx = unfade_sfx
        self.message = Message(
            self.main.screen,
            ["Loading..."],
            self.main.data.title_font,
            self.main.data.colors["white"],
            outline_thickness=2,
            center_coordinates=(
                self.main.data.horizontal_center,
                self.main.data.vertical_center,
            ),
        )
        self.center_message = center_message
        self.setup()

        # Algorithm variables
        self.time_tracker = 0
        self.time_increment = 1 / self.main.data.setting["fps"]
        self.fadeout_length = 0.5  # second(s)
        self.opacity_unit = self.set_opacity_unit(self.transition_length)

    def setup(self):
        # Guide:
        # Alpha values
        #   0 - transparent (invisible)
        # 255 - opaque (fully visible)

        if self.fade_current_frame:
            self.alpha = 0
            self.STATE = self.FADE_OUT
            self.opacity_unit = self.set_opacity_unit(self.fadeout_length)
        else:
            self.alpha = 255
            self.STATE = self.FADE_IN
            self.opacity_unit = self.set_opacity_unit(self.transition_length)

        self.main.display_surface.set_alpha(self.alpha)
        self.sfx_played = False

        if self.center_message != None:
            self.message.set_message(self.center_message)

    def set_opacity_unit(self, max_duration: float):
        assert max_duration
        self.time_unit = max_duration * self.main.data.setting["fps"]
        return 255 / self.time_unit

    def change_state(self, new_state):
        self.STATE = new_state
        self.time_tracker = 0

    def update_alpha(self):
        if self.STATE == self.FADE_IN or self.STATE == self.UNFADE:
            self.alpha = max(self.alpha - self.opacity_unit, 0)
        elif self.STATE == self.FADE_OUT:
            self.alpha = min(self.alpha + self.opacity_unit, 255)
        self.main.display_surface.set_alpha(self.alpha)

    def run(self):
        while self.STATE != self.UNFADE:
            if self.fade_current_frame:
                self.main.screen.blit(self.main.display_surface, (0, 0))
                self.update_alpha()
                self.main.refresh_display()

                if self.alpha >= 255:
                    self.change_state(self.FADE_IN)
                    self.fade_current_frame = False
                    self.setup()
                continue

            if self.STATE == self.FADE_IN:
                if not self.sfx_played and self.hold_sfx:
                    self.main.mixer_meta_channel.play(self.hold_sfx)
                    self.sfx_played = True

                self.main.screen.blit(self.display_image, (0, 0))
                if self.center_message != None:
                    self.message.update()
                self.main.screen.blit(self.main.display_surface, (0, 0))
                self.update_alpha()

                if self.alpha <= 0:
                    self.change_state(self.HOLD)

            elif self.STATE == self.HOLD:
                self.main.screen.blit(self.display_image, (0, 0))
                if self.center_message != None:
                    self.message.update()

                self.time_tracker += self.time_increment
                if self.time_tracker >= self.duration_length:
                    self.change_state(self.FADE_OUT)

            elif self.STATE == self.FADE_OUT:
                self.main.screen.blit(self.display_image, (0, 0))
                if self.center_message != None:
                    self.message.update()
                self.main.screen.blit(self.main.display_surface, (0, 0))
                self.update_alpha()

                if self.alpha >= 255:
                    self.change_state(self.UNFADE)

            self.main.refresh_display()

    def update(self):
        if self.STATE != self.UNFADE:
            return

        self.main.screen.blit(self.main.display_surface, (0, 0))
        self.update_alpha()

        if self.alpha <= 0:
            self.change_state(self.FADE_OUT)

    def setup_and_run(
        self,
        transition_length: float,
        duration_length: float,
        display_image: pygame.Surface,
        fade_current_frame: bool = True,
        hold_sfx: pygame.mixer.Sound = None,
        unfade_sfx: pygame.mixer.Sound = None,
        center_message: str = None,
    ):
        self.transition_length = transition_length
        self.duration_length = duration_length
        self.display_image = display_image
        self.fade_current_frame = fade_current_frame
        self.hold_sfx = hold_sfx
        self.unfade_sfx = unfade_sfx
        self.center_message = center_message

        self.setup()
        self.run()

    def setup_and_fade_out(
        self,
        transition_length: float,
        duration_length: float,
        display_image: pygame.Surface,
        fade_current_frame: bool = True,
        hold_sfx: pygame.mixer.Sound = None,
        unfade_sfx: pygame.mixer.Sound = None,
        center_message: str = None,
    ):
        self.transition_length = transition_length
        self.duration_length = duration_length
        self.display_image = display_image
        self.fade_current_frame = fade_current_frame
        self.hold_sfx = hold_sfx
        self.unfade_sfx = unfade_sfx
        self.center_message = center_message

        self.last_frame = self.main.screen.copy()

        # Override quick fade-out
        self.alpha = 0
        self.STATE = self.FADE_OUT
        self.opacity_unit = self.set_opacity_unit(self.transition_length)
        self.main.display_surface.set_alpha(self.alpha)

        while self.STATE != self.UNFADE:
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Closing the game properly
                    self.main.close_game()

            self.main.screen.blit(self.last_frame, (0, 0))
            self.main.screen.blit(self.main.display_surface, (0, 0))
            self.update_alpha()
            self.main.refresh_display()

            if self.alpha >= 255:
                self.change_state(self.UNFADE)
                self.fade_current_frame = False
