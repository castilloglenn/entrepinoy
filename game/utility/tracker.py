import pygame
import random


class Tracker:
    def __init__(self, main):
        self.main = main

        # Main data
        self.progress = self.main.data.progress
        self.data = self.progress["statistics"]
        self.businesses = self.progress["businesses"]

        # Tracker variables
        self.max_missions = 3
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
        }

        if self.progress["mission"] == {}:
            self.generate_missions()

    def save(self):
        self.main.scene_window.update_data()

    def generate_missions(self):
        self.main.data.progress["mission"] = {}
        self.save()

        missions_selected = []
        for _ in range(self.max_missions):
            mission_selected = random.choice(list(self.missions.keys()))
            while mission_selected in missions_selected:
                mission_selected = random.choice(list(self.missions.keys()))
            missions_selected.append(mission_selected)

            self.main.data.progress["mission"][mission_selected] = self.missions[
                mission_selected
            ]
        self.save()

    # Increment statistics data
    def increment_tracker(self, name, increment=None):
        if name in self.progress["mission"]:
            if self.progress["mission"][name]["active"]:
                self.progress["mission"][name]["value"] = min(
                    self.progress["mission"][name]["value"] + 1,
                    self.progress["mission"][name]["requirement"],
                )

        if name in self.progress["statistics"]:
            if increment:
                self.data[name] += increment
            else:
                self.data[name] += 1

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
