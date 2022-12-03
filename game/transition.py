import pygame


class Transition:
    def __init__(
        self,
        main,
        transition_length: float,
        duration_length: float,
        display_image: pygame.Surface,
        fade_current_frame: bool = True,
    ) -> None:
        """Quickly display a transition, this will automatically close upon the
        completion of its animation span.

        Args:
            main (_type_): The main class instance
            transition_length (float): the time it takes from being transparent
                to opaque and vice versa.
            duration_length (float): the time it takes to display the image in-
                between the transition periods.
            display_image (pygame.Surface): The image to display in the window.
            fade_current_frame (bool, optional): Specifies if the current frame
                comes from a certain window towards another window. Defaults to True.
        """
