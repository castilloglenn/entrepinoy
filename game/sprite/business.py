from game.sprite.message import Message
from game.sprite.button import Button

from datetime import datetime, timedelta
import random
import pygame
import copy

from pprint import pprint


class Business(Button):
    """
    This class handles the business interface in the scene.
    It controls its attributes and the states when it is open or closed.
    """

    def __init__(
        self,
        scene,
        name,
        callback_function,
        business_data,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
        collide_rect=None,
        **states,
    ):
        super().__init__(
            scene.main,
            callback_function,
            top_left_coordinates=top_left_coordinates,
            center_coordinates=center_coordinates,
            midbottom_coordinates=midbottom_coordinates,
            collide_rect=collide_rect,
            **states,
        )
        # Hide the business object as it loads to its proper place
        self.visible = False

        self.scene = scene
        self.name = name
        self.time = self.scene.time
        self.progress = None

        self.states = states
        self.outline = self.states["outline"].convert_alpha()

        # Business attributes
        self.business_data = business_data
        self.name_code = None
        self.ownership = None
        self.open_until = None
        self.business_state = None
        self.has_employee = None

        self.employee_spritesheet = self.states["employee"]["spritesheet"]
        self.employee_json = self.states["employee"]["json"]
        self.serve_button_relative_location = (0.5, 0.5)
        self.employee_frames = []
        self.employee_index = 0

        self.fps = self.scene.main.data.setting["fps"]
        self.frame_length = 1 / self.fps

        # Serving animation waiting attributes
        self.serving_frame_counter = 0
        self.serving_seconds_counter = 0
        self.serving_cooldown = 1  # seconds

        # Income display message
        self.current_income = 0.0
        self.income_visible = False
        self.income_message = Message(
            self.scene.main.screen,
            ["+P0.00"],
            self.scene.main.data.large_font,
            self.scene.main.data.colors["yellow"],
            outline_thickness=2,
        )
        self.income_travel_distance = 50
        self.income_travel_distance_per_frame = (
            self.income_travel_distance * self.frame_length
        )
        self.income_travel_counter = 0
        self.income_opacity = 255
        self.income_frame_counter = 0
        self.income_seconds_counter = 0
        self.income_display_duration = 1  # seconds
        self.income_display_fade_duration = 3  # seconds
        self.income_decrement = (
            self.frame_length / self.income_display_fade_duration
        ) * 255

        # This speed controls when to switch from sprite animation to the
        #   next animation in the spritesheet
        self.animate_speed = self.fps * 0.12
        self.animation_tick = 0

        # Parsing all the sprites contained in the spritesheet
        for frame_name, content in self.employee_json["frames"].items():
            self.name_keyword = frame_name.replace("_employee_1.png", "")
            break

        for index in range(len(self.employee_json["frames"])):
            self.employee_frames.append(
                self.fetch_sprite(f"{self.name_keyword}_employee_{index + 1}.png")
            )

        self.standby_image = self.employee_frames.pop()
        self.is_standby = True
        self.is_serving = False

        self.queue = []
        self.queue_limit = 5

        # Setting up pop-up buttons
        self.serve_button = Button(
            self.scene.main,
            None,
            **{
                "idle": self.scene.main.data.scene["serve_button_idle"].convert_alpha(),
                "outline": self.scene.main.data.scene[
                    "serve_button_hovered"
                ].convert_alpha(),
            },
        )
        self.serve_button.set_callback(self.serve_customer)

        # Assigning important data to the None variables above
        self.reset_data()

        # Showing back the business after it reconstructs everything back
        self.visible = True

    def reset_data(self):
        self.progress = self.scene.main.data.progress

        if self.business_data["name"] == "Street Foods Stall":
            self.name_code = "street_food"
        else:
            self.name_code = self.name

        self.ownership = self.progress["businesses"][self.progress["last_location"]][
            self.name_code
        ]["ownership"]
        self.open_until = self.progress["businesses"][self.progress["last_location"]][
            self.name_code
        ]["open_until"]
        self.served_count = 0

        # Setting the standing animation for the sprite
        if not self.ownership:
            self.business_state = "closed"
        elif self.ownership:
            is_open = self.progress["businesses"][self.progress["last_location"]][
                self.name_code
            ]["is_open"]
            if is_open:
                self.business_state = "open"
            else:
                self.business_state = "closed"
        # Final check for business if the business duration is over
        if self.open_until == "":
            self.business_state = "closed"

        self.has_employee = self.progress["businesses"][self.progress["last_location"]][
            self.name_code
        ]["has_employee"]

    def reconstruct(
        self,
        scene,
        name,
        callback_function,
        business_data,
        top_left_coordinates=None,
        center_coordinates=None,
        midbottom_coordinates=None,
        collide_rect=None,
        **states,
    ):
        super().__init__(
            scene.main,
            callback_function,
            top_left_coordinates=top_left_coordinates,
            center_coordinates=center_coordinates,
            midbottom_coordinates=midbottom_coordinates,
            collide_rect=collide_rect,
            **states,
        )
        # Hide the business object as it loads to its proper place
        self.visible = False

        self.scene = scene
        self.name = name
        self.time = self.scene.time
        self.progress = None

        self.states = states
        self.outline = self.states["outline"].convert_alpha()

        # Business attributes
        self.business_data = business_data
        self.name_code = None
        self.ownership = None
        self.open_until = None
        self.business_state = None
        self.has_employee = None

        self.employee_spritesheet = self.states["employee"]["spritesheet"]
        self.employee_json = self.states["employee"]["json"]
        self.serve_button_relative_location = (0.5, 0.5)
        self.employee_frames = []
        self.employee_index = 0

        self.fps = self.scene.main.data.setting["fps"]
        self.frame_length = 1 / self.fps

        # Serving animation waiting attributes
        self.serving_frame_counter = 0
        self.serving_seconds_counter = 0

        # Income display message
        self.current_income = 0.0
        self.income_visible = False
        self.income_travel_distance_per_frame = (
            self.income_travel_distance * self.frame_length
        )
        self.income_travel_counter = 0
        self.income_frame_counter = 0
        self.income_seconds_counter = 0
        self.income_decrement = (
            self.frame_length / self.income_display_fade_duration
        ) * 255

        self.animate_speed = self.fps * 0.12
        self.animation_tick = 0

        # Parsing all the sprites contained in the spritesheet
        for frame_name, content in self.employee_json["frames"].items():
            self.name_keyword = frame_name.replace("_employee_1.png", "")
            break

        for index in range(len(self.employee_json["frames"])):
            self.employee_frames.append(
                self.fetch_sprite(f"{self.name_keyword}_employee_{index + 1}.png")
            )

        self.standby_image = self.employee_frames.pop()
        self.is_standby = True
        self.is_serving = False

        self.queue = []

        # Assigning important data to the None variables above
        self.reset_data()

        # Showing back the business after it reconstructs everything back
        self.visible = True

    def disown_business(self):
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "level"
        ] = 1
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "date_acquired"
        ] = ""
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "ownership"
        ] = False
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "is_open"
        ] = False
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "open_until"
        ] = ""
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "has_employee"
        ] = False
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "sales"
        ] = 0.0
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "lifetime_sales"
        ] = 0.0
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "last_profit"
        ] = 0.0
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "lifetime_profit"
        ] = 0.0
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "current_operation_sales"
        ] = 0.0

        self.reset_data()

    def is_business_serving(self):
        return self.has_employee and not self.is_standby and self.is_serving

    def is_business_ready_to_serve(self):
        return (
            self.has_employee
            and self.is_standby
            and not self.is_serving
            and len(self.queue) > 0
        )

    def update(self):
        if not self.visible:
            return

        if self.is_business_serving():
            self.animation_tick += 1
            if self.animation_tick >= self.animate_speed:
                self.animation_tick = 0
                self.employee_index = (self.employee_index + 1) % len(
                    self.employee_frames
                )

                self.idle = self.employee_frames[self.employee_index]
                self.hovered = self.employee_frames[self.employee_index].copy()
                self.hovered.blit(self.outline, (0, 0))

                if self.employee_index == len(self.employee_frames) - 1:
                    self.is_serving = False
                    self.is_standby = True

                    self.update_business_images()
                    self.serve_customer()

        elif self.is_business_ready_to_serve():
            if self.queue[0].is_standing:
                self.serving_frame_counter += self.frame_length
                if int(self.serving_frame_counter) >= 1:
                    self.serving_frame_counter -= 1
                    self.serving_seconds_counter += 1

                    # Automatic serving when employees is present
                    if self.serving_seconds_counter >= self.serving_cooldown:
                        self.serving_seconds_counter = 0
                        self.set_serve_animation()
        else:
            self.update_business_images()

        self.set_image_and_rect()
        super().update()

        # Checks for income generation presentation
        if self.income_visible:
            if self.income_opacity <= 0:
                self.reset_income_display()
                return

            if self.income_seconds_counter != self.income_display_duration:
                self.income_frame_counter += self.frame_length
                if int(self.income_frame_counter) >= 1:
                    self.income_frame_counter -= 1
                    self.income_seconds_counter += 1

                self.income_travel_counter += self.income_travel_distance_per_frame
                if self.income_travel_counter >= 1:
                    self.income_message.center_coordinates = (
                        self.income_message.center_coordinates[0],
                        self.income_message.center_coordinates[1]
                        - int(self.income_travel_counter),
                    )
                    self.income_travel_counter -= int(self.income_travel_counter)
            else:
                self.income_opacity = max(
                    self.income_opacity - self.income_decrement, 0
                )
                self.income_message.set_opacity(self.income_opacity)

            self.income_message.update()

        # Checks for the manual serving button
        if len(self.queue) > 0 and not self.has_employee and self.visible:
            if self.queue[0].is_standing:
                # self.business_data["rel_serve_coordinates"]
                if self.business_data["placement"] == "front":
                    new_center = (
                        self.rect.center[0],
                        self.scene.main.screen.get_rect().height * 0.43,
                    )
                elif self.business_data["placement"] == "back":
                    new_center = (
                        self.rect.center[0],
                        self.scene.main.screen.get_rect().height * 0.3,
                    )

                self.serve_button.rect.center = new_center
                self.serve_button.visible = True
            else:
                self.serve_button.visible = False
        else:
            self.serve_button.visible = False
        self.serve_button.update()

        # Checks if the time limit for operation and employment stops
        if self.business_state == "open":
            deadline = datetime.strptime(
                self.progress["businesses"][self.progress["last_location"]][
                    self.name_code
                ]["open_until"],
                self.time.format,
            )
            if self.time.time >= deadline:
                self.set_business_state("closed")

    def reset_income_display(self):
        # Placing the income message relative to the position of the serve button
        self.income_message.center_coordinates = (
            int(
                self.rect.x
                + (
                    self.rect.width
                    * self.scene.main.data.business[self.name_code]["queuing_point"]
                )
            ),
            int(self.rect.top + (self.rect.height * 0.3)),
        )

        self.income_frame_counter = 0
        self.income_seconds_counter = 0
        self.income_travel_counter = 0

        self.income_message.set_opacity(255)
        self.income_opacity = 255
        self.income_visible = False

    def set_serve_animation(self):
        # Trigger one full sprite animation then trigger serve command
        #   and makes the first customer leave
        if len(self.queue) > 0 and self.has_employee and self.queue[0].is_standing:
            self.is_standby = False
            self.is_serving = True

    def set_business_state(self, new_state: str):
        # Open or closed
        if new_state == "open":
            current_in_game_time = self.time.time
            expiration = current_in_game_time + timedelta(
                hours=self.scene.main.data.meta["operating_hours"]
            )
            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "open_until"
            ] = datetime.strftime(expiration, self.time.format)
            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "current_operation_sales"
            ] = 0.0

            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "is_open"
            ] = True

        elif new_state == "closed":
            current_sales = self.progress["businesses"][self.progress["last_location"]][
                self.name_code
            ]["current_operation_sales"]
            operation_cost = self.business_data["daily_expenses"]
            employment_cost = self.business_data["employee_cost"]

            if self.has_employee:
                operation_cost += employment_cost

            net_profit_or_loss = current_sales - operation_cost
            if net_profit_or_loss > 0.0:
                self.main.tracker.increment_tracker(
                    "business_profit", increment=net_profit_or_loss
                )
                self.main.tracker.increment_tracker(
                    "earn_profit", increment=net_profit_or_loss
                )

            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "open_until"
            ] = ""
            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "is_open"
            ] = False
            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "last_profit"
            ] = net_profit_or_loss
            self.progress["businesses"][self.progress["last_location"]][self.name_code][
                "lifetime_profit"
            ] += net_profit_or_loss
            self.set_employee_status(False)

        self.business_state = new_state
        self.update_business_images()
        self.set_image_and_rect()

    def set_employee_status(self, employee_status):
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "has_employee"
        ] = employee_status
        self.has_employee = employee_status
        self.update_business_images()
        self.set_image_and_rect()

    def check_hovered(self, hover_coordinates):
        if self.state == "disabled" or not self.visible:
            return False

        if (
            self.serve_button.check_hovered(hover_coordinates)
            and self.serve_button.visible
        ):
            self.state = "idle"
            self.set_image_and_rect()
            return True
        else:
            self.state = "hovered"
            self.set_image_and_rect()
            return super().check_hovered(hover_coordinates)

    def check_clicked(self, click_coordinates):
        if self.state == "disabled" or not self.visible:
            return False

        if (
            self.serve_button.check_clicked(click_coordinates)
            and self.serve_button.visible
        ):
            return True
        else:
            return super().check_clicked(click_coordinates)

    def update_business_images(self):
        if self.business_state == "open":
            if self.has_employee and self.is_standby:
                self.idle = self.standby_image.convert_alpha()
                self.hovered = self.standby_image.convert_alpha()
            else:
                self.idle = self.states["idle"].convert_alpha()
                self.hovered = self.states["idle"].convert_alpha()

        elif self.business_state == "closed":
            self.is_standby = True
            self.is_serving = False

            self.clear_queue()
            self.idle = self.states["closed"].convert_alpha()
            self.hovered = self.states["closed"].convert_alpha()

        self.hovered.blit(self.outline, (0, 0))

    def serve_customer(self, *args):
        if len(self.queue) == 0:
            return

        if len(args) > 0:
            self.main.tracker.increment_tracker("serve_manual")

        if self.queue[0].is_standing:
            self.served_count += 1
            self.queue.pop(0).serve()

            for customer in self.queue:
                customer.queue_move(-1)

            self.main.tracker.increment_tracker("serve_customer")

    def clear_queue(self):
        # Free the queue
        for customer in self.queue:
            customer.leave()
        self.queue = []

    def fetch_sprite(self, name):
        sprite = self.employee_json["frames"][name]["frame"]
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        image.blit(self.employee_spritesheet, (0, 0), (x, y, width, height))
        self.rect = image.get_rect()
        return image.convert_alpha()

    def generate_income(self, animation=True):
        if animation:
            self.main.play_random_coin_sfx()

        level = self.progress["businesses"][self.progress["last_location"]][
            self.name_code
        ]["level"]
        income_range = self.business_data["income_per_customer_range"]
        income_amp = self.scene.main.data.upgrade[str(level)][
            "income_per_customer_range"
        ]
        income_range = [irange * iamp for irange, iamp in zip(income_range, income_amp)]

        probability_weight = random.choices(
            population=[0.5, 0.7, 0.8, 0.9, 1.0],
            weights=[0.5, 0.2, 0.2, 0.05, 0.05],
        )[0]
        delta_range = income_range[1] - income_range[0]
        income_range[1] = delta_range * probability_weight + income_range[0]

        self.income_step = 0.25  # nudge every atomic value to 25 cents
        self.income_range = (
            round(income_range[0] / self.income_step),
            round(income_range[1] / self.income_step),
        )
        self.current_income = (
            random.randint(self.income_range[0], self.income_range[1])
            * self.income_step
        )

        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "sales"
        ] += self.current_income
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "lifetime_sales"
        ] += self.current_income
        self.progress["businesses"][self.progress["last_location"]][self.name_code][
            "current_operation_sales"
        ] += self.current_income

        if animation:
            # Setting the income animation
            self.reset_income_display()
            self.income_message.set_message([f"+P{self.current_income:,.2f}"])
            self.income_visible = True

        return self.current_income

    def earnings_calculation(self):
        if not self.progress["businesses"][self.progress["last_location"]][
            self.name_code
        ]["has_employee"]:
            return 0.0

        last_visited_string = self.progress["businesses"][self.scene.location][
            "last_visited"
        ]
        time_until_closed_string = self.progress["businesses"][self.scene.location][
            self.name_code
        ]["open_until"]
        # print(f"{self.name_code} earnings calculation")
        # print(f"last_visited_string: {last_visited_string}")
        # print(f"time_until_closed_string: {time_until_closed_string}")

        if last_visited_string != "" and time_until_closed_string != "":
            current_in_game_time = self.scene.time.time

            last_visited = datetime.strptime(
                last_visited_string, self.scene.time.format
            )
            time_until_closed = datetime.strptime(
                time_until_closed_string, self.scene.time.format
            )

            real_life_seconds_difference = round(
                (current_in_game_time - last_visited).seconds
                / self.scene.time.second_ratio
            )
            real_life_seconds_before_closed_difference = round(
                (time_until_closed - last_visited).seconds
                / self.scene.time.second_ratio
            )

            simulation_seconds = min(
                real_life_seconds_difference, real_life_seconds_before_closed_difference
            )
            time_after_simulated_seconds = last_visited + timedelta(
                seconds=simulation_seconds * self.scene.time.second_ratio
            )
            # print(f"simulation_seconds: {simulation_seconds}")

            customers_spawned = 0
            if time_after_simulated_seconds.hour < last_visited.hour:
                hours_span = [hour for hour in range(last_visited.hour, 24)]
                hours_past_midnight = [
                    hour for hour in range(0, time_after_simulated_seconds.hour + 1)
                ]
                hours_span += hours_past_midnight
            else:
                hours_span = [
                    hour
                    for hour in range(
                        last_visited.hour, time_after_simulated_seconds.hour + 1
                    )
                ]
            spawn_chance_per_second = 1 / (
                self.scene.main.data.meta["crowd_spawn_timeout"] / 1000
            )

            for hour in hours_span:
                npc_spawn_rate = self.scene.main.data.crowd_statistics[
                    self.scene.location
                ][hour]
                customer_spawn_rate = self.scene.main.data.customer_statistics[
                    self.scene.location
                ][hour]
                customer_spawn_rate = int(
                    customer_spawn_rate / self.scene.total_location_businesses
                )
                spawn_chances = 60

                if len(hours_span) == 1:
                    spawn_chances = (
                        time_after_simulated_seconds.minute - last_visited.minute
                    )
                else:
                    if hour == hours_span[-1]:
                        spawn_chances = time_after_simulated_seconds.minute
                    elif hour == hours_span[0]:
                        spawn_chances = spawn_chances - last_visited.minute

                hourly_customers = 0
                converted_chances_per_hour = int(
                    ((spawn_chances / 60) * self.scene.time.seconds_per_hour)
                    * spawn_chance_per_second
                )
                for chance_randomness_simulation in range(converted_chances_per_hour):
                    random_npc_spawn_value = random.randint(0, 100)
                    if random_npc_spawn_value <= npc_spawn_rate:
                        random_customer_spawn_value = random.randint(0, 100)
                        if random_customer_spawn_value <= customer_spawn_rate:
                            hourly_customers += 1

                customers_spawned += min(hourly_customers, self.queue_limit)

            # print(f"Income generated {customers_spawned} times.\n")
            total_income = 0.0
            for income_generation in range(customers_spawned):
                total_income += self.generate_income(animation=False)
                self.main.tracker.increment_tracker("serve_customer")

            return total_income

        return 0.0

    def __str__(self):
        return f"{self.name_code}: {len(self.queue)}/{self.queue_limit} Served customers: {self.served_count}"
