from game.sprite.menu_background import MenuBackground
from game.sprite.radio_button import RadioButton
from game.sprite.text_box import TextBox
from game.sprite.message import Message
from game.sprite.button import Button

import pygame


class NewGameInputMenu:
    """
    Menu showing the input form for user's name and gender.
    Game-blocking menu
    """

    def __init__(self, main) -> None:
        self.main = main
        self.running = False

        # Instantiate logical variables
        self.name = None
        self.gender = None

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()
        self.radio_group = pygame.sprite.Group()

        # Instantiate buttons and objects
        self.window_background = self.main.data.meta_images[
            "window_background"
        ].convert_alpha()
        self.gui_background_object = MenuBackground(
            self.main.screen, 0.75, image=self.main.data.meta_images["menu_background"]
        )
        self.gui_background = self.gui_background_object.image
        self.gui_background_rect = self.gui_background_object.rect

        self.name_message = Message(
            self.main.screen,
            [
                "Please enter",
                "your name:",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.075)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.215)
                + self.gui_background_rect.y,
            ),
        )

        self.text_box = TextBox(
            self.main,
            text_box_ratio=0.7,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.485)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.215)
                + self.gui_background_rect.y,
            ),
        )

        self.gender_message = Message(
            self.main.screen,
            [
                "Select your",
                "gender:",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.075)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.425)
                + self.gui_background_rect.y,
            ),
        )

        self.male_radio_button = RadioButton(
            self.main,
            value="MALE",
            radio_button_ratio=0.8,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.485)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.425)
                + self.gui_background_rect.y,
            ),
        )

        self.male_message = Message(
            self.main.screen,
            ["MALE"],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.585)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.455)
                + self.gui_background_rect.y,
            ),
        )

        self.female_radio_button = RadioButton(
            self.main,
            value="FEMALE",
            radio_button_ratio=0.8,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.485)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.575)
                + self.gui_background_rect.y,
            ),
        )

        self.female_message = Message(
            self.main.screen,
            ["FEMALE"],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.585)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.605)
                + self.gui_background_rect.y,
            ),
        )

        self.next_button = Button(
            self.main,
            self.validate_fields,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.485)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.755)
                + self.gui_background_rect.y,
            ),
            button_ratio=2.0,
            **{
                "idle": self.main.data.meta_images["next_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "next_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "next_button_disabled"
                ].convert_alpha(),
            },
        )

        # Objects addition
        self.name_message.add(self.objects)
        self.male_message.add(self.objects)
        self.female_message.add(self.objects)
        self.gender_message.add(self.objects)
        self.text_box.add(self.objects, self.buttons)
        self.male_radio_button.add(self.objects, self.buttons, self.radio_group)
        self.female_radio_button.add(self.objects, self.buttons, self.radio_group)
        self.next_button.add(self.objects, self.buttons, self.hoverable_buttons)

        # Radio buttons
        self.male_radio_button.set_radio_group(self.radio_group)
        self.female_radio_button.set_radio_group(self.radio_group)

    def get_data(self) -> tuple:
        assert self.name
        assert self.gender
        return (self.name, self.gender)

    def validate_fields(self, args):
        self.name = self.text_box.get_data()
        self.gender = None

        for radio_button in self.radio_group:
            if radio_button.check_selected():
                self.gender = radio_button.get_data()

        errors = []
        if len(self.name) < 4:
            errors.append("Name must be 4-10")
            errors.append("characters.")

        if not self.gender:
            errors.append("Please select")
            errors.append("a gender.")

        if len(errors) > 0:
            self.main.response_menu.set_message(errors)
            self.main.response_menu.enable = True
        else:
            self.running = False

    def run(self):
        self.running = True
        while self.running:
            # Screen rendering
            self.main.screen.blit(self.window_background, (0, 0))
            self.main.screen.blit(self.gui_background, self.gui_background_rect)
            self.objects.update()

            # Checking if menus will be displaying
            self.main.confirm_menu.update()
            self.main.response_menu.update()

            # Event processing
            for event in pygame.event.get():
                if self.main.response_menu.enable:
                    self.main.response_menu.handle_event(event)

                elif self.main.confirm_menu.enable:
                    self.main.confirm_menu.handle_event(event)

                else:
                    if event.type == pygame.QUIT:
                        # Closing the game properly
                        self.main.close_game()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            print(self.text_box.get_data())

                        self.text_box.receive_key_inputs(event)

                    elif event.type == pygame.MOUSEMOTION:
                        for button in self.hoverable_buttons:
                            button.check_hovered(event.pos)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = event.pos
                            for button in self.buttons:
                                button.check_clicked(mouse_pos)

            # Updating the display
            self.main.refresh_display()
