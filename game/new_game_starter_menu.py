from game.sprite.menu_background import MenuBackground
from game.sprite.radio_button import RadioButton
from game.sprite.text_box import TextBox
from game.sprite.message import Message
from game.sprite.button import Button

import pygame


class NewGameStarterMenu:
    """
    Menu showing the starter business selection section.
    Game-blocking menu
    """

    def __init__(self, main) -> None:
        self.main = main
        self.running = False

        # Instantiate logical variables
        self.starter = None

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()

        # Instantiate buttons and objects
        self.window_background = self.main.data.meta_images[
            "window_background"
        ].convert_alpha()
        self.gui_background_object = MenuBackground(
            self.main.screen, 0.75, image=self.main.data.meta_images["menu_background"]
        )
        self.gui_background = self.gui_background_object.image
        self.gui_background_rect = self.gui_background_object.rect

        self.choose_message = Message(
            self.main.screen,
            ["Select your preferred type of business:"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.gui_background_rect.width * 0.135)
                + self.gui_background_rect.x,
                int(self.gui_background_rect.height * 0.105)
                + self.gui_background_rect.y,
            ),
        )

        # Coordinates arrangement
        group_1 = (
            int(self.gui_background_rect.width * 0.105) + self.gui_background_rect.x,
            int(self.gui_background_rect.height * 0.205) + self.gui_background_rect.y,
        )
        group_2 = (
            int(self.gui_background_rect.width * 0.38) + self.gui_background_rect.x,
            int(self.gui_background_rect.height * 0.205) + self.gui_background_rect.y,
        )
        group_3 = (
            int(self.gui_background_rect.width * 0.68) + self.gui_background_rect.x,
            int(self.gui_background_rect.height * 0.205) + self.gui_background_rect.y,
        )

        self.buko_icon = self.main.data.meta_images["buko_stall"]
        self.buko_icon_rect = self.buko_icon.get_rect()
        self.buko_icon_coordinates = (
            group_1[0] + (self.buko_icon_rect.width / 2),
            group_1[1],
        )

        self.fish_ball_icon = self.main.data.meta_images["fish_ball_stand"]
        self.fish_ball_icon_coordinates = (
            group_2[0] + (self.buko_icon_rect.width / 2),
            group_2[1],
        )

        self.sorbetes_icon = self.main.data.meta_images["sorbetes"]
        self.sorbetes_icon_coordinates = (
            group_3[0] + (self.buko_icon_rect.width / 2),
            group_3[1],
        )

        buko_dict = self.main.data.starter["buko_stall"]
        self.buko_message = Message(
            self.main.screen,
            [
                f"  Buko Stall",
                f"",
                f"Business Cost: ",
                f"    P{buko_dict['initial_cost']:,.2f}",
                f"Operation Cost: ",
                f"    P{buko_dict['daily_expenses']:,.2f}",
                f"Employee Cost: ",
                f"    P{buko_dict['employee_cost']:,.2f}",
                f"Income Range: ",
                f"    P{buko_dict['income_per_customer_range'][0]:,.2f}-P{buko_dict['income_per_customer_range'][1]:,.2f}",
            ],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                group_1[0],
                int(self.gui_background_rect.height * 0.4) + self.gui_background_rect.y,
            ),
        )

        fish_ball_dict = self.main.data.starter["fish_ball_stand"]
        self.fish_ball_message = Message(
            self.main.screen,
            [
                f"Fish Ball Stand",
                f"",
                f" Business Cost: ",
                f"    P{fish_ball_dict['initial_cost']:,.2f}",
                f" Operation Cost: ",
                f"    P{fish_ball_dict['daily_expenses']:,.2f}",
                f" Employee Cost: ",
                f"    P{fish_ball_dict['employee_cost']:,.2f}",
                f" Income Range: ",
                f"    P{fish_ball_dict['income_per_customer_range'][0]:,.2f}-P{fish_ball_dict['income_per_customer_range'][1]:,.2f}",
            ],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                group_2[0],
                int(self.gui_background_rect.height * 0.4) + self.gui_background_rect.y,
            ),
        )

        sorbetes_dict = self.main.data.starter["sorbetes"]
        self.sorbetes_message = Message(
            self.main.screen,
            [
                f"Sorbetes Cart",
                f"",
                f"Business Cost: ",
                f"    P{sorbetes_dict['initial_cost']:,.2f}",
                f"Operation Cost: ",
                f"    P{sorbetes_dict['daily_expenses']:,.2f}",
                f"Employee Cost: ",
                f"    P{sorbetes_dict['employee_cost']:,.2f}",
                f"Income Range: ",
                f"    P{sorbetes_dict['income_per_customer_range'][0]:,.2f}-P{sorbetes_dict['income_per_customer_range'][1]:,.2f}",
            ],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                group_3[0],
                int(self.gui_background_rect.height * 0.4) + self.gui_background_rect.y,
            ),
        )

        button_nudge = group_1[0] * 0.15
        self.buko_button = Button(
            self.main,
            self.buko_selected,
            top_left_coordinates=(
                group_1[0] + button_nudge,
                int(self.gui_background_rect.height * 0.78)
                + self.gui_background_rect.y,
            ),
            button_ratio=1.5,
            **{
                "idle": self.main.data.meta_images[
                    "select_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "select_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "select_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Select buko stall as your",
                    "preferred first business.",
                ],
            },
        )

        self.fish_ball_button = Button(
            self.main,
            self.fish_ball_selected,
            top_left_coordinates=(
                group_2[0] + button_nudge,
                int(self.gui_background_rect.height * 0.78)
                + self.gui_background_rect.y,
            ),
            button_ratio=1.5,
            **{
                "idle": self.main.data.meta_images[
                    "select_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "select_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "select_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Select fish ball stand as your",
                    "preferred first business.",
                ],
            },
        )

        self.sorbetes_button = Button(
            self.main,
            self.sorbetes_selected,
            top_left_coordinates=(
                group_3[0] + button_nudge,
                int(self.gui_background_rect.height * 0.78)
                + self.gui_background_rect.y,
            ),
            button_ratio=1.5,
            **{
                "idle": self.main.data.meta_images[
                    "select_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "select_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "select_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Select sorbetes cart as your",
                    "preferred first business.",
                ],
            },
        )

        # # Objects addition
        self.choose_message.add(self.objects)
        self.buko_message.add(self.objects)
        self.fish_ball_message.add(self.objects)
        self.sorbetes_message.add(self.objects)
        self.buko_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.fish_ball_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.sorbetes_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

    def get_data(self) -> tuple:
        assert self.starter
        return self.starter

    def buko_selected(self, args):
        self.starter = "buko_stall"
        self.running = False

    def fish_ball_selected(self, args):
        self.starter = "fish_ball_stand"
        self.running = False

    def sorbetes_selected(self, args):
        self.starter = "sorbetes"
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # Screen rendering
            self.main.screen.blit(self.window_background, (0, 0))
            self.main.screen.blit(self.gui_background, self.gui_background_rect)
            self.main.screen.blit(self.buko_icon, self.buko_icon_coordinates)
            self.main.screen.blit(self.fish_ball_icon, self.fish_ball_icon_coordinates)
            self.main.screen.blit(self.sorbetes_icon, self.sorbetes_icon_coordinates)
            self.objects.update()

            # Checking if menus will be displaying
            self.main.confirm_menu.update()
            self.main.response_menu.update()

            # Display tooltips
            for button in self.tooltips:
                button.display_tooltips()

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
