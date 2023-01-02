from game.sprite.message import Message
from game.sprite.button import Button

import pygame
import copy


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
        self.force_click = None
        self.closable = None

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
            outline_thickness=2,
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
            outline_thickness=2,
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.975) + self.canvas_rect.y,
            ),
        )

        self.seq_gen = None

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
        v = copy.deepcopy(visible_rect)
        # print(f"visible rect: {v}")

        # assert gw >= v.x + v.w
        # assert gh >= v.y + v.h
        if v.x + v.w > gw:
            delta = (v.x + v.w) - gw
            v.x -= delta

        # north shade
        s1 = pygame.Rect(w(0.0), h(0.0), w(1.0), v.y)
        # print(f"s1: {s1}")

        # south shade
        s2 = pygame.Rect(w(0.0), v.y + v.h, w(1.0), gh - (v.y + v.h))
        # print(f"s2: {s2}")

        # west shade
        s3 = pygame.Rect(w(0.0), v.y, v.x, s2.y - s1.h)
        # print(f"s3: {s3}")

        # east shade
        s4 = pygame.Rect(v.x + v.w, v.y, gw - (v.x + v.w), s3.h)
        # print(f"s4: {s4}\n")

        # center anchor
        vhc = v.x + round(v.w / 2)
        vvc = v.y + round(v.h / 4)
        message_width = round(gw * width)
        if vhc > gw / 2:
            # Box is tend to right
            self.guide_message.top_left_coordinates = (
                v.x - round(message_width * 1.2),  # +20% margin
                vvc,
            )
        else:
            # Box is tend to left
            self.guide_message.top_left_coordinates = (
                v.x + round(message_width * 1.2),  # +20% margin
                vvc,
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
        if not next(self.seq_gen):
            return False

        if len(self.queue) <= 0:
            self.enable = False
            return False

        data = self.queue[0]
        self.set_overlay_boundaries(
            data["rect"],
            data["width"],
        )
        self.force_click = data["force_click"]
        self.closable = data["close_after"]

        self.guide_message.set_message(data["message"])

        del self.queue[0]
        return True

    def sequence_generator(self):
        # Sequence 1-2
        for business in self.main.scene_window.business_data:
            if business["meta"]["name"] == "Street Foods Stall":
                self.queue.append(
                    {
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
                        "force_click": None,
                        "close_after": None,
                        "width": 0.2,
                    }
                )
                yield True
                self.queue.append(
                    {
                        "rect": business["object"].collide_rect,
                        "message": [
                            "You can click each",
                            "businesses to see",
                            "its attributes and",
                            "features.",
                        ],
                        "force_click": business["object"],
                        "close_after": None,
                        "width": 0.2,
                    }
                )
                yield True
                break

        # Sequence 3
        self.queue.append(
            {
                "rect": pygame.Rect(200, 125, 550, 475),
                "message": [
                    "This is the",
                    "business attributes.",
                    "In here, you will",
                    "see how the business",
                    "operation costs",
                    "and how much income",
                    "and sales are ",
                    "calculated",
                    "automatically.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.375,
            }
        )
        yield True

        # Sequence 4
        self.queue.append(
            {
                "rect": pygame.Rect(750, 125, 340, 475),
                "message": [
                    "Here are the buttons",
                    "for you to control  ",
                    "the busines itself. ",
                    "You have different ",
                    "options here to  ",
                    "collect the sales, ",
                    "start the business, ",
                    "hire employees, and ",
                    "lastly to either sell ",
                    "or upgrade the ",
                    "business itself.",
                ],
                "force_click": None,
                "close_after": self.main.scene_window.business_menu,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 5
        self.queue.append(
            {
                "rect": self.main.sliding_menu.sliding_menu_button.rect,
                "message": [
                    "This is the button ",
                    "to view the ",
                    "sliding menu. --->",
                ],
                "force_click": self.main.sliding_menu.sliding_menu_button,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 6
        self.queue.append(
            {
                "rect": self.main.sliding_menu.sliding_menu_rect,
                "message": [
                    "In here, there are  ",
                    "different game ",
                    "features that will ",
                    "help you with your ",
                    "progress. Each one ",
                    "of them contains ",
                    "different functions.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 7
        self.queue.append(
            {
                "rect": self.main.sliding_menu.map_button.rect,
                "message": [
                    "You can visit the ",
                    "region map that ",
                    "contains all the ",
                    "cities you can ",
                    "unlock further in ",
                    "the game by clicking ",
                    "this region button.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 8
        self.queue.append(
            {
                "rect": self.main.sliding_menu.mission_button.rect,
                "message": [
                    "In this menu you ",
                    "will see your daily ",
                    "missions consists ",
                    "of three different ",
                    "tasks you can take ",
                    "each day to maximize ",
                    "your daily income.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 9
        self.queue.append(
            {
                "rect": self.main.sliding_menu.achievement_button.rect,
                "message": [
                    "Your overall game ",
                    "progress will be ",
                    "recorded and can ",
                    "be seen here. Once ",
                    "you reached a major ",
                    "milestone in the ",
                    "game, you can collect ",
                    "the rewards here.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 10
        self.queue.append(
            {
                "rect": self.main.sliding_menu.part_time_button.rect,
                "message": [
                    "You can start working ",
                    "on your daily freelance ",
                    "jobs here. It posts new ",
                    "jobs hourly and the ",
                    "rewards scale as you ",
                    "grow your business ",
                    "and freelance portfolio. ",
                    "It is a great start ",
                    "to the game to ",
                    "puchase your first ",
                    "business!",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 11
        self.queue.append(
            {
                "rect": self.main.sliding_menu.news_button.rect,
                "message": [
                    "The news contains the ",
                    "daily updates to the ",
                    "game and also realtime ",
                    "traffic updates and ",
                    "other updates on the ",
                    "game's different ",
                    "features. ",
                    "Keep an eye on the ",
                    "details in here as ",
                    "they might serve as ",
                    "clues for you to ",
                    "utilize!",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 12
        self.queue.append(
            {
                "rect": self.main.sliding_menu.bank_button.rect,
                "message": [
                    "Banks provide services ",
                    "that will help aid you ",
                    "in the game. You can ",
                    "deposit some of your ",
                    "money in your savings ",
                    "account and let it grow ",
                    "5% monthly, or you can ",
                    "use your business as ",
                    "collateral to borrow ",
                    "money equates to its ",
                    "cost for 5% interest ",
                    "as well.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 13
        self.queue.append(
            {
                "rect": self.main.sliding_menu.stock_button.rect,
                "message": [
                    "Stocks provides an ",
                    "easy to use software ",
                    "that simplifies the ",
                    "process of trading ",
                    "shares of a stock in ",
                    "the market. You can ",
                    "easily purchase and ",
                    "sell shares in an ",
                    "instant using the ",
                    "tool. One great advice ",
                    'for this is to "Buy ',
                    'low, Sell high" ',
                    "strategy. Use it ",
                    "wisely!",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 14
        self.queue.append(
            {
                "rect": self.main.sliding_menu.crypto_button.rect,
                "message": [
                    "Crypto has the same ",
                    "functionality with ",
                    "stocks in all aspects, ",
                    "the only difference is ",
                    "that the price is more ",
                    "volatile and changes ",
                    "every second and ",
                    "resets daily, whereas ",
                    "in stocks it updates ",
                    "once a day and would ",
                    "reset every first day ",
                    "of month. Trade here ",
                    "for lower risk and ",
                    "fast reward strategy.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 15
        self.queue.append(
            {
                "rect": self.main.sliding_menu.setting_button.rect,
                "message": [
                    "Basic game settings ",
                    "can be adjusted here ",
                    "such as the background",
                    "music volume and sound ",
                    "effects volume. Also ",
                    "you can toggle the ",
                    "option to full screen ",
                    "the game.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 17
        self.queue.append(
            {
                "rect": self.main.sliding_menu.main_menu_button.rect,
                "message": [
                    "You can go back to ",
                    "the main menu to ",
                    "restart the game if ",
                    "you do like by ",
                    "pressing this button.",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.2,
            }
        )
        yield True

        # Sequence 17
        self.queue.append(
            {
                "rect": self.main.sliding_menu.information_button.rect,
                "message": [
                    "A more comprehensive ",
                    "tutorial or documentation ",
                    "can be read here. Give ",
                    "it a read everytime you ",
                    "forgot how to play the game",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.25,
            }
        )
        yield True

        # Hacky way to close moving sliding menu
        self.main.sliding_menu.switch_state()

        # Sequence 17
        self.queue.append(
            {
                "rect": self.main.scene_window.profile_holder.rect,
                "message": [
                    "And here is your profile, in the phone you",
                    "can check the time and bank balance but if ",
                    "you click it you will see your overall  ",
                    "statistics in the game.",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "That's all we can share with you, the rest ",
                    "of the game is for you to discover, earn, ",
                    "risk, obtain all the businesses, and finish ",
                    "all the achievements in order to finish ",
                    "the game. ",
                    "",
                    "Good luck!",
                ],
                "force_click": None,
                "close_after": None,
                "width": 0.25,
            }
        )
        yield True

        self.main.data.progress["tutorial_shown"] = True
        self.enable = False
        # End of generator
        while True:
            yield False

    def prologue_sequence(self):
        self.seq_gen = self.sequence_generator()
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
                if self.main.sliding_menu.is_moving:
                    return

                self.main.mixer_buttons_channel.play(
                    self.main.data.music["button_clicked"]
                )
                if self.force_click:
                    self.force_click.force_clicked()
                if self.closable:
                    self.closable.background.enable = False

                if not self._next():
                    self.enable = False

    def update(self):
        if not self.enable:
            return

        self.main.screen.blit(self.shade_1, self.shade_1_size)
        self.main.screen.blit(self.shade_2, self.shade_2_size)
        self.main.screen.blit(self.shade_3, self.shade_3_size)
        self.main.screen.blit(self.shade_4, self.shade_4_size)

        pygame.draw.rect(
            surface=self.main.screen,
            color=self.main.data.colors["white"],
            rect=self.visible_rect,
            width=2,
        )

        self.guide_message.update()
        self.continue_message.update()
