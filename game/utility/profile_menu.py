from game.utility.generic_menu import GenericMenu
from game.sprite.message import Message

import pygame


class ProfileMenu(GenericMenu):
    """
    This class will handle menu that is related to the profile of the user
    containing their details, business status, financial status, and the game
    progress such as achievements and etc.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.data = self.main.data.progress

        # Instantiate buttons and objects
        self.profile_label_message = Message(
            self.screen,
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.profile_values_message = Message(
            self.screen,
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.51) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.295) + self.canvas_rect.y,
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
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
            "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234",
        ]
        max_width = 45
        max_height = 16
        labels = []
        values = []

        # Line 1
        # Guide        "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        labels.append("==========================PROFILE========================")

        # Line 2
        name = self.data["name"]
        gender = self.data["gender"]
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        labels.append(f"Name: {name:<10s}               Gender: {gender:>6s}")

        # Line 3
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        location = self.main.data.city[self.data["last_location"]]
        labels.append(f"Location: {location}")

        # Line 4
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        cheat = self.data["cheater"]
        if cheat:
            labels.append(f"======================CHEAT=DETECTED=====================")
        else:
            labels.append(f"========================STATISTICS=======================")

        # Line 5
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        daily_expenses = f"P{self.data['daily_expenses']:,.2f}"
        labels.append(f"Daily Expenses:")
        values.append(daily_expenses)

        # Line 6
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        e_cash = f"P{self.data['cash']:,.2f}"
        labels.append(f"E-Cash Balance:")
        values.append(e_cash)

        # Line 7
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        savings = f"P{self.data['bank']['balance']:,.2f}"
        labels.append(f"Savings Balance:")
        values.append(savings)

        # Line 8
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        mouse_clicks = f"{self.data['statistics']['clicks']:,d}"
        labels.append(f"Mouse Clicks:")
        values.append(mouse_clicks)

        # Line 9
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        serve_customer = f"{self.data['statistics']['serve_customer']:,d}"
        labels.append(f"Served Customers:")
        values.append(serve_customer)

        # Line 10
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        serve_manual = f"{self.data['statistics']['serve_manual']:,d}"
        labels.append(f"Manual Service:")
        values.append(serve_manual)

        # Line 11
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        hire_employee = f"{self.data['statistics']['hire_employee']:,d}"
        labels.append(f"Employees Hired:")
        values.append(hire_employee)

        # Line 12
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        bank_interest = f"P{self.data['statistics']['bank_interest']:,.2f}"
        labels.append(f"Interest Profits:")
        values.append(bank_interest)

        # Line 13
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        earn_pnl = f"P{self.data['statistics']['earn_pnl']:,.2f}"
        labels.append(f"Share Profits:")
        values.append(earn_pnl)

        # Line 14
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        earn_profit = f"P{self.data['statistics']['earn_profit']:,.2f}"
        labels.append(f"Total Profits:")
        values.append(earn_profit)

        # Line 15
        # Guide         "0123456789ABCDEFGHIJ0123456789ABCDEFGHIJ01234"
        part_time_income = f"P{self.data['statistics']['part_time_income']:,.2f}"
        labels.append(f"Part-Time Income:")
        values.append(part_time_income)

        # Line 16
        labels.append("")

        self.profile_label_message.set_message(labels)
        self.profile_values_message.set_message(values)

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.profile_label_message.add(self.objects)
        self.profile_values_message.add(self.objects)
