from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

import pygame
import copy


class InformationMenu(GenericMenu):
    """
    Menu showing the TLDR's tutorial documentation of the game.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress["statistics"]
        self.tutorial_text: list[str] = self.main.data.tutorial_text
        self.guide = [
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
        ]
        self.max_width = len(self.guide[0])
        self.width_center = int(self.max_width / 2)
        self.max_height = len(self.guide)
        self.pages: list[list[str]] = []
        self.page: list[str] = []
        self.page_index = 0
        self.page_total = 0
        self._parse_tutorial_text()

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["Game Tutorial"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.information_message = Message(
            self.screen,
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.17) + self.canvas_rect.y,
            ),
        )
        self.previous_button = Button(
            self.main,
            self._previous_page,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.8) + self.canvas_rect.y,
            ),
            button_ratio=0.8,
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
                int(self.canvas_rect.width * 0.85) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.8) + self.canvas_rect.y,
            ),
            button_ratio=0.8,
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

    def _parse_tutorial_text(self):
        formats = [
            "TITLE",
            "SUB-TITLE",
            "PARAGRAPH",
            "LIST",
        ]

        page = []
        line = ""

        def _insert_line(page, line):
            if len(page) >= self.max_height:
                self.pages.append(page)
                return [line]
            page.append(line)
            return page

        for index, unparsed_line in enumerate(self.tutorial_text):
            split_line = unparsed_line.split(" ")
            code = split_line[0]
            content = split_line[2:]

            assert code in formats
            if code == "TITLE":
                if index > 0:
                    while len(page) < self.max_height:
                        page.append("")
                    self.pages.append(page)
                    page = []

                content = " ".join(content)[: self.max_width]
                start_index = self.width_center - int(len(content) / 2)
                line = " " * start_index + content + " " * start_index
                page = _insert_line(page, line)
                line = ""

            elif code == "SUB-TITLE":
                page = _insert_line(page, "")
                line = ""

                for word in content:
                    if len(line) + len(word) > self.max_width + 1:
                        page = _insert_line(page, line)
                        line = f"{word} "
                        continue

                    line += word + " "

            elif code == "PARAGRAPH":
                line = "  "
                for word in content:
                    if len(line) + len(word) > self.max_width:
                        page = _insert_line(page, line)
                        line = f"{word} "
                        continue

                    line += word + " "

            elif code == "LIST":
                line = "  - "
                for word in content:
                    if len(line) + len(word) > self.max_width + 1:
                        page = _insert_line(page, line)
                        line = f"{word} "
                        continue

                    line += word + " "

            if line != "":
                page = _insert_line(page, line)

        if len(page) > 0:
            while len(page) < self.max_height:
                page.append("")
            self.pages.append(page)

        self.page_total = len(self.pages)

    # Abstract method implementation
    def set_button_states(self):
        self.previous_button.set_disabled(self.page_index == 0)
        self.next_button.set_disabled(self.page_index == self.page_total - 1)

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        current_page = copy.deepcopy(self.pages[self.page_index])
        page_number = f"{self.page_index + 1}/{self.page_total}"
        start_index = (self.width_center - (int(len(page_number) / 2))) - 1
        line = " " * start_index + page_number + " " * start_index
        current_page.append("")
        current_page.append(line)

        self.information_message.set_message(current_page)
        self.set_button_states()

        self.previous_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.next_button.add(self.objects, self.buttons, self.hoverable_buttons)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.information_message.add(self.objects)

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
