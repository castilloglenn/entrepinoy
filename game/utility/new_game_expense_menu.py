from game.sprite.menu_background import MenuBackground
from game.sprite.radio_button import RadioButton
from game.sprite.text_box import TextBox
from game.sprite.message import Message
from game.sprite.button import Button

import pygame


class NewGameExpenseMenu:
    """
    Menu showing the input form for user's daily expenses.
    Game-blocking menu
    """

    def __init__(self, main) -> None:
        self.main = main
        self.running = False

        # Instantiate logical variables
        self.expense = None
        self.first_radio_button_value = 500.0
        self.second_radio_button_value = 1_000.0
        self.third_radio_button_value = 1_500.0

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

        self.expense_message = Message(
            self.main.screen,
            [
                "How much does your daily",
                "expenses cost?",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.gui_background_rect.width * 0.5) + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.125)
                + self.gui_background_rect.y,
            ),
        )
        self.first_message = Message(
            self.main.screen,
            [
                f"P{self.first_radio_button_value:,.2f}",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.425)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.33)
                + self.gui_background_rect.y,
            ),
        )
        self.first_radio_button = RadioButton(
            self.main,
            value=self.first_radio_button_value,
            radio_button_ratio=0.8,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.325)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.3) + self.gui_background_rect.y,
            ),
        )
        self.second_message = Message(
            self.main.screen,
            [
                f"P{self.second_radio_button_value:,.2f}",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.425)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.48)
                + self.gui_background_rect.y,
            ),
        )
        self.second_radio_button = RadioButton(
            self.main,
            value=self.second_radio_button_value,
            radio_button_ratio=0.8,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.325)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.45)
                + self.gui_background_rect.y,
            ),
        )
        self.third_message = Message(
            self.main.screen,
            [
                f"P{self.third_radio_button_value:,.2f}",
            ],
            self.main.data.input_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.425)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.63)
                + self.gui_background_rect.y,
            ),
        )
        self.third_radio_button = RadioButton(
            self.main,
            value=self.third_radio_button_value,
            radio_button_ratio=0.8,
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.325)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.6) + self.gui_background_rect.y,
            ),
        )

        self.next_button = Button(
            self.main,
            self.validate_fields,
            center_coordinates=(
                int(self.gui_background_rect.width * 0.5) + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.85)
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
        self.expense_message.add(self.objects)
        self.first_message.add(self.objects)
        self.second_message.add(self.objects)
        self.third_message.add(self.objects)
        self.first_radio_button.add(self.objects, self.buttons, self.radio_group)
        self.second_radio_button.add(self.objects, self.buttons, self.radio_group)
        self.third_radio_button.add(self.objects, self.buttons, self.radio_group)
        self.next_button.add(self.objects, self.buttons, self.hoverable_buttons)

        # Radio buttons
        self.first_radio_button.set_radio_group(self.radio_group)
        self.second_radio_button.set_radio_group(self.radio_group)
        self.third_radio_button.set_radio_group(self.radio_group)

    def get_data(self) -> tuple:
        assert self.expense
        return self.expense

    def validate_fields(self, args):
        self.expense = None

        for radio_button in self.radio_group:
            if radio_button.check_selected():
                self.expense = radio_button.get_data()

        errors = []
        if not self.expense:
            errors.append("")
            errors.append("Please select")
            errors.append("an expense amount.")

        if len(errors) > 0:
            self.main.response_menu.queue_message(errors)
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

                    # elif event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_F1:
                    #         self.validate_fields(None)
                    #         print(self.get_data())

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
