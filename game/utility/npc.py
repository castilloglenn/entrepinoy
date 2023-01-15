from game.sprite.spritesheet import Spritesheet

import pygame
import random


class NPC(Spritesheet):
    """
    This class is has a spritesheet and basic movements like turning and moving
    at a certain speed.
    """

    def __init__(
        self,
        main,
        form: str,
        name: str,
        spritesheet: pygame.Surface,
        meta_data: dict,
        fps: int,
    ):
        self.main = main
        self.form = form
        self.hasten = False

        if form == "people":
            self.min_speed = 90
            self.max_speed = 120

            self.min_animation_speed = 10
            self.max_animation_speed = 12
        elif form == "vehicle":
            self.min_speed = 460
            self.max_speed = 560

            self.min_animation_speed = 6
            self.max_animation_speed = 8

        self.speed_value = random.randint(self.min_speed, self.max_speed)
        self.speed_ratio = (self.speed_value - self.min_speed) / (
            self.max_speed - self.min_speed
        )

        self.animation_scale = self.max_animation_speed - self.min_animation_speed
        self.animation_rate = (
            self.max_animation_speed - (self.animation_scale * self.speed_ratio)
        ) / 100

        super().__init__(
            main, form, name, spritesheet, meta_data, fps, self.animation_rate
        )

        self.fps = fps
        self.speed = self.speed_value / fps
        self.speed_tick = 0

        if form == "people":
            self.crowd_top = int(self.screen.get_height() * 0.75)
            self.crowd_bottom = int(self.screen.get_height() * 0.81)

            self.direction = random.choice(["left", "right"])
            if self.direction == "left":
                self.rect.midbottom = (
                    self.screen.get_width() + self.rect.width,
                    random.randint(self.crowd_top, self.crowd_bottom),
                )
            elif self.direction == "right":
                self.is_flipped = True
                self.rect.midbottom = (
                    0 - self.rect.width,
                    random.randint(self.crowd_top, self.crowd_bottom),
                )
        elif form == "vehicle":
            self.left_road = int(self.screen.get_height() * 0.87)
            self.right_road = int(self.screen.get_height() * 0.97)

            y_adjustments = 10  # To lessen the chance to collide vehicles
            self.direction = random.choice(["left", "right"])
            if self.direction == "left":
                self.rect.midbottom = (
                    self.screen.get_width() + self.rect.width,
                    random.randint(
                        self.left_road - y_adjustments, self.left_road + y_adjustments
                    ),
                )
            elif self.direction == "right":
                self.is_flipped = True
                self.rect.midbottom = (
                    0 - self.rect.width,
                    random.randint(
                        self.right_road - y_adjustments, self.right_road + y_adjustments
                    ),
                )

    def animate(self):
        super().update()

    def speed_up(self):
        if not self.hasten:
            self.min_speed = self.min_speed * 1.5
            self.max_speed = self.max_speed * 1.5

            self.min_animation_speed = int(self.min_animation_speed / 1.25)
            self.max_animation_speed = int(self.max_animation_speed / 1.25)

            self.speed_value = random.randint(self.min_speed, self.max_speed)
            self.speed_ratio = (self.speed_value - self.min_speed) / (
                self.max_speed - self.min_speed
            )

            self.animation_scale = self.max_animation_speed - self.min_animation_speed
            self.animation_rate = (
                self.max_animation_speed - (self.animation_scale * self.speed_ratio)
            ) / 100

            self.speed = self.speed_value / self.fps
            self.animate_speed = self.fps * self.animation_rate

            self.hasten = True

    def update(self):
        if self.form == "people":
            if self.main.scene_window.weather.state == "rainfall":
                self.speed_up()

        self.speed_tick += self.speed
        if self.speed_tick >= 1:
            absolute_movement = int(self.speed_tick)
            if self.direction == "left":
                self.rect.x -= absolute_movement
            elif self.direction == "right":
                self.rect.x += absolute_movement

            if self.rect.x <= 0 - self.rect.width and self.direction == "left":
                self.free()
            elif (
                self.rect.x >= self.screen.get_width() + self.rect.width
                and self.direction == "right"
            ):
                self.free()

            self.speed_tick -= absolute_movement

        self.animate()
