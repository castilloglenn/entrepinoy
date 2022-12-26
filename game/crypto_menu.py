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
        self.data = self.main.data.progress["crypto"]
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
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.27) + self.canvas_rect.y,
            ),
        )
        self.symbol_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.36) + self.canvas_rect.y,
            ),
        )
        self.price_message = Message(
            self.screen,
            [""],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.5) + self.canvas_rect.y,
            ),
        )
        self.change_message = Message(
            self.screen,
            [""],
            self.main.data.title_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.6) + self.canvas_rect.y,
            ),
        )
        self.change_start_message = Message(
            self.screen,
            [""],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.06) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.7) + self.canvas_rect.y,
            ),
        )
        self.shares_title_message = Message(
            self.screen,
            ["Shares"],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.46) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.305) + self.canvas_rect.y,
            ),
        )
        self.pnl_title_message = Message(
            self.screen,
            ["Profit and Loss"],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.67) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.305) + self.canvas_rect.y,
            ),
        )
        self.shares_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.5) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.425) + self.canvas_rect.y,
            ),
        )
        self.pnl_message = Message(
            self.screen,
            [""],
            self.main.data.giga_font,
            self.main.data.colors["brown"],
            center_coordinates=(
                int(self.canvas_rect.width * 0.77) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.425) + self.canvas_rect.y,
            ),
        )
        self.buy_button = Button(
            self.main,
            lambda x: print("buy"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.49) + self.canvas_rect.x,
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
                    "Buy stock(s) at the current price.",
                ],
            },
        )
        self.buy_increase_button = Button(
            self.main,
            lambda x: print("buy increase"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.58) + self.canvas_rect.x,
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
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.575) + self.canvas_rect.y,
            ),
        )
        self.buy_decrease_button = Button(
            self.main,
            lambda x: print("buy decrease"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
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
            lambda x: print("sell"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.49) + self.canvas_rect.x,
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
                    "Sell stock(s) at the current price.",
                ],
            },
        )
        self.sell_increase_button = Button(
            self.main,
            lambda x: print("sell increase"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.58) + self.canvas_rect.x,
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
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.695) + self.canvas_rect.y,
            ),
        )
        self.sell_decrease_button = Button(
            self.main,
            lambda x: print("buy decrease"),
            center_coordinates=(
                int(self.canvas_rect.width * 0.72) + self.canvas_rect.x,
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

    # If reconstructable, add this function
    # def reconstruct(self, args):
    #     ...

    # Internal functions here
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

    def _dump_shares(self):
        ...

    def _reset_symbol(self):
        if len(self.data["ledger"]) > 0:
            self._dump_shares()

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

        self.traj_weight = [0.5, 0.5]

    # Abstract method implementation
    def set_button_states(self):
        ...

    # Abstract method implementation
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        self.symbol_message.set_message([f"{self.data['symbol']}"])
        self.price_message.set_message([f"P{self.data['price']:,.2f}"])

        change_prefix = "+" if self.traj else "-"
        self.change_message.set_message([f"({change_prefix}{self.change * 100:,.2f}%)"])
        self.change_start_message.set_message(
            [f"{self.start_change:,.2f}% vs. price at 8:00AM"]
        )

        self.shares_message.set_message([f"{numerize(self.data['shares'])}"])
        self.pnl_message.set_message([f"{numerize(self.data['pnl'])}"])

        self.buy_indicator_message.set_message([f"{self.buy_count}"])

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
