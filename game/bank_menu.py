from game.sprite.message import Message
from game.sprite.button import Button

from game.generic_menu import GenericMenu

from datetime import datetime, timedelta
import pygame


class BankMenu(GenericMenu):
    """
    Menu showing the bank interface where the user can loan or store their money.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.progress = self.main.data.progress
        self.business_data = self.main.data.business
        self.data = self.progress["bank"]
        self.savings_interest = 0.05
        self.loan_interest = 0.05
        self.min_deposit = 10_000.0
        self.max_savings_limit = 1_000_000.0
        self.collateral = None
        self.business_location = None
        self.loan_months_payable = 3

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["Bank"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.savings_title_message = Message(
            self.screen,
            ["Savings Account"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.2) + self.canvas_rect.y,
            ),
        )
        self.savings_balance_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.28) + self.canvas_rect.y,
            ),
        )
        self.savings_description_message = Message(
            self.screen,
            [
                f"Your savings balance grows 5% every month from its deposit date.",
                f"Maximum limit is P{self.max_savings_limit:,.2f}",
            ],
            self.main.data.small_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.41) + self.canvas_rect.y,
            ),
        )
        self.deposit_button = Button(
            self.main,
            self._deposit_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.675) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.2) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "deposit_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "deposit_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "deposit_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    f"Minimum deposit: P{self.min_deposit:,.2f}",
                ],
            },
        )
        self.withdraw_button = Button(
            self.main,
            self._withdraw_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.675) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.3475) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images[
                    "withdraw_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "withdraw_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "withdraw_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    f"Withdraw all funds.",
                ],
            },
        )

        self.loan_title_message = Message(
            self.screen,
            ["Loan Balance"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.5) + self.canvas_rect.y,
            ),
        )
        self.loan_balance_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.58) + self.canvas_rect.y,
            ),
        )
        self.loan_description_message = Message(
            self.screen,
            [
                f"Loan requires a collateral (The business you own that has the",
                f"highest value) in order to be accepted. Payable within 3-month",
                f"equal payments plus 5% interest rate deducted automatically from",
                f"your e-cash account.",
            ],
            self.main.data.small_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.1) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.71) + self.canvas_rect.y,
            ),
        )
        self.loan_button = Button(
            self.main,
            self._loan_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.675) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.6) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["loan_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "loan_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "loan_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    f"Check loan eligibility.",
                ],
            },
        )
        self.loan_pay_button = Button(
            self.main,
            self._loan_pay_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.675) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7475) + self.canvas_rect.y,
            ),
            **{
                "idle": self.main.data.meta_images["pay_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "pay_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "pay_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    f"Pay your loan's",
                    f"bill in advance.",
                ],
            },
        )

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    def _check_savings_interests(self):
        current_date = datetime.strptime(
            self.progress["time"], self.main.scene_window.time.format
        )
        total_increase = 0
        account = "Savings"
        for index, entry in enumerate(self.data["ledger"]):
            entry_date = datetime.strptime(entry[0], self.main.scene_window.time.format)
            time_delta: timedelta = current_date - entry_date

            if time_delta.days >= 30:
                new_entry_date = entry_date + timedelta(days=30)
                savings_increase = entry[1] * self.savings_interest

                if self.data["balance"] < self.max_savings_limit:
                    self.data["balance"] += savings_increase
                    self.data["ledger"][index][1] += savings_increase
                else:
                    excess = abs(self.data["balance"] - self.max_savings_limit)
                    savings_increase += excess

                    self.data["balance"] = self.max_savings_limit
                    self.progress["cash"] += savings_increase
                    self.data["ledger"][index][1] = self.max_savings_limit
                    account = "E-Cash"

                self.data["ledger"][index][0] = new_entry_date.strftime(
                    self.main.scene_window.time.format
                )
                total_increase += savings_increase

        return total_increase, account

    def _deposit_confirm_callback(self):
        self.progress["cash"] -= self.min_deposit
        self.data["balance"] += self.min_deposit

        current_date = datetime.strptime(
            self.progress["time"], self.main.scene_window.time.format
        )
        for index, entry in enumerate(self.data["ledger"]):
            entry_date = datetime.strptime(entry[0], self.main.scene_window.time.format)
            if current_date.date() == entry_date.date():
                self.data["ledger"][index][1] += self.min_deposit
                break
        else:
            ledger_entry = [self.progress["time"], self.min_deposit]
            self.data["ledger"].append(ledger_entry)

        self.main.response_menu.set_message(
            [
                f"",
                f"Successfully deposited",
                f"P{self.min_deposit:,.2f} to the",
                f"Savings Account.",
                f"",
            ]
        )
        self.main.response_menu.enable = True

    def _deposit_button_callback(self, args):
        cash = self.progress["cash"]
        balance = self.data["balance"]

        if balance >= self.max_savings_limit:
            self.main.response_menu.set_message(
                [
                    f"Maximum limit reached.",
                    f"You can't deposit any",
                    f"more into the savings",
                    f"account.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True
        elif cash >= self.min_deposit:
            assumed_balance = cash - self.min_deposit
            self.main.confirm_menu.set_message_and_callback(
                [
                    f"",
                    f"Are you sure want to deposit",
                    f"P{self.min_deposit:,.2f} from",
                    f"your account?",
                    f"",
                    f"Your new balance will be:",
                    f"P{assumed_balance:,.2f}",
                ],
                self._deposit_confirm_callback,
            )
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"You dont have enough",
                    f"balance in your e-cash",
                    f"account.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True

        self.main.scene_window.update_data()

    def _withdraw_confirm_callback(self):
        withdrawn_funds = self.data["balance"]
        self.data["balance"] = 0.0
        self.data["ledger"] = []

        self.progress["cash"] += withdrawn_funds
        self.main.response_menu.set_message(
            [
                f"",
                f"Successfully withdrawn",
                f"P{withdrawn_funds:,.2f} to the",
                f"E-Cash Account.",
                f"",
            ]
        )
        self.main.response_menu.enable = True

    def _withdraw_button_callback(self, args):
        balance = self.data["balance"]
        if balance > 0:
            assumed_balance = self.progress["cash"] + balance
            self.main.confirm_menu.set_message_and_callback(
                [
                    f"",
                    f"Are you sure want to withdraw",
                    f"P{balance:,.2f} from your",
                    f"savings account?",
                    f"",
                    f"Your new balance will be:",
                    f"P{assumed_balance:,.2f}",
                ],
                self._withdraw_confirm_callback,
            )
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"You dont have enough",
                    f"balance in your savings",
                    f"account.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True

        self.main.scene_window.update_data()

    def _seize_collateral(self):
        location = self.data["loan_collateral_location"]
        business = self.data["loan_collateral_code"]

        self.progress["businesses"][location][business]["level"] = 1
        self.progress["businesses"][location][business]["date_acquired"] = ""
        self.progress["businesses"][location][business]["ownership"] = False
        self.progress["businesses"][location][business]["is_open"] = False
        self.progress["businesses"][location][business]["open_until"] = ""
        self.progress["businesses"][location][business]["has_employee"] = False
        self.progress["businesses"][location][business]["sales"] = 0.0
        self.progress["businesses"][location][business]["lifetime_sales"] = 0.0
        self.progress["businesses"][location][business]["last_profit"] = 0.0
        self.progress["businesses"][location][business]["lifetime_profit"] = 0.0
        self.progress["businesses"][location][business]["current_operation_sales"] = 0.0

        if self.progress["last_location"] == location:
            for business_meta in self.main.scene_window.business_data:
                meta = business_meta["meta"]
                if business == "street_food":
                    if isinstance(meta["image_name"], list):
                        business_object = business_meta["object"]
                        business_object.reset_data()

                elif meta["image_name"] == business:
                    business_object = business_meta["object"]
                    business_object.reset_data()

        # Clearing loan
        self.data["loan"] = 0.0
        self.data["loan_balance"] = 0.0
        self.data["loan_date"] = ""
        self.data["loan_collateral_ui"] = ""
        self.data["loan_collateral_code"] = ""
        self.data["loan_collateral_location"] = ""

        self.main.scene_window.update_data()

    def _check_loan_payment(self, for_seizing=True, monthly_check=True):
        if self.data["loan"] == 0.0:
            return None

        current_date = datetime.strptime(
            self.progress["time"], self.main.scene_window.time.format
        )
        loan_date = datetime.strptime(
            self.data["loan_date"], self.main.scene_window.time.format
        )
        time_delta = current_date - loan_date
        if time_delta.days < 30 and monthly_check:
            return None

        if monthly_check:
            new_loan_date = loan_date + timedelta(days=30)
        else:
            new_loan_date = current_date

        loan_base_payment = self.data["loan"] / self.loan_months_payable
        loan_interest = loan_base_payment * self.loan_interest
        loan_total_payment = loan_base_payment + loan_interest

        if self.progress["cash"] >= loan_total_payment:
            self.data["loan_date"] = new_loan_date.strftime(
                self.main.scene_window.time.format
            )
            self.data["loan_balance"] -= loan_base_payment
            self.progress["cash"] -= loan_total_payment

            if self.data["loan_balance"] <= 0.0:
                self.data["loan"] = 0.0
                self.data["loan_balance"] = 0.0
                self.data["loan_date"] = ""
                self.data["loan_collateral_ui"] = ""
                self.data["loan_collateral_code"] = ""
                self.data["loan_collateral_location"] = ""

            return loan_base_payment, loan_interest, "E-Cash"
        elif self.data["balance"] >= loan_total_payment:
            self.data["loan_date"] = new_loan_date.strftime(
                self.main.scene_window.time.format
            )
            self.data["loan_balance"] -= loan_base_payment
            self.data["balance"] -= loan_total_payment

            ledger_balance = loan_total_payment
            ledger_zero_indexes = []

            for index, entry in enumerate(self.data["ledger"]):
                if ledger_balance >= entry[1]:
                    ledger_balance -= entry[1]
                    self.data["ledger"][index][1] -= 0
                    ledger_zero_indexes.append(index)
                elif ledger_balance < entry[1]:
                    self.data["ledger"][index][1] -= ledger_balance
                    break

            if len(ledger_zero_indexes) > 0:
                for index in ledger_zero_indexes:
                    del self.data["ledger"][index]

            if self.data["loan_balance"] <= 0.0:
                self.data["loan"] = 0.0
                self.data["loan_balance"] = 0.0
                self.data["loan_date"] = ""
                self.data["loan_collateral_ui"] = ""
                self.data["loan_collateral_code"] = ""
                self.data["loan_collateral_location"] = ""

            return loan_base_payment, loan_interest, "Savings"
        elif for_seizing:
            self._seize_collateral()
            return "SEIZED"
        else:
            return "NOT ENOUGH"

    def _evaluate_businesses(self):
        highest_business_name = None
        highest_business_code = None
        highest_business_cost = 0.0

        location_attributes = ["last_visited"]
        for location in self.progress["businesses"]:
            if location == "test_location":
                continue

            for business_name in self.progress["businesses"][location]:
                if business_name in location_attributes:
                    continue

                business_data = self.progress["businesses"][location][business_name]
                if business_data["ownership"]:
                    cost = self.business_data[business_name]["initial_cost"]
                    ui_name = self.business_data[business_name]["name"]

                    if not highest_business_name:
                        highest_business_name = ui_name
                        highest_business_code = business_name
                        highest_business_cost = cost
                        self.data["loan_collateral_location"] = location
                    else:
                        if cost >= highest_business_cost:
                            highest_business_name = ui_name
                            highest_business_code = business_name
                            highest_business_cost = cost
                            self.data["loan_collateral_location"] = location

        if not highest_business_name:
            return None

        return highest_business_name, highest_business_code, highest_business_cost

    def _loan_confirm_callback(self):
        assert self.collateral
        business_name, business_code, business_cost = self.collateral

        self.data["loan"] = business_cost
        self.data["loan_balance"] = business_cost
        self.data["loan_date"] = self.progress["time"]
        self.data["loan_collateral_ui"] = business_name
        self.data["loan_collateral_code"] = business_code

        self.progress["cash"] += business_cost
        self.main.response_menu.set_message(
            [
                f"",
                f"Successfully loaned",
                f"P{business_cost:,.2f} from the",
                f"Bank.",
                f"",
            ]
        )
        self.main.response_menu.enable = True

    def _loan_pay_button_callback(self, args):
        message = None
        response = self._check_loan_payment(
            for_seizing=False,
            monthly_check=False,
        )
        if response == "NOT ENOUGH":
            message = [
                f"",
                f"You don't have enough",
                f"E-Cash or Savings Account",
                f"balance to pay your loan.",
                f"",
            ]
        else:
            loan_base_payment, loan_interest, account = response
            message = [
                f"Bank Loan Update:",
                f"P{loan_base_payment:,.2f} ",
                f"+(P{loan_interest:,.2f})",
                f"interest is paid using",
                f"your {account} Account.",
            ]

        if self.main.response_menu.enable:
            # add to queue
            self.main.response_menu.queue.append(message)
        else:
            # set_message and enable
            self.main.response_menu.set_message(message)
            self.main.response_menu.enable = True

    def _loan_button_callback(self, args):
        if self.data["loan"]:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"You only have one loan",
                    f"at a time. Please settle",
                    f"your current loan first.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True
            return

        self.collateral = self._evaluate_businesses()
        if self.collateral:
            business_name, x, business_cost = self.collateral
            self.main.confirm_menu.set_message_and_callback(
                [
                    f"",
                    f"You can loan up to P{business_cost:,.2f}",
                    f"if you use {business_name:.20s}",
                    f"as your collateral.",
                    f"",
                    f"Would you like to proceed?",
                    f"",
                ],
                self._loan_confirm_callback,
            )
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"You must own atleast one",
                    f"business to use it as",
                    f"your loan collateral.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True

        self.main.scene_window.update_data()

    # Abstract method implementation
    def set_button_states(self):
        self.loan_pay_button.set_disabled(True)
        if self.data["loan"] > 0.0:
            self.loan_pay_button.set_disabled(False)

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        collateral = ""
        if self.data["loan"]:
            collateral = f"(Collateral: {self.data['loan_collateral_ui']:.15s})"

        self.savings_balance_message.set_message([f"P{self.data['balance']:,.2f}"])
        self.loan_title_message.set_message([f"Loan Balance {collateral}"])
        self.loan_balance_message.set_message([f"P{self.data['loan_balance']:,.2f}"])

        self.set_button_states()

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.savings_title_message.add(self.objects)
        self.savings_balance_message.add(self.objects)
        self.savings_description_message.add(self.objects)
        self.deposit_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.withdraw_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.loan_title_message.add(self.objects)
        self.loan_balance_message.add(self.objects)
        self.loan_description_message.add(self.objects)
        self.loan_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
        self.loan_pay_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

    def handle_event(self, event):
        super().handle_event(event)

        if event.type != pygame.KEYDOWN:
            return

        # For debug only
        if event.key == pygame.K_F1:
            # print(self._check_loan_payment())
            ...
