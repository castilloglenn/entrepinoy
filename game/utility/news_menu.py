from game.sprite.message import Message
from game.sprite.button import Button

from game.utility.generic_menu import GenericMenu

from datetime import datetime
import pygame
import random


class NewsMenu(GenericMenu):
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
        self.data = self.main.data.progress
        self.calendars = self.main.data.calendars

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["                 Daily News"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.news_message = Message(
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

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    # ...

    # Abstract method implementation
    def set_button_states(self):
        ...

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        max_width = 45
        max_height = 14
        message = []

        # Line 1
        date = self.data["time"]
        date_object = datetime.strptime(date, self.main.scene_window.time.format)
        day_of_month = int(date_object.strftime("%d"))
        header_date = date_object.strftime(f"%A, %B {day_of_month}, %Y")
        message.append(f"{header_date}")

        # Line 2
        hour = date_object.hour
        greeting = "Evening"
        if hour <= 11:
            greeting = "Morning"
        elif hour <= 17:
            greeting = "Afternoon"
        location = self.main.data.city[self.data["last_location"]]
        message.append(f"Good {greeting}, {location}!")

        # Line 3
        message.append("Events and Latest Traffic")

        # Line 4
        holiday = self.main.scene_window.holiday

        if holiday != "":
            # Guide        "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
            message.append(f"  Its Holiday! {holiday[:30]}")
        else:
            message.append(f"  Today is a regular day")

        # Line 5
        crowd_chance = self.main.scene_window.crowd_chance[
            self.main.scene_window.time.time.hour
        ]
        if crowd_chance <= 30:
            message.append(f"  Quite few people passes the streets")
        elif crowd_chance <= 60:
            message.append(f"  The streets are busy.")
        else:
            message.append(f"  Rush hour can be observed down the road")

        # Line 6
        message.append("Finance and Economy")

        # Line 7
        bank = self.data["bank"]
        if bank["loan"] > 0.0:
            message.append(f"  Remember to save some for loan payments!")
        elif bank["balance"] == 0.0:
            message.append(f"  Deposit now to utilize bank interest")
        else:
            message.append(f"  Short on budget? Loan at the bank!")

        # Line 8
        part_time = self.data["part_time"]
        if part_time["available"]:
            message.append(f"  Wanted freelancers to do data encoding.")
        else:
            message.append(f"  More job opportunities tomorrow.")

        # Line 9
        # Guide        "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        missions = self.data["mission"]
        uncollected_missions = 0
        for mission in missions:
            if missions[mission]["reward"] > 0.0:
                uncollected_missions += 1

        if uncollected_missions:
            message.append("  Local citizens must do missions daily.")
        else:
            message.append("  Plan out your strategy tomorrow, citizen!")

        # Line 10
        message.append("Global News")

        # Line 11
        crypto = self.data["crypto"]
        name = crypto["symbol"]
        change = crypto["price"] / crypto["starting_price"] * 100
        if change > 120:
            message.append(f"  {name} skyrockets to the moon!")
        elif change < 80:
            message.append(f"  {name} plummets to the floor.")
        else:
            message.append(f"  Start trading with {name}, not an ad.")

        # Line 12
        stock = self.data["stocks"]
        name = stock["symbol"]
        change = stock["price"] / stock["starting_price"] * 100
        if change > 110:
            message.append(f"  Business is boomin' with {name}")
        elif change < 90:
            message.append(f"  {name} is unstable in terms of money.")
        else:
            message.append(f"  Get a hold of {name} shares long term!")

        # Line 13
        message.append("Tourism")

        # Line 14
        # Guide            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        if self.main.data.city[self.data["last_location"]] == "IMUS":
            message.append("  Imus longganisa is the best longganisa.")
        elif self.main.data.city[self.data["last_location"]] == "BACOOR":
            message.append("  Have you tried Digman's Halo-halo in Bacoor?")
        elif self.main.data.city[self.data["last_location"]] == "MOLINO":
            message.append("  Come visit Sto. Nino Church in Pag-asa!")
        elif self.main.data.city[self.data["last_location"]] == "GENERAL TRIAS":
            message.append("  Visit the Tejeros Convention site!")
        elif self.main.data.city[self.data["last_location"]] == "DASMARINAS":
            message.append("  Museo De La Salle is a must go place!")
        elif self.main.data.city[self.data["last_location"]] == "INDANG":
            message.append("  Visit the CvSU Main Campus today!")
        else:
            message.append("  Philippines is a great country to visit.")

        # Message update
        self.news_message.set_message(messages=message)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.news_message.add(self.objects)
