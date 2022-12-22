from game.sprite.message import Message

import pygame
import re


class RadioButton(pygame.sprite.Sprite):
    """
    Class to display a simple text box with limit
    """

    def __init__(
        self,
        main,
        value,
        radio_button_ratio,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
    ):
        super().__init__()

        self.main = main
        self.value = value
        self.is_selected = False
        self.radio_group = None

        self.idle = self.main.data.meta_images["radio_button_idle"].convert_alpha()
        self.selected = self.main.data.meta_images[
            "radio_button_selected"
        ].convert_alpha()

        self.width = int(self.idle.get_rect().width * radio_button_ratio)
        self.height = int(self.idle.get_rect().height * radio_button_ratio)

        self.idle = pygame.transform.scale(
            self.idle, (self.width, self.height)
        ).convert_alpha()
        self.selected = pygame.transform.scale(
            self.selected, (self.width, self.height)
        ).convert_alpha()

        self.image = self.idle
        self.rect = self.image.get_rect()

        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates

        self.update_rect()

    def set_radio_group(self, radio_group):
        self.radio_group = radio_group

    def get_data(self):
        return self.value

    def check_selected(self):
        return self.is_selected

    def unselect(self):
        self.is_selected = False

    def update(self):
        if self.is_selected:
            self.main.screen.blit(self.selected, self.rect)
        else:
            self.main.screen.blit(self.idle, self.rect)

    def update_rect(self):
        if self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates is not None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)

    def check_clicked(self, click_coordinates):
        assert self.radio_group
        if self.rect.collidepoint(click_coordinates) and not self.is_selected:
            self.is_selected = True

            for radio_button in self.radio_group:
                if radio_button is not self:
                    radio_button.unselect()
