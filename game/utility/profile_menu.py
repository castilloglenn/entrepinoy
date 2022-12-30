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
        message.append("")

        # Line 3
        name = self.data["name"]
        gender = self.data["gender"]
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"Name: {name:<10s}               Gender: {gender:>6s}")

        # Line 4
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"========================STATISTICS=======================")

        # Line 5
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"")

        # Line 6
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        location = self.main.data.city[self.data["last_location"]]
        message.append(f"Current location: {location}")

        # Line 7
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        e_cash = f"P{self.data['cash']:,.2f}"
        message.append(f"E-Cash Balance: {e_cash}")

        # Line 8
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        e_cash = f"P{self.data['bank']['balance']:,.2f}"
        message.append(f"Savings Balance: {e_cash}")

        # Line 9
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        mouse_clicks = self.data["statistics"]["clicks"]
        message.append(f"Total Mouse Clicks: {mouse_clicks}")

        # Line 10
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"10")

        # Line 11
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"11")

        # Line 12
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"12")

        # Line 13
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"13")

        # Line 14
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"14")

        # Line 15
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"15")

        # Line 16
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        message.append(f"16")

        self.news_message.set_message(message)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.news_message.add(self.objects)
