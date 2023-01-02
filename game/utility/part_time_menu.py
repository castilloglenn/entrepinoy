from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

from datetime import datetime
import pygame
import random
import re


class PartTimeMenu(GenericMenu):
    """
    Menu showing the available part time jobs and their UI's as well.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress["part_time"]
        self.word_pool = self.main.data.word_pool

        self.TAB_OVERVIEW = 0
        self.TAB_GAME_TYPING_TEST = 1
        self.TAB_ACTIVE = self.TAB_OVERVIEW

        self.time_started = None
        self.time_ended = None

        self.word_set = None
        self.word_set_index = None
        self.word_set_size = None
        self.word_letters_sum = None

        self.word_written = None
        self.max_length = None

        self.key_press_count = None
        self.inaccuracies = None
        self.wpm = None
        self.accuracy = None
        self.awpm = None

        self.FEEDBACK_IDLE = "System feedback: "
        self.FEEDBACK_UNSUCCESSFUL = self.FEEDBACK_IDLE + "Incorrect data! Rejected."
        self.FEEDBACK_SUCCESSFUL = self.FEEDBACK_IDLE + "Data successfully uploaded!"
        self.FEEDBACK_STATE = self.FEEDBACK_IDLE

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["", "", "               Freelance Jobs"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.available_message = Message(
            self.screen,
            ["Current Job Available"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.4) + self.canvas_rect.y,
            ),
        )
        self.job_message = Message(
            self.screen,
            ["Data Encoder"],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.5) + self.canvas_rect.y,
            ),
        )
        self.unavailable_message = Message(
            self.screen,
            ["Available once daily. Refresh every hour."],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.65) + self.canvas_rect.y,
            ),
        )
        self.available_button = Button(
            self.main,
            self._available_button_callback,
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.65) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["start_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "start_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "start_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Start working on the job",
                ],
            },
        )

        self.instruction_message = Message(
            self.screen,
            [
                "Type the word shown below then press Enter in order",
                "to upload it in the client's database:",
            ],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.125) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.15) + self.canvas_rect.y,
            ),
        )
        self.guide_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.125) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.236) + self.canvas_rect.y,
            ),
        )
        self.written_message = Message(
            self.screen,
            [self.word_written],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.125) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.36) + self.canvas_rect.y,
            ),
        )
        self.feedback_message = Message(
            self.screen,
            [self.FEEDBACK_IDLE],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.125) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.52) + self.canvas_rect.y,
            ),
        )
        self.statistic_message = Message(
            self.screen,
            [""],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.125) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.6) + self.canvas_rect.y,
            ),
        )

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    def _available_button_callback(self, args):
        self._generate_words()

        self.TAB_ACTIVE = self.TAB_GAME_TYPING_TEST
        self.set_data()

    def _generate_words(self):
        self.word_set = []
        for _ in range(self.word_set_size):
            size_set = random.choice(list(self.word_pool.keys()))
            word = random.choice(self.word_pool[size_set]).upper()
            self.word_letters_sum += len(word)
            self.word_set.append(word)

    def _check_written_word(self):
        if self.word_written == self.word_set[self.word_set_index]:
            self.word_set_index += 1
            self.FEEDBACK_STATE = self.FEEDBACK_SUCCESSFUL
            self.word_written = ""

            if self.word_set_index >= self.word_set_size:
                self.word_set_index = self.word_set_size - 1
                self._calculate_score()
        else:
            self.FEEDBACK_STATE = self.FEEDBACK_UNSUCCESSFUL

    def _calculate_wpm(self):
        self.current_time = datetime.now()
        self.delta = self.current_time - self.time_started
        self.minutes = max(self.delta.seconds / 60, 0.1)
        self.wpm = round((self.key_press_count / 5) / self.minutes, 1)

        self.inaccurate_perc = self.inaccuracies / self.key_press_count
        self.accuracy = round((1 - self.inaccurate_perc) * 100, 1)

        self.awpm = round(self.wpm * (self.accuracy / 100), 1)

    def _calculate_score(self):
        self._calculate_wpm()

        span = self.delta.seconds
        accuracy = self.accuracy
        awpm = self.awpm

        base_pay_per_letter = 2.0 + len(
            self.main.data.progress["statistics"]["business_owned"]
        )
        bonus_thresholds = {
            "job_span": [40, 50, 60],
            "accuracy": [98, 95, 90],
            "awpm": [60, 50, 40],
        }
        bonus_weights = {
            "job_span": 0.1,
            "accuracy": 0.2,
            "awpm": 0.2,
        }

        base_pay = self.word_letters_sum * base_pay_per_letter

        span_bonus = 0.0
        for index, reach in enumerate(bonus_thresholds["job_span"]):
            if span <= reach:
                threshold_length = len(bonus_thresholds["job_span"])
                tier = (threshold_length - index) / threshold_length
                weight = bonus_weights["job_span"]
                bonus_perc = weight * tier
                span_bonus = base_pay * bonus_perc
                break

        accuracy_bonus = 0.0
        for index, reach in enumerate(bonus_thresholds["accuracy"]):
            if accuracy >= reach:
                threshold_length = len(bonus_thresholds["accuracy"])
                tier = (threshold_length - index) / threshold_length
                weight = bonus_weights["accuracy"]
                bonus_perc = weight * tier
                accuracy_bonus = base_pay * bonus_perc
                break

        awpm_bonus = 0.0
        for index, reach in enumerate(bonus_thresholds["awpm"]):
            if awpm >= reach:
                threshold_length = len(bonus_thresholds["awpm"])
                tier = (threshold_length - index) / threshold_length
                weight = bonus_weights["awpm"]
                bonus_perc = weight * tier
                awpm_bonus = base_pay * bonus_perc
                break

        total_pay = base_pay + span_bonus + accuracy_bonus + awpm_bonus

        # Tracker
        self.main.tracker.increment_tracker(
            "part_time_income",
            increment=total_pay,
        )

        self.main.response_menu.queue_message(
            [
                f"P{base_pay:,.2f} : Base Pay",
                f"P{span_bonus:,.2f} : Speed {span:,d} sec",
                f"P{accuracy_bonus:,.2f} : Accuracy {accuracy:,.0f}%",
                f"P{awpm_bonus:,.2f} : AWPM {awpm:,.0f} words",
                f"P{total_pay:,.2f} : Total Pay",
            ],
            alignment="left",
        )
        self.main.data.progress["cash"] += total_pay
        self.data["available"] = False

        self.main.scene_window.update_data()
        self.TAB_ACTIVE = self.TAB_OVERVIEW
        self.set_data()

    # Abstract method implementation
    def set_button_states(self):
        if self.TAB_ACTIVE == self.TAB_OVERVIEW:
            if self.data["available"]:
                self.available_button.visible = True
                self.unavailable_message.visible = False
            else:
                self.unavailable_message.visible = True
                self.available_button.visible = False

        elif self.TAB_ACTIVE == self.TAB_GAME_TYPING_TEST:
            ...

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        if self.TAB_ACTIVE == self.TAB_OVERVIEW:
            ...

        elif self.TAB_ACTIVE == self.TAB_GAME_TYPING_TEST:
            gap = self.max_length - len(self.word_written)
            self.guide_message.set_message([self.word_set[self.word_set_index]])
            self.written_message.set_message([self.word_written + ("_" * gap)])
            self.feedback_message.set_message([self.FEEDBACK_STATE])

            if not self.time_started:
                self.statistic_message.set_message(
                    [
                        "The system will start tracking your actions as soon",
                        "as you press a key.",
                    ],
                )
            else:
                self._calculate_wpm()
                self.statistic_message.set_message(
                    [
                        f"Time Started: {self.delta.seconds:,d} seconds ago...",
                        "",
                        f"Data index: {self.word_set_index + 1:,d}/{self.word_set_size:,d}",
                        f"Key Progress: {self.key_press_count - self.inaccuracies:,d}/{self.word_letters_sum:,d}",
                        f"Words Per Minute: {self.wpm}",
                        f"Accuracy: {self.accuracy}%",
                        f"Adjusted Words Per Minute Rating: {self.awpm}",
                    ],
                )

        self.set_button_states()

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        if self.TAB_ACTIVE == self.TAB_OVERVIEW:
            self.time_started = None
            self.time_ended = None

            self.word_set = []
            self.word_set_index = 0
            self.word_set_size = 20
            self.word_letters_sum = 0

            self.word_written = ""
            self.max_length = max([int(size) for size in self.word_pool])

            self.key_press_count = 0
            self.inaccuracies = 0
            self.wpm = 0
            self.accuracy = 0.0
            self.awpm = 0.0

            self.FEEDBACK_STATE = self.FEEDBACK_IDLE

            self.title_message.add(self.objects)
            self.available_message.add(self.objects)
            self.job_message.add(self.objects)

            self.available_button.add(
                self.objects,
                self.buttons,
                self.hoverable_buttons,
                self.tooltips,
            )
            self.unavailable_message.add(self.objects)

        elif self.TAB_ACTIVE == self.TAB_GAME_TYPING_TEST:
            self.instruction_message.add(self.objects)
            self.guide_message.add(self.objects)
            self.written_message.add(self.objects)
            self.feedback_message.add(self.objects)
            self.statistic_message.add(self.objects)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type != pygame.KEYDOWN:
            return

        if self.TAB_ACTIVE != self.TAB_GAME_TYPING_TEST:
            return

        if event.key == pygame.K_BACKSPACE:
            if len(self.word_written) > 0:
                self.word_written = self.word_written[:-1]
            return

        if event.key == pygame.K_RETURN:
            self._check_written_word()
            return
        else:
            self.FEEDBACK_STATE = self.FEEDBACK_IDLE

        if len(self.word_written) >= self.max_length:
            return

        # Statistics logging
        self.key_press_count += 1
        if not self.time_started:
            self.time_started = datetime.now()

        char = list(event.unicode)
        if len(char) == 1:
            self.word_written += char[0]

        """Source (Modified): https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
        Explanation: Need to extract alphanumeric values only from a string"""
        self.word_written = re.sub(r"\W+", "", self.word_written.upper())

        if not self.word_set[self.word_set_index].startswith(self.word_written):
            self.inaccuracies += 1
