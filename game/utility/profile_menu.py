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
            ],
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
        ...

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.news_message.add(self.objects)
