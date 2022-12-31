from game.utility.new_game_input_menu import NewGameInputMenu
from game.utility.new_game_starter_menu import NewGameStarterMenu


class Prologue:
    """
    This class will present the initial sequences of the game upon starting a
    new save file/pressing new game button. The sequences will be:
    1. Name and Gender selection/input window
    2. Starting Business selection window
    3. Prologue Story (Frames) Presentation Window
    """

    def __init__(self, main) -> None:
        # Setting up the assets
        self.main = main

        # # 1. Name/Gender Menu
        self.name = None
        self.gender = None
        self.input_menu = NewGameInputMenu(main)

        # # 2. Starter picks
        self.starter = None
        self.starter_menu = NewGameStarterMenu(main)

        # # 3. Prologue
        self.album_name = "prologue"

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
        self.input_menu.run()
        self.name, self.gender = self.input_menu.get_data()

        self.starter_menu.run()
        self.starter = self.starter_menu.get_data()

        self.create_save_file()

        self.main.slide_show.set_album(
            self.album_name,
            self.name,
            self.gender,
        )
        self.main.transition.setup_and_fade_out(
            transition_length=2,
            duration_length=self.main.slide_show.get_total_hold(),
            display_image=self.main.slide_show.image,
        )
        self.main.slide_show.run()
