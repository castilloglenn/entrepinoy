from game.sprite.button import Button
from game.sprite.message import Message

from game.utility.transition import Transition

import pygame


class Slideshow:
    """
    Class to present both prologue and epilogue in a slideshow manner, showing
    1 photo at a time with a certain duration and a next button.
    """

    def __init__(self, main) -> None:
        self.main = main
        self.running = False

        self.main.data.get_albums()
        self.albums = self.main.data.albums

        self.album = None
        self.slide_gen = None
        self.slide = None

        self.name = None
        self.gender = None

        self.image = None
        self.text = None
        self.coords = None

        # States
        self.INITIAL = 0
        self.READ = 1
        self.BUTTON_HOLD = 2

        self.initial_hold = 1  # plus the reading time (depends on the text length)
        self.words_per_second = 8
        self.total_hold = 0

    def slide_generator(self):
        for index, image_data in self.album.items():
            yield image_data

    def next_slide(self):
        try:
            pronouns = {"MALE": "He", "FEMALE": "She"}
            possessives = {"MALE": "His", "FEMALE": "Her"}
            self.slide = next(self.slide_gen)

            self.image = self.slide["image"][self.gender]
            self.image_rect = self.image.get_rect()
            self.text = []
            for line in self.slide["text"]:
                self.text.append(
                    line.format(
                        player_name=self.name,
                        pronoun=pronouns[self.gender],
                        possessive=possessives[self.gender],
                    )
                )

            self.coords = self.slide["text_rel_coords"]

            message = Message(
                self.image,
                self.text,
                self.main.data.medium_font,
                self.main.data.colors["white"],
                outline_thickness=1,
                top_left_coordinates=(
                    self.image_rect.width * self.coords[0],
                    self.image_rect.height * self.coords[1],
                ),
            )
            message.update()
        except StopIteration:
            self.running = False

            self.album = None
            self.slide_gen = None
            self.slide = None

            self.name = None
            self.gender = None

            self.image = None
            self.text = None
            self.coords = None

    def get_total_hold(self):
        total = 0
        for line in self.text:
            total += len(line.split(" "))

        self.total_hold = self.initial_hold + round(total / self.words_per_second)
        return self.total_hold

    def set_album(self, album, name, gender):
        self.main.data.get_albums()
        assert album in self.albums
        self.album = self.albums[album]
        self.slide_gen = self.slide_generator()
        self.name = name
        self.gender = gender
        self.next_slide()

    def run(self):

        self.running = True
        fps_counter = 0
        seconds_counter = 0

        while self.running:
            # Screen rendering
            self.main.screen.blit(self.image, (0, 0))
            # self.objects.update()

            # Check transition fading, render fade animation
            self.main.transition.update()

            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Closing the game properly
                    self.main.close_game()

            # Updating the display
            self.main.refresh_display()

            # Update timers
            if self.main.transition.alpha > 0:
                continue

            fps_counter += 1
            if fps_counter >= self.main.data.setting["fps"]:
                fps_counter = 0
                seconds_counter += 1
                if seconds_counter == self.total_hold:
                    seconds_counter = 0
                    self.next_slide()
                    self.main.transition.setup_and_fade_out(
                        transition_length=3,
                        duration_length=self.get_total_hold(),
                        display_image=self.image,
                    )
