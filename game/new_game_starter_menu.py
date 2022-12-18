from game.generic_menu import GenericMenu

import pygame


class NewGameStarterMenu(GenericMenu):
    """
    Menu showing the three starter businesses for the user to pick.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        ...

        # Instantiate buttons and objects
        self.window_background = self.main.data.meta_images[
            "window_background"
        ].convert_alpha()
        self.menu_background = self.main.data.meta_images[
            "menu_background"
        ].convert_alpha()

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
        ...
