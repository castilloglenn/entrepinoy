from game.generic_menu import GenericMenu

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
        self.data = None

        # Instantiate buttons and objects
        ...

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
        self.data = self.main.data.progress["statistics"]
        print(self.data)
