import pygame


class Prologue:
    """
    This class will present the initial sequences of the game upon starting a
    new save file/pressing new game button. The sequences will be:
    1. Name and Gender selection/input window
    2. Starting Business selection window
    3. Prologue Story (Frames) Presentation window
    """

    def __init__(self, main) -> None:
        # Setting up the assets
        self.main = main
        self.running = False

    def run(self):
        pass
