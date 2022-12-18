from game.sprite.message import Message
from game.sprite.button import Button

from game.new_game_input_menu import NewGameInputMenu
from game.new_game_starter_menu import NewGameStarterMenu
from game.slideshow import Slideshow

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

        # # 1. Name/Gender Menu
        # self.name = None
        # self.gender = None
        # self.input_menu = NewGameInputMenu(main)

        # # 2. Starter picks
        # self.starter = None
        # self.starter_menu = NewGameStarterMenu(main)

        # # 3. Prologue
        # self.prologue = Slideshow(main)

    def create_save_file(self):
        assert self.name
        assert self.gender
        assert self.starter

        self.main.data.create_new_save_file(
            name=self.name,
            gender=self.gender,
            starter=self.starter,
        )

    def run(self):
        # NOTE Test only
        self.name = "GLENN"
        self.gender = "MALE"

        random_choices = ["buko_stall", "fish_ball_stand", "sorbetes"]
        import random

        self.starter = random.choice(random_choices)

        self.create_save_file()
