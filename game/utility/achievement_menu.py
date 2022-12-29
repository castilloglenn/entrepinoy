from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

import pygame


class AchievementMenu(GenericMenu):
    """
    Menu showing the list of achievements the user can obtain throughout the game.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress["statistics"]
        self.obtain = self.main.data.meta_images[
            "achievement_trophy_true"
        ].convert_alpha()
        self.not_obtain = self.main.data.meta_images[
            "achievement_trophy_false"
        ].convert_alpha()
        self.achievement_1_rect = self.obtain.get_rect()
        self.achievement_1_rect.topleft = (
            int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
            int(self.canvas_rect.height * 0.235) + self.canvas_rect.y,
        )
        self.achievement_2_rect = self.obtain.get_rect()
        self.achievement_2_rect.topleft = (
            int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
            int(self.canvas_rect.height * 0.442) + self.canvas_rect.y,
        )
        self.achievement_3_rect = self.obtain.get_rect()
        self.achievement_3_rect.topleft = (
            int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
            int(self.canvas_rect.height * 0.652) + self.canvas_rect.y,
        )
        self.bar = "============================================================"
        self.max_width = len("0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234")
        self.width_center = int(self.max_width / 2)
        self.page_index = 0
        self.page_total = 2

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["               Achievements"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )

        page_number = f"{self.page_index + 1}/{self.page_total}"
        start_index = (self.width_center - (int(len(page_number) / 2))) - 1
        line = " " * start_index + page_number + " " * start_index
        self.mission_message = Message(
            self.screen,
            [
                "============================================================",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "============================================================",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "============================================================",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "     0123456789ABCDEFGHIJ012345678           ",
                "============================================================",
                f"{line}",
            ],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.17) + self.canvas_rect.y,
            ),
        )
        coords = {
            "1": [0.749, 0.238],
            "2": [0.749, 0.445],
            "3": [0.749, 0.655],
        }
        self.mission_1_collect_button = Button(
            self.main,
            lambda x: print("test"),
            top_left_coordinates=(
                int(self.canvas_rect.width * coords["1"][0]) + self.canvas_rect.x,
                int(self.canvas_rect.height * coords["1"][1]) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_2_collect_button = Button(
            self.main,
            lambda x: print("test"),
            top_left_coordinates=(
                int(self.canvas_rect.width * coords["2"][0]) + self.canvas_rect.x,
                int(self.canvas_rect.height * coords["2"][1]) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_3_collect_button = Button(
            self.main,
            lambda x: print("test"),
            top_left_coordinates=(
                int(self.canvas_rect.width * coords["3"][0]) + self.canvas_rect.x,
                int(self.canvas_rect.height * coords["3"][1]) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )

        self.previous_button = Button(
            self.main,
            self._previous_page,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.85) + self.canvas_rect.y,
            ),
            button_ratio=0.5,
            **{
                "idle": self.main.data.meta_images[
                    "previous_arrow_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "previous_arrow_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "previous_arrow_button_disabled"
                ].convert_alpha(),
            },
        )
        self.next_button = Button(
            self.main,
            self._next_page,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.884) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.85) + self.canvas_rect.y,
            ),
            button_ratio=0.5,
            **{
                "idle": self.main.data.meta_images[
                    "next_arrow_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "next_arrow_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "next_arrow_button_disabled"
                ].convert_alpha(),
            },
        )

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    def _previous_page(self, args):
        self.page_index = max(self.page_index - 1, 0)

    def _next_page(self, args):
        self.page_index = min(self.page_index + 1, self.page_total - 1)

    # Abstract method implementation
    def set_button_states(self):
        ...

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.

        self.set_button_states()

    def update(self):
        super().update()

        # Render trophies images
        if self.background.enable:
            self.main.screen.blit(self.obtain, self.achievement_1_rect)
            self.main.screen.blit(self.not_obtain, self.achievement_2_rect)
            self.main.screen.blit(self.obtain, self.achievement_3_rect)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.mission_message.add(self.objects)

        self.mission_1_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_2_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_3_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.previous_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.next_button.add(self.objects, self.buttons, self.hoverable_buttons)
