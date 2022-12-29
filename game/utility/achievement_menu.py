from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

from numerize.numerize import numerize
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
        self.data = self.main.data.progress["achievements"]
        self.pages = []
        self.page_index = 0
        self.page_total = 0

        displayed_per_page = 3
        page = []
        for achievement in self.data:
            page.append(achievement)
            if len(page) >= displayed_per_page:
                self.pages.append(page)
                self.page_total += 1
                page = []

        if len(page) > 0:
            self.pages.append(page)
            self.page_total += 1

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

        self.achievement_message = Message(
            self.screen,
            [""],
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
        self.achievement_1_collect_button = Button(
            self.main,
            self._achievement_1_collect,
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
        self.achievement_2_collect_button = Button(
            self.main,
            self._achievement_2_collect,
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
        self.achievement_3_collect_button = Button(
            self.main,
            self._achievement_3_collect,
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
    def _notify_success(self, reward):
        assert isinstance(reward, float)
        self.main.response_menu.queue_message(
            [
                f"",
                f"You have received the",
                f"reward amounting to",
                f"P{reward:,.2f}",
                f"",
            ]
        )

    def _previous_page(self, args):
        self.page_index = max(self.page_index - 1, 0)

    def _next_page(self, args):
        self.page_index = min(self.page_index + 1, self.page_total - 1)

    def _achievement_1_collect(self, args):
        if len(self.pages[self.page_index]) >= 1:
            self.data[self.pages[self.page_index][0]]["obtained"] = True
            self.main.data.progress["cash"] += self.data[
                self.pages[self.page_index][0]
            ]["reward"]
            self._notify_success(self.data[self.pages[self.page_index][0]]["reward"])
            self.data[self.pages[self.page_index][0]]["reward"] = 0.0
            self.main.mixer_coins_channel.play(self.main.data.music["earn_coins"])

    def _achievement_2_collect(self, args):
        if len(self.pages[self.page_index]) >= 2:
            self.data[self.pages[self.page_index][1]]["obtained"] = True
            self.main.data.progress["cash"] += self.data[
                self.pages[self.page_index][1]
            ]["reward"]
            self._notify_success(self.data[self.pages[self.page_index][1]]["reward"])
            self.data[self.pages[self.page_index][1]]["reward"] = 0.0
            self.main.mixer_coins_channel.play(self.main.data.music["earn_coins"])

    def _achievement_3_collect(self, args):
        if len(self.pages[self.page_index]) >= 3:
            self.data[self.pages[self.page_index][2]]["obtained"] = True
            self.main.data.progress["cash"] += self.data[
                self.pages[self.page_index][2]
            ]["reward"]
            self._notify_success(self.data[self.pages[self.page_index][2]]["reward"])
            self.data[self.pages[self.page_index][2]]["reward"] = 0.0
            self.main.mixer_coins_channel.play(self.main.data.music["earn_coins"])

    # Abstract method implementation
    def set_button_states(self):
        self.previous_button.set_disabled(self.page_index == 0)
        self.next_button.set_disabled(self.page_index == self.page_total - 1)

        if len(self.pages[self.page_index]) >= 1:
            achievement_data = self.data[self.pages[self.page_index][0]]
            if (
                achievement_data["value"] == achievement_data["requirement"]
                and not achievement_data["obtained"]
            ):
                self.achievement_1_collect_button.set_disabled(False)
            else:
                self.achievement_1_collect_button.set_disabled(True)

        if len(self.pages[self.page_index]) >= 2:
            achievement_data = self.data[self.pages[self.page_index][1]]
            if (
                achievement_data["value"] == achievement_data["requirement"]
                and not achievement_data["obtained"]
            ):
                self.achievement_2_collect_button.set_disabled(False)
            else:
                self.achievement_2_collect_button.set_disabled(True)

        if len(self.pages[self.page_index]) >= 3:
            achievement_data = self.data[self.pages[self.page_index][2]]
            if (
                achievement_data["value"] == achievement_data["requirement"]
                and not achievement_data["obtained"]
            ):
                self.achievement_3_collect_button.set_disabled(False)
            else:
                self.achievement_3_collect_button.set_disabled(True)

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        message = [self.bar]
        for achievement in self.pages[self.page_index]:
            data = self.data[achievement]
            value = numerize(data["value"])
            achievement_desc = data["description"][:2]
            progress = data["description"][2].format(value=value)
            achievement_desc.append(progress)

            message += achievement_desc
            message.append(self.bar)

        page_number = f"{self.page_index + 1}/{self.page_total}"
        start_index = (self.width_center - (int(len(page_number) / 2))) - 1
        line = " " * start_index + page_number + " " * start_index
        message.append(line)

        self.achievement_message.set_message(messages=message)
        self.set_button_states()

    def update(self):
        super().update()

        # Render trophies images
        if self.background.enable:
            if len(self.pages[self.page_index]) >= 1:
                if self.data[self.pages[self.page_index][0]]["obtained"]:
                    self.main.screen.blit(self.obtain, self.achievement_1_rect)
                else:
                    self.main.screen.blit(self.not_obtain, self.achievement_1_rect)

            if len(self.pages[self.page_index]) >= 2:
                if self.data[self.pages[self.page_index][1]]["obtained"]:
                    self.main.screen.blit(self.obtain, self.achievement_2_rect)
                else:
                    self.main.screen.blit(self.not_obtain, self.achievement_2_rect)

            if len(self.pages[self.page_index]) >= 3:
                if self.data[self.pages[self.page_index][2]]["obtained"]:
                    self.main.screen.blit(self.obtain, self.achievement_3_rect)
                else:
                    self.main.screen.blit(self.not_obtain, self.achievement_3_rect)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.achievement_message.add(self.objects)

        self.achievement_1_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.achievement_2_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.achievement_3_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.previous_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.next_button.add(self.objects, self.buttons, self.hoverable_buttons)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user scrolls the mouse wheel downward
            if event.button == 4:
                self.page_index = max(self.page_index - 1, 0)
                return

            # If the user scrolls the mouse wheel upward
            if event.button == 5:
                self.page_index = min(self.page_index + 1, self.page_total - 1)
                return
