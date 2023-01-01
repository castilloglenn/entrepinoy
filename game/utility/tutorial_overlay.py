from game.sprite.message import Message
from game.sprite.button import Button

import pygame


class TutorialOverlay:
    """
    Class to include an overlay to the game that teaches certain aspects on how
    the game shall be played.
    """

    def __init__(self, main) -> None:
        self.main = main
        self.canvas_rect = self.main.display_surface.get_rect()

        self.enable = False
        self.overlay_alpha = 128
        self.queue = []
        self.executable = None

        self.QUEUE_GUIDE = 0  # Texts highlights only
        self.QUEUE_BUTTON = 1  # With outside callbacks

        # Make this separate message in the lower center of the screen
        self.continue_message = "(Click anywhere to continue)"

        self.visible_rect: pygame.Rect = None

        self.shade_1: pygame.Surface = None
        self.shade_1_size: pygame.Rect = None

        self.shade_2: pygame.Surface = None
        self.shade_2_size: pygame.Rect = None

        self.shade_3: pygame.Surface = None
        self.shade_3_size: pygame.Rect = None

        self.shade_4: pygame.Surface = None
        self.shade_4_size: pygame.Rect = None

        self.guide_message = Message(
            self.main.screen,
            [""],
            self.main.data.medium_font,
            self.main.data.colors["white"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.5) + self.canvas_rect.y,
            ),
        )
        self.guide_message.alignment = "left"
        self.continue_message = Message(
            self.main.screen,
            ["(Click anywhere to continue)"],
            self.main.data.medium_font,
            self.main.data.colors["white"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.85) + self.canvas_rect.y,
            ),
        )

    def set_overlay_boundaries(self, visible_rect: pygame.Rect, width: int):
        # Message should be automatically placed somewhere
        gw = self.main.data.setting["game_width"]
        gh = self.main.data.setting["game_height"]

        def w(size):
            """Relative width"""
            return round(gw * size)

        def h(size):
            """Relative height"""
            return round(gh * size)

        self.visible_rect = visible_rect
        v = visible_rect

        # assert gw >= v.x + v.w
        # assert gh >= v.y + v.h

        # north shade
        s1 = pygame.Rect(w(0.0), h(0.0), w(1.0), v.y)

        # south shade
        s2 = pygame.Rect(w(0.0), v.y + v.h, w(1.0), gh - (v.y + v.h))

        # west shade
        s3 = pygame.Rect(w(0.0), v.y, v.x, s2.y - s1.h)

        # east shade
        s4 = pygame.Rect(v.x + v.w, v.y, gw - (v.x + v.w), s3.h)

        # center anchor
        vc = v.x + round(v.w / 2)
        message_width = round(gw * width)
        if vc > gw / 2:
            # Box is tend to right
            self.guide_message.top_left_coordinates = (
                v.x - round(message_width * 1.2),  # +20% margin
                v.y,
            )
        else:
            # Box is tend to left
            self.guide_message.top_left_coordinates = (
                v.x + round(message_width * 1.2),  # +20% margin
                v.y,
            )

        # assert s1.h + s3.h + s2.h == gh
        # assert s1.h + v.h + s2.h == gh
        # assert s1.h + s4.h + s2.h == gh
        # assert s3.w + v.w + s4.w == gw

        self.shade_1 = pygame.Surface((s1.w, s1.h))
        self.shade_1.fill(self.main.data.colors["black"])
        self.shade_1.convert_alpha()
        self.shade_1.set_alpha(self.overlay_alpha)
        self.shade_1_size = s1

        self.shade_2 = pygame.Surface((s2.w, s2.h))
        self.shade_2.fill(self.main.data.colors["black"])
        self.shade_2.convert_alpha()
        self.shade_2.set_alpha(self.overlay_alpha)
        self.shade_2_size = s2

        self.shade_3 = pygame.Surface((s3.w, s3.h))
        self.shade_3.fill(self.main.data.colors["black"])
        self.shade_3.convert_alpha()
        self.shade_3.set_alpha(self.overlay_alpha)
        self.shade_3_size = s3

        self.shade_4 = pygame.Surface((s4.w, s4.h))
        self.shade_4.fill(self.main.data.colors["black"])
        self.shade_4.convert_alpha()
        self.shade_4.set_alpha(self.overlay_alpha)
        self.shade_4_size = s4

    def _next(self):
        if len(self.queue) <= 0:
            self.enable = False
            return

        data = self.queue[0]
        if data["type"] == self.QUEUE_GUIDE:
            self.set_overlay_boundaries(data["rect"], data["width"])
            self.executable = None
        elif data["type"] == self.QUEUE_BUTTON:
            self.set_overlay_boundaries(data["button"].collide_rect, data["width"])
            self.executable = data["button"]

        self.guide_message.set_message(data["message"])

        del self.queue[0]

    def prologue_sequence(self):
        # Sequence 1-2
        for business in self.main.scene_window.business_data:
            if business["meta"]["name"] == "Street Foods Stall":
                self.queue.append(
                    {
                        "type": self.QUEUE_GUIDE,
                        "rect": business["object"].collide_rect,
                        "message": [
                            "Welcome to EntrePinoy,",
                            "This is the business you have chosen,",
                            "You don't own it currently, but you will, soon.",
                            "",
                            "In this tutorial, we will show you the features",
                            "of the game and what each modules do in order to",
                            "successfully complete the game, and learn many",
                            "things about business and handling money and assets!",
                        ],
                        "width": 0.2,
                    }
                )
                self.queue.append(
                    {
                        "type": self.QUEUE_BUTTON,
                        "button": business["object"],
                        "message": [
                            "Click the street food business to see ",
                            "its attributes and features.",
                        ],
                        "width": 0.2,
                    }
                )
                break

        self._next()
        self.enable = True

    def handle_event(self, event):
        if not self.enable:
            return

        if event.type == pygame.QUIT:
            # Closing the game properly
            self.main.close_game()

        # If the user clicked on left mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.executable:
                    self.executable.force_clicked()
                self._next()

    def update(self):
        if not self.enable:
            return

        self.main.screen.blit(self.shade_1, self.shade_1_size)
        self.main.screen.blit(self.shade_2, self.shade_2_size)
        self.main.screen.blit(self.shade_3, self.shade_3_size)
        self.main.screen.blit(self.shade_4, self.shade_4_size)

        self.guide_message.update()
        self.continue_message.update()
