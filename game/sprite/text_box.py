from game.sprite.message import Message

import pygame
import re


class TextBox(pygame.sprite.Sprite):
    """
    Class to display a simple text box with limit
    """

    def __init__(
        self,
        main,
        text_box_ratio,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
    ):
        super().__init__()

        self.main = main
        self.states = ["focused", "unfocused"]
        self.state = ""
        self.locator = "|"
        self.text = ""
        self.max_length = 10

        self.image = self.main.data.meta_images["text_box"].convert_alpha()

        self.width = int(self.image.get_rect().width * text_box_ratio)
        self.height = int(self.image.get_rect().height * text_box_ratio)

        self.image = pygame.transform.scale(
            self.image, (self.width, self.height)
        ).convert_alpha()
        self.rect = self.image.get_rect()

        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates

        self.update_rect()

        self.message = Message(
            self.main.screen,
            [self.text + self.locator],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.rect.width * 0.0825) + self.rect.x,
                int(self.rect.height * 0.175) + self.rect.y,
            ),
        )

    def get_data(self):
        return self.text

    def update(self):
        self.main.screen.blit(self.image, self.rect)

        if self.state == "focused":
            self.message.set_message([self.text + self.locator])
        else:
            self.message.set_message([self.text])

        self.message.update()

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
        if self.rect.collidepoint(click_coordinates):
            self.state = "focused"

            # Return booleans to prevent overlapping buttons to react the same
            return True

        self.state = "unfocused"
        return False

    def receive_key_inputs(self, event):
        if self.state == "unfocused":
            return False

        if event.key == pygame.K_BACKSPACE:
            if len(self.text) > 0:
                self.text = self.text[:-1]
            return True

        if len(self.text) > self.max_length:
            return True

        char = list(event.unicode)
        if len(char) == 1:
            self.text += char[0]

        """Source (Modified): https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
        Explanation: Need to extract alphanumeric values only from a string"""
        self.text = re.sub(r"\W+", "", self.text.upper())
        return True
