import pygame
from pygame.sprite import Sprite
from pygame import Surface
from pygame import Rect

from game.sprite.message import Message


class Button(Sprite):
    """
    Base class for constructing basic buttons with functionality and different
    states when hovered.
    """

    def __init__(
        self,
        main,
        callback_function,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
        collide_rect: tuple[float] = None,
        button_ratio: float = None,
        **states
    ):
        """
        Button interface to construct a hoverable button with function.

        Args:
            screen (pygame.Surface): The screen in which the button will appear onto
            callback_function (function): Python function to run when the button is clicked
            top_left_coordinates (_type_, optional): x and y coordinates for the top-left of the button. Defaults to None.. Defaults to None.
            center_coordinates (tuple, optional): x and y coordinates for the center of the button. Defaults to None.. Defaults to None.
            collide_rect (tuple[float], optional): relative percentage of the box where it is hoverable.
                may input in percentages, (0.5, 0.5) means 50% smaller box is the hoverable range of the
                button/background. Defaults to None.
        """
        super().__init__()

        # Debugging
        self.show_bound = False
        self.bound_color = (255, 255, 255)
        self.bound_opacity = 128

        # SFX Variables
        self.hovered_sfx_played = False

        self.visible = True
        self.main = main
        self.state = "idle"
        self.callback = callback_function
        self.button_ratio = button_ratio

        self.idle = states["idle"].convert_alpha()
        self.has_tooltip = False
        self.tooltip = None
        self.tooltip_display_gap = 30
        self.previous_mouse_location = (-1, -1)

        if self.button_ratio is not None:
            self.width = int(self.idle.get_rect().width * button_ratio)
            self.height = int(self.idle.get_rect().height * button_ratio)
            self.idle = self.resize_button(self.idle)

        if "hovered" in states:
            self.hovered = self.resize_button(states["hovered"].convert_alpha())
        else:
            self.hovered = self.resize_button(states["idle"].convert_alpha())
            self.outline = self.resize_button(states["outline"].convert_alpha())
            self.hovered.blit(self.outline, (0, 0))

        if "disabled" in states:
            self.disabled = self.resize_button(states["disabled"].convert_alpha())

        if "tooltip" in states:
            self.has_tooltip = True
            self.set_tooltip(states["tooltip"])

        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.collide_rect = None

        if self.top_left_coordinates != None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates != None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates != None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)

        self.x_coordinate_offset = 0

        # Collide rect refers to the inner rectangle of the button to where
        #   specifically the triggers function inside the box, this avoids
        #   triggering hover and callback function when targeting the transparent
        #   points inside the button/background
        self.collide_rect_rel = collide_rect
        if collide_rect == None:
            self.collide_rect_rel = (0, 0, 1, 1)

        self.collide_x = self.rect.x + self.rect.width * self.collide_rect_rel[0]
        self.collide_y = self.rect.y + self.rect.height * self.collide_rect_rel[1]
        self.collide_width = self.rect.width * self.collide_rect_rel[2]
        self.collide_height = self.rect.height * self.collide_rect_rel[3]

        # Screen surface (for displaying hitbox)
        self.hitbox = Surface((self.collide_width, self.collide_height))
        self.hitbox.fill(self.bound_color)
        self.hitbox.convert_alpha()
        self.hitbox.set_alpha(self.bound_opacity)

        self.set_image_and_rect()

    def reconstruct(
        self,
        main,
        callback_function,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
        collide_rect: tuple[float] = None,
        button_ratio: float = None,
        **states
    ):
        self.main = main
        self.callback = callback_function
        self.idle = states["idle"].convert_alpha()
        self.button_ratio = button_ratio

        if self.button_ratio != None:
            self.width = int(self.idle.get_rect().width * button_ratio)
            self.height = int(self.idle.get_rect().height * button_ratio)

        if "hovered" in states:
            self.hovered = self.resize_button(states["hovered"].convert_alpha())
        else:
            self.hovered = self.resize_button(states["idle"].convert_alpha())
            self.outline = self.resize_button(states["outline"].convert_alpha())
            self.hovered.blit(self.outline, (0, 0))

        if "disabled" in states:
            self.disabled = self.resize_button(states["disabled"].convert_alpha())

        if "tooltip" in states:
            self.has_tooltip = True
            self.previous_mouse_location = None
            self.set_tooltip(states["tooltip"])

        self.top_left_coordinates = top_left_coordinates
        self.center_coordinates = center_coordinates
        self.midbottom_coordinates = midbottom_coordinates

        self.image = self.idle
        self.rect = self.image.get_rect()
        self.collide_rect = None

        if self.top_left_coordinates != None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates != None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates != None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)

        self.x_coordinate_offset = 0

        self.collide_rect_rel = collide_rect
        if collide_rect == None:
            self.collide_rect_rel = (0, 0, 1, 1)

        self.collide_x = self.rect.x + self.rect.width * self.collide_rect_rel[0]
        self.collide_y = self.rect.y + self.rect.height * self.collide_rect_rel[1]
        self.collide_width = self.rect.width * self.collide_rect_rel[2]
        self.collide_height = self.rect.height * self.collide_rect_rel[3]

        # Screen surface (for displaying hitbox)
        self.hitbox = Surface((self.collide_width, self.collide_height))
        self.hitbox.fill(self.bound_color)
        self.hitbox.convert_alpha()
        self.hitbox.set_alpha(self.bound_opacity)

        self.set_image_and_rect()

    def resize_button(self, surface) -> Surface:
        if self.button_ratio is not None:
            return pygame.transform.scale(
                surface, (self.width, self.height)
            ).convert_alpha()
        return surface

    def update(self):
        if self.visible:
            self.collide_x = self.rect.x + self.rect.width * self.collide_rect_rel[0]
            self.collide_y = self.rect.y + self.rect.height * self.collide_rect_rel[1]
            self.main.screen.blit(self.image, self.rect)

            if self.show_bound:
                self.main.screen.blit(self.hitbox, (self.collide_x, self.collide_y))

    def display_tooltips(self):
        if self.visible and self.state == "hovered" and self.has_tooltip:
            self.display_location = (
                self.previous_mouse_location[0],
                self.previous_mouse_location[1] + self.tooltip_display_gap,
            )

            self.tooltip.mid_bottom_coordinates = self.display_location
            self.tooltip.update()

    def set_image_and_rect(self):
        if self.state == "disabled":
            self.image = self.disabled
        elif self.state == "idle":
            self.image = self.idle
        elif self.state == "hovered":
            self.image = self.hovered

        self.update_rect()

    def update_rect(self):
        self.rect = self.image.get_rect()
        if self.top_left_coordinates is not None:
            self.rect.topleft = self.top_left_coordinates
        elif self.center_coordinates is not None:
            self.rect.center = self.center_coordinates
        elif self.midbottom_coordinates is not None:
            self.rect.midbottom = self.midbottom_coordinates
        else:
            self.rect.topleft = (0, 0)

        self.rect.x += self.x_coordinate_offset

        self.collide_rect = Rect(
            self.collide_x, self.collide_y, self.collide_width, self.collide_height
        )

    def set_disabled(self, is_disabled):
        if is_disabled:
            self.state = "disabled"
            self.set_image_and_rect()
        else:
            self.state = "idle"
            self.check_hovered(self.previous_mouse_location)

    def set_callback(self, new_callback):
        self.callback = new_callback

    def set_tooltip(self, tooltip):
        if self.tooltip == None:
            self.tooltip = Message(
                self.main.screen,
                tooltip,
                self.main.data.medium_font,
                self.main.data.colors["white"],
                outline_thickness=2,
            )
        else:
            self.tooltip.set_message(tooltip)

    def check_hovered(self, hover_coordinates):
        # Return booleans to prevent overlapping buttons to react the same
        self.previous_mouse_location = hover_coordinates
        if self.state == "disabled" or not self.visible:
            return False

        if self.collide_rect.collidepoint(hover_coordinates):
            self.play_sound("button_hovered")
            self.state = "hovered"
            self.set_image_and_rect()
            return True
        else:
            self.state = "idle"
            self.set_image_and_rect()
            self.hovered_sfx_played = False
            return False

    def check_clicked(self, click_coordinates):
        if self.state == "disabled" or not self.visible:
            return False

        if self.collide_rect.collidepoint(click_coordinates) and self.visible:
            self.play_sound("button_clicked")
            self.force_clicked()

            # Return booleans to prevent overlapping buttons to react the same
            return True
        return False

    def force_clicked(self):
        self.state = "idle"
        self.set_image_and_rect()
        self.callback(self)

    def play_sound(self, sfx_name):
        if sfx_name == "button_hovered":
            if not self.hovered_sfx_played:
                self.main.mixer_buttons_channel.play(self.main.data.music[sfx_name])
                self.hovered_sfx_played = True
        elif sfx_name == "button_clicked":
            self.main.mixer_buttons_channel.play(self.main.data.music[sfx_name])
