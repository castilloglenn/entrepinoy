from game.utility.generic_menu import GenericMenu
from game.sprite.message import Message

import pygame


class ProfileMenu(GenericMenu):
    """
    This class will handle menu that is related to the profile of the user
    containing their details, business status, financial status, and the game
    progress such as achievements and etc.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress

        # Instantiate buttons and objects
        self.news_message = Message(
            self.screen,
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    # ...

    # Abstract method implementation
    def set_button_states(self):
        ...

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        [
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
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
        ]
        max_width = 45
        max_height = 16
        message = []

        # Line 1
        # Guide        "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append("                  Profile")

        # Line 2

        # Line 3

        # Line 4

        # Line 5

        # Line 6

        # Line 7

        # Line 8

        # Line 9

        # Line 10

        # Line 11

        # Line 12

        # Line 13

        # Line 14

        # Line 15

        # Line 16

        self.news_message.set_message(message)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.news_message.add(self.objects)
