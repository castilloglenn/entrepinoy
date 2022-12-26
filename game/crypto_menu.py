from game.sprite.message import Message
from game.sprite.button import Button

from game.generic_menu import GenericMenu

from numerize.numerize import numerize
import pygame
import random


class CryptoMenu(GenericMenu):
    """
    Menu showing the simplified trading UI of crptocurrencies.
    """

    def __init__(self, main) -> None:
        super().__init__(main)
        # The parent class contains:
        # handle_event(self, event)
        # update(self)
        # close(self)

        # Instantiate logical variables
        self.progress = self.main.data.progress
        self.data = self.progress["crypto"]
        self.symbols = self.main.data.symbols["crypto"]
        self.ranges = {
            "low": [20, 100],
            "medium": [200, 1000],
            "high": [2_000, 10_000],
        }
        self.range_weight = [0.6, 0.3, 0.1]
        self.traj_weight = [0.5, 0.5]
        self.traj = 1
        self.change = 0.0
        self.start_change = 0.0
        self.buy_count = 1
        self.sell_count = 1
        self.average_position = 0.0

        # Mitigate empty symbol (Scene's Day Callback should be the one to update)
        if self.data["symbol"] == "":
            self._reset_symbol()

        # Instantiate buttons and objects
        self.title_message = Message(
            self.screen,
            ["Cryptocurrency Market"],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y,
            ),
        )
        self.symbol_title_message = Message(
            self.screen,
            [
                "Today's",
                "Most Active Crypto",
            ],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.09) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.27) + self.canvas_rect.y,
            ),
        )
        self.symbol_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.09) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.36) + self.canvas_rect.y,
            ),
        )
        self.price_message = Message(
            self.screen,
            [""],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.09) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.5) + self.canvas_rect.y,
            ),
        )
        self.change_message = Message(
            self.screen,
            [""],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.09) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.6) + self.canvas_rect.y,
            ),
        )
        self.change_start_message = Message(
            self.screen,
            [""],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.09) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7) + self.canvas_rect.y,
            ),
        )
        self.shares_title_message = Message(
            self.screen,
            ["Shares"],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.49) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.305) + self.canvas_rect.y,
            ),
        )
        self.pnl_title_message = Message(
            self.screen,
            ["Profit and Loss"],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.7) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.305) + self.canvas_rect.y,
            ),
        )
        self.shares_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.53) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.425) + self.canvas_rect.y,
            ),
        )
        self.pnl_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.8) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.425) + self.canvas_rect.y,
            ),
        )
        self.buy_button = Button(
            self.main,
            self._buy_share,
            center_coordinates=(
                int(self.canvas_rect.width * 0.55) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.58) + self.canvas_rect.y,
            ),
            button_ratio=0.8,
            **{
                "idle": self.main.data.meta_images["buy_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "buy_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "buy_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Buy share(s) at the current price.",
                ],
            },
        )
        self.buy_increase_button = Button(
            self.main,
            self._increase_buy_count,
            center_coordinates=(
                int(self.canvas_rect.width * 0.66) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.58) + self.canvas_rect.y,
            ),
            button_ratio=0.3,
            **{
                "idle": self.main.data.meta_images[
                    "plus_sign_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "plus_sign_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "plus_sign_button_disabled"
                ].convert_alpha(),
            },
        )
        self.buy_indicator_message = Message(
            self.screen,
            [f"{self.buy_count}"],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.73) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.575) + self.canvas_rect.y,
            ),
        )
        self.buy_decrease_button = Button(
            self.main,
            self._decrease_buy_count,
            center_coordinates=(
                int(self.canvas_rect.width * 0.8) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.58) + self.canvas_rect.y,
            ),
            button_ratio=0.3,
            **{
                "idle": self.main.data.meta_images[
                    "minus_sign_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "minus_sign_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "minus_sign_button_disabled"
                ].convert_alpha(),
            },
        )

        self.sell_button = Button(
            self.main,
            self._sell_share,
            center_coordinates=(
                int(self.canvas_rect.width * 0.55) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7) + self.canvas_rect.y,
            ),
            button_ratio=0.8,
            **{
                "idle": self.main.data.meta_images["sell_button_idle"].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "sell_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "sell_button_disabled"
                ].convert_alpha(),
                "tooltip": [
                    "Sell share(s) at the current price.",
                ],
            },
        )
        self.sell_increase_button = Button(
            self.main,
            self._increase_sell_count,
            center_coordinates=(
                int(self.canvas_rect.width * 0.66) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7) + self.canvas_rect.y,
            ),
            button_ratio=0.3,
            **{
                "idle": self.main.data.meta_images[
                    "plus_sign_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "plus_sign_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "plus_sign_button_disabled"
                ].convert_alpha(),
            },
        )
        self.sell_indicator_message = Message(
            self.screen,
            [f"{self.sell_count}"],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.73) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.695) + self.canvas_rect.y,
            ),
        )
        self.sell_decrease_button = Button(
            self.main,
            self._decrease_sell_count,
            center_coordinates=(
                int(self.canvas_rect.width * 0.8) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7) + self.canvas_rect.y,
            ),
            button_ratio=0.3,
            **{
                "idle": self.main.data.meta_images[
                    "minus_sign_button_idle"
                ].convert_alpha(),
                "outline": self.main.data.meta_images[
                    "minus_sign_button_hovered"
                ].convert_alpha(),
                "disabled": self.main.data.meta_images[
                    "minus_sign_button_disabled"
                ].convert_alpha(),
            },
        )

        self._update_average_position()

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
    def _update_average_position(self):
        if len(self.data["ledger"]) == 0:
            self.average_position = 0.0
            return

        position_gross_sum = 0.0
        weights = 0
        for entry in self.data["ledger"]:
            weights += entry[1]
            position_gross_sum += entry[1] * entry[2]

        self.average_position = position_gross_sum / weights

    def _sell_share(self, args, dump_all=False):
        shares = self.data["shares"]
        if shares == 0:
            return

        price = self.data["price"]
        if dump_all:
            for entry in self.data["ledger"]:
                share_count = entry[1]
                share_price = entry[2] * share_count
                sell_price = price * share_count
                delta = sell_price - share_price
                self.data["pnl"] += delta
                self.progress["cash"] += sell_price

            message = [
                f"Crypto Shares Update:",
                f"Your remaining shares",
                f"has been sold.",
                f"Yesterday's PNL:",
                f"P{self.data['pnl']:,.2f}",
            ]
            if self.main.response_menu.enable:
                # add to queue
                self.main.response_menu.queue.append(message)
            else:
                # set_message and enable
                self.main.response_menu.set_message(message)
                self.main.response_menu.enable = True

            self.main.scene_window.update_data()
            return

        count = self.sell_count
        if count > shares:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"You cannot sell more",
                    f"shares than you have.",
                    f"",
                    f"",
                ]
            )
            self.main.response_menu.enable = True
            return

        for index, entry in enumerate(self.data["ledger"]):
            sell_count = min(count, self.data["ledger"][index][1])
            share_price = entry[2] * sell_count
            sell_price = price * sell_count
            delta = sell_price - share_price

            self.data["pnl"] += delta
            self.progress["cash"] += sell_price
            self.data["shares"] -= sell_count
            self.data["ledger"][index][1] -= sell_count

            count -= sell_count
            if count == 0:
                break

        new_ledger = []
        for entry in self.data["ledger"]:
            if entry[1] > 0:
                new_ledger.append(entry)
        self.data["ledger"] = new_ledger

        self._update_average_position()
        self.main.scene_window.update_data()

    def _buy_share(self, args):
        cost = self.data["price"] * self.buy_count
        if self.progress["cash"] < cost:
            self.main.response_menu.set_message(
                [
                    f"",
                    f"Not enough balance in",
                    f"your E-Cash Account to",
                    f"pay P{cost:,.2f}.",
                    f"",
                ]
            )
            self.main.response_menu.enable = True
            return

        self.progress["cash"] -= cost
        self.data["shares"] += self.buy_count

        for index, entry in enumerate(self.data["ledger"]):
            if entry[0] == self.progress["time"] and entry[2] == self.data["price"]:
                self.data["ledger"][index][1] += self.buy_count
                break
        else:
            self.data["ledger"].append(
                [
                    self.progress["time"],
                    self.buy_count,
                    self.data["price"],
                ]
            )

        self._update_average_position()
        self.main.scene_window.update_data()

    def _increase_buy_count(self, args):
        self.buy_count = min(self.buy_count + 1, 99)

    def _decrease_buy_count(self, args):
        self.buy_count = max(self.buy_count - 1, 1)

    def _increase_sell_count(self, args):
        self.sell_count = min(self.sell_count + 1, 99)

    def _decrease_sell_count(self, args):
        self.sell_count = max(self.sell_count - 1, 1)

    def _update_price(self):
        changes = [0.01, 0.03, 0.05, 0.1, 0.25, 0.5, 0.75]
        changes_weights = [0.8, 0.1, 0.08, 0.01, 0.008, 0.0015, 0.0005]
        traj_balancer = 0.1

        self.traj = random.choices(population=[0, 1], weights=self.traj_weight)[0]
        self.change = random.choices(population=changes, weights=changes_weights)[0]
        self.change = random.uniform(self.change - 0.005, self.change + 0.005)
        change_value = max(self.data["price"] * self.change, 0.01)

        if self.traj == 1:
            # Upwards/Increase
            self.data["price"] += change_value

            self.traj_weight = (
                min(self.traj_weight[0] + traj_balancer, 1.0),
                max(self.traj_weight[1] - traj_balancer, 0.0),
            )
        elif self.traj == 0:
            # Downwards/Decrease
            self.data["price"] -= change_value

            self.traj_weight = (
                max(self.traj_weight[0] - traj_balancer, 0.0),
                min(self.traj_weight[1] + traj_balancer, 1.0),
            )

        # Additional balancer
        exp_balancer = traj_balancer * 1.5
        self.start_change = round(
            self.data["price"] / self.data["starting_price"] * 100, 2
        )
        if self.start_change > 120.0:
            # Bullish
            self.traj_weight = (
                min(self.traj_weight[0] + exp_balancer, 1.0),
                max(self.traj_weight[1] - exp_balancer, 0.0),
            )
        elif self.start_change < 80.0:
            # Bearish
            self.traj_weight = (
                max(self.traj_weight[0] - exp_balancer, 0.0),
                min(self.traj_weight[1] + exp_balancer, 1.0),
            )

    def _reset_symbol(self):
        if len(self.data["ledger"]) > 0:
            self._sell_share(None, dump_all=True)

        previous_symbol = self.data["symbol"]
        new_symbol = self.data["symbol"]
        while previous_symbol == new_symbol:
            new_symbol = random.choice(self.symbols)

        self.data["symbol"] = new_symbol
        price_range_threshold = random.choices(
            population=list(self.ranges.keys()),
            weights=self.range_weight,
        )[0]
        price_range = self.ranges[price_range_threshold]
        price = random.uniform(float(price_range[0]), float(price_range[1]))
        self.data["starting_price"] = round(price, 2)
        self.data["price"] = round(price, 2)
        self.data["shares"] = 0
        self.data["pnl"] = 0.0
        self.data["ledger"] = []
        self.average_position = 0.0
        self.traj_weight = [0.5, 0.5]

        if self.main.scene_window:
            self.main.scene_window.update_data()

    # Abstract method implementation
    def set_button_states(self):
        self.buy_increase_button.set_disabled(self.buy_count >= 99)
        self.sell_increase_button.set_disabled(self.sell_count >= 99)

        self.buy_decrease_button.set_disabled(self.buy_count <= 1)
        self.sell_decrease_button.set_disabled(self.sell_count <= 1)

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        self.symbol_message.set_message([f"{self.data['symbol']}"])
        self.price_message.set_message([f"P{self.data['price']:,.2f}"])

        change_prefix = "+" if self.traj else "-"
        self.change_message.set_message([f"({change_prefix}{self.change * 100:,.2f}%)"])

        position = ""
        if self.average_position > 0.0:
            position = f"Average Position: P{self.average_position:,.2f}"
        self.change_start_message.set_message(
            [
                f"vs. Price at 8:00AM: {self.start_change:,.2f}%",
                position,
            ]
        )

        self.shares_message.set_message([f"{numerize(self.data['shares'])}"])
        self.pnl_message.set_message([f"{numerize(self.data['pnl'])}"])

        self.buy_indicator_message.set_message([f"{self.buy_count}"])
        self.sell_indicator_message.set_message([f"{self.sell_count}"])

        self.set_button_states()

    # Abstract method implementation
    def set_data(self):
        super().set_data()

        self.title_message.add(self.objects)
        self.symbol_title_message.add(self.objects)
        self.symbol_message.add(self.objects)
        self.price_message.add(self.objects)
        self.change_message.add(self.objects)
        self.change_start_message.add(self.objects)
        self.shares_title_message.add(self.objects)
        self.pnl_title_message.add(self.objects)
        self.shares_message.add(self.objects)
        self.pnl_message.add(self.objects)
        self.buy_indicator_message.add(self.objects)
        self.sell_indicator_message.add(self.objects)

        self.buy_decrease_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.buy_increase_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.buy_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )

        self.sell_decrease_button.add(
            self.objects, self.buttons, self.hoverable_buttons
        )
        self.sell_increase_button.add(
            self.objects, self.buttons, self.hoverable_buttons
        )
        self.sell_button.add(
            self.objects, self.buttons, self.hoverable_buttons, self.tooltips
        )
