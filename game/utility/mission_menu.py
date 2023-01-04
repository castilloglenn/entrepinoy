from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

import pygame


class MissionMenu(GenericMenu):
    """
    Menu showing the missions with rewards that can be picked up for the day.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress["mission"]

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["               Daily Missions"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.mission_message = Message(
            self.screen,
            [
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
                "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            ],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.17) + self.canvas_rect.y,
            ),
        )
        self.mission_1_start_button = Button(
            self.main,
            self._start_mission_1,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.29) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["start_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "start_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "start_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_2_start_button = Button(
            self.main,
            self._start_mission_2,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.495) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["start_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "start_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "start_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_3_start_button = Button(
            self.main,
            self._start_mission_3,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.705) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["start_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "start_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "start_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_1_collect_button = Button(
            self.main,
            self._collect_mission_1,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.29) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_2_collect_button = Button(
            self.main,
            self._collect_mission_2,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.495) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )
        self.mission_3_collect_button = Button(
            self.main,
            self._collect_mission_3,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.705) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "collect_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "collect_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "collect_button_disabled"
                ].convert_alpha(),
            },
        )

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    def _notify_success(self, reward):
        assert isinstance(reward, float)
        self.main.response_menu.queue_message(
            [
                f"",
                f"You have received the",
                f"reward amounting to",
                f"P{reward:,.2f}",
                f"",
            ]
        )

    def _start_mission_1(self, args):
        mission_1 = list(self.data.keys())[0]
        self.main.data.progress["mission"][mission_1]["active"] = True

    def _collect_mission_1(self, args):
        mission_1 = list(self.data.keys())[0]
        reward = self.data[mission_1]["reward"]
        self.main.data.progress["cash"] += reward
        self._notify_success(reward=reward)
        self.main.data.progress["mission"][mission_1]["reward"] = 0.0
        self.main.play_random_coin_sfx()

    def _start_mission_2(self, args):
        mission_2 = list(self.data.keys())[1]
        self.main.data.progress["mission"][mission_2]["active"] = True

    def _collect_mission_2(self, args):
        mission_2 = list(self.data.keys())[1]
        reward = self.data[mission_2]["reward"]
        self.main.data.progress["cash"] += reward
        self._notify_success(reward=reward)
        self.main.data.progress["mission"][mission_2]["reward"] = 0.0
        self.main.play_random_coin_sfx()

    def _start_mission_3(self, args):
        mission_3 = list(self.data.keys())[2]
        self.main.data.progress["mission"][mission_3]["active"] = True

    def _collect_mission_3(self, args):
        mission_3 = list(self.data.keys())[2]
        reward = self.data[mission_3]["reward"]
        self.main.data.progress["cash"] += reward
        self._notify_success(reward=reward)
        self.main.data.progress["mission"][mission_3]["reward"] = 0.0
        self.main.play_random_coin_sfx()

    # Abstract method implementation
    def set_button_states(self):
        self.data = self.main.data.progress["mission"]
        missions = list(self.data.keys())

        mission_1 = self.data[missions[0]]
        if mission_1["active"]:
            self.mission_1_start_button.visible = False
            self.mission_1_collect_button.visible = True
            if (
                mission_1["value"] == mission_1["requirement"]
                and mission_1["reward"] > 0.0
            ):
                self.mission_1_collect_button.set_disabled(False)
            else:
                self.mission_1_collect_button.set_disabled(True)
        else:
            self.mission_1_start_button.visible = True
            self.mission_1_collect_button.visible = False
            self.mission_1_collect_button.set_disabled(True)

        mission_2 = self.data[missions[1]]
        if mission_2["active"]:
            self.mission_2_start_button.visible = False
            self.mission_2_collect_button.visible = True
            if (
                mission_2["value"] == mission_2["requirement"]
                and mission_2["reward"] > 0.0
            ):
                self.mission_2_collect_button.set_disabled(False)
            else:
                self.mission_2_collect_button.set_disabled(True)
        else:
            self.mission_2_start_button.visible = True
            self.mission_2_collect_button.visible = False
            self.mission_2_collect_button.set_disabled(True)

        mission_3 = self.data[missions[2]]
        if mission_3["active"]:
            self.mission_3_start_button.visible = False
            self.mission_3_collect_button.visible = True
            if (
                mission_3["value"] == mission_3["requirement"]
                and mission_3["reward"] > 0.0
            ):
                self.mission_3_collect_button.set_disabled(False)
            else:
                self.mission_3_collect_button.set_disabled(True)
        else:
            self.mission_3_start_button.visible = True
            self.mission_3_collect_button.visible = False
            self.mission_3_collect_button.set_disabled(True)

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        self.data = self.main.data.progress["mission"]
        message = [
            "              Resets every 12AM.",
            "============================================================",
        ]
        for mission in self.data:
            mission_desc = self.data[mission]["description"][:2]
            progress = self.data[mission]["description"][2].format(
                value=self.data[mission]["value"]
            )
            mission_desc.append(progress)

            message += mission_desc
            message.append(
                "============================================================"
            )

        self.mission_message.set_message(message)
        self.set_button_states()

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.mission_message.add(self.objects)

        self.mission_1_start_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_2_start_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_3_start_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.mission_1_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_2_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.mission_3_collect_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.set_button_states()
