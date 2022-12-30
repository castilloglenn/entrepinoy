import pygame
import random
import copy


class Tracker:
    def __init__(self, main):
        self.main = main

        # Main data
        self.progress = self.main.data.progress
        self.data = self.progress["statistics"]
        self.businesses = self.progress["businesses"]

        # Tracker variables
        self.max_missions = 3
        self.completed_and_notified = []
        self.missions = {
            "business_start": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " Business Minded",
                    "   Start a business.",
                    "   {value}/1",
                ],
                "active": False,
                "value": 0,
                "requirement": 1,
                "reward": 100.0,
            },
            "hire_employee": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " Employer",
                    "   Hire an employee.",
                    "   {value}/1",
                ],
                "active": False,
                "value": 0,
                "requirement": 1,
                "reward": 100.0,
            },
            "serve_customer": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " What can I do for you?",
                    "   Serve 20 customers",
                    "   {value}/20",
                ],
                "active": False,
                "value": 0,
                "requirement": 20,
                "reward": 200.0,
            },
            "serve_manual": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " Hands-on Manager",
                    "   Manually serve 10 customers",
                    "   {value}/10",
                ],
                "active": False,
                "value": 0,
                "requirement": 10,
                "reward": 200.0,
            },
            "earn_pnl": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " Trader's Dream",
                    "   Earn a profit in trading",
                    "   {value}/1",
                ],
                "active": False,
                "value": 0,
                "requirement": 1,
                "reward": 200.0,
            },
            "business_profit": {
                "description": [
                    # 0123456789ABCDEFGHIJ0123456789A
                    " Business is boomin'",
                    "   Earn a profit in business",
                    "   operation. {value}/1",
                ],
                "active": False,
                "value": 0,
                "requirement": 1,
                "reward": 200.0,
            },
        }

        if self.progress["mission"] == {}:
            self.generate_missions()

    def save(self):
        self.main.scene_window.update_data()

    def detect_game_completion(self):
        for achievement in self.progress["achievements"]:
            if not self.progress["achievements"][achievement]["obtained"]:
                return False
        return True

    def generate_missions(self):
        # Collect uncollected rewards
        for mission in self.progress["mission"]:
            if not self.progress["mission"][mission]["active"]:
                continue

            if (
                self.progress["mission"][mission]["value"]
                != self.progress["mission"][mission]["requirement"]
            ):
                continue

            if self.progress["mission"][mission]["reward"] > 0.0:
                self.progress["cash"] += self.progress["mission"][mission]["reward"]

        self.main.data.progress["mission"] = dict()
        missions_selected = []
        for _ in range(self.max_missions):
            mission_selected = random.choice(list(self.missions.keys()))
            while mission_selected in missions_selected:
                mission_selected = random.choice(list(self.missions.keys()))
            missions_selected.append(mission_selected)

            mission_copy = copy.deepcopy(self.missions[mission_selected])
            self.main.data.progress["mission"][mission_selected] = mission_copy

        self.completed_and_notified = []
        self.save()

    def notify_success(self, mission_title: str, title="Mission"):
        if mission_title in self.completed_and_notified:
            return

        self.main.mixer_notifications_channel.play(self.main.data.music["success"])
        message = [
            f"{title} Completed:",
            f"{mission_title.strip()}",
            f"",
            f"Please collect",
            f"your reward.",
        ]
        self.main.response_menu.queue_message(message)
        self.completed_and_notified.append(mission_title)

    # Increment statistics data
    def increment_tracker(self, name, increment=None):
        if name in self.progress["mission"]:
            if self.progress["mission"][name]["active"]:
                self.progress["mission"][name]["value"] = min(
                    self.progress["mission"][name]["value"] + 1,
                    self.progress["mission"][name]["requirement"],
                )

                if (
                    self.progress["mission"][name]["value"]
                    == self.progress["mission"][name]["requirement"]
                    and self.progress["mission"][name]["reward"] > 0.0
                ):
                    self.notify_success(
                        self.progress["mission"][name]["description"][0]
                    )

        if name in self.progress["statistics"]:
            if increment:
                self.data[name] += increment
            else:
                self.data[name] += 1

        if name in self.progress["achievements"]:
            if not self.progress["achievements"][name]["obtained"]:
                increase = increment if increment else 1
                self.progress["achievements"][name]["value"] = min(
                    self.progress["achievements"][name]["value"] + increase,
                    self.progress["achievements"][name]["requirement"],
                )

                if (
                    self.progress["achievements"][name]["value"]
                    >= self.progress["achievements"][name]["requirement"]
                    and self.progress["achievements"][name]["reward"] > 0.0
                ):
                    self.notify_success(
                        self.main.data.progress["achievements"][name]["description"][0],
                        title="Achievement",
                    )

    def add_click(self):
        self.data["clicks"] += 1

    # Calculate statistics
    def get_business_owned_count(self):
        owned = 0
        total = 0

        unincluded_location = ["test_location"]
        unincluded_business = ["last_visited"]

        for location in self.businesses:
            if location in unincluded_location:
                continue

            for business in self.businesses[location]:
                if business in unincluded_business:
                    continue

                total += 1
                if self.businesses[location][business]["ownership"]:
                    owned += 1

        return owned, total
