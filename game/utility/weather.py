from datetime import datetime
import pygame
import random


class Weather:
    """Class to control unpredictable weather events in the game such as:
    - Rainfall
    - Heat wave
    """

    def __init__(self, scene):
        self.main = scene.main
        self.current_month = scene.time.time.month

        # Clouds assets
        self.cloud_images = [
            self.main.data.scene[f"cloud_{index}"].convert_alpha() for index in range(3)
        ]
        self.cloud_images = list(
            map(
                lambda cloud: pygame.transform.scale(
                    cloud,
                    (
                        int(cloud.get_rect().width * 0.75),
                        int(cloud.get_rect().height * 0.75),
                    ),
                ).convert_alpha(),
                self.cloud_images,
            )
        )

        # Rainfall animation
        self.rainfall_surface = self.main.data.scene["weather_rainfall"]["sheet"]
        self.rainfall_data = self.main.data.scene["weather_rainfall"]["data"]

        self.rainfall_sprites = []
        for index in range(len(self.rainfall_data["frames"])):
            self.rainfall_sprites.append(
                self.fetch_sprite(f"weather_rainfall_{index + 1}.png")
            )

        # Heat wave assets
        self.heatwave_image = self.main.data.scene["weather_heatwave"].convert_alpha()

        # Debug only
        # self.weather = {
        #     # January
        #     "1": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # February
        #     "2": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # March
        #     "3": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # April
        #     "4": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # May
        #     "5": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # June
        #     "6": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # July
        #     "7": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # August
        #     "8": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # September
        #     "9": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # October
        #     "10": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # November
        #     "11": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        #     # December
        #     "12": {
        #         "rainfall": 70,
        #         "heatwave": 65,
        #     },
        # }

        self.weather = {
            # January
            "1": {
                "rainfall": 30,
                "heatwave": 20,
            },
            # February
            "2": {
                "rainfall": 30,
                "heatwave": 30,
            },
            # March
            "3": {
                "rainfall": 30,
                "heatwave": 40,
            },
            # April
            "4": {
                "rainfall": 30,
                "heatwave": 60,
            },
            # May
            "5": {
                "rainfall": 40,
                "heatwave": 70,
            },
            # June
            "6": {
                "rainfall": 50,
                "heatwave": 40,
            },
            # July
            "7": {
                "rainfall": 60,
                "heatwave": 30,
            },
            # August
            "8": {
                "rainfall": 70,
                "heatwave": 20,
            },
            # September
            "9": {
                "rainfall": 60,
                "heatwave": 20,
            },
            # October
            "10": {
                "rainfall": 50,
                "heatwave": 20,
            },
            # November
            "11": {
                "rainfall": 40,
                "heatwave": 20,
            },
            # December
            "12": {
                "rainfall": 50,
                "heatwave": 20,
            },
        }

        self.states = [
            "regular",
            "rainfall",
            "heatwave",
        ]

        self.constraints = {
            "rainfall": [4, 22],
            "heatwave": [9, 17],
        }

        self.span = {
            "rainfall": [3, 6],
            "heatwave": [2, 4],
        }

        self.time_format = "%Y/%m/%d, %H:%M:%S.%f"

        self.reconstruct(scene)

    def reconstruct(self, scene):
        self.main = scene.main
        self.game_fps = self.main.data.setting["fps"]
        self.game_tick = 1 / self.game_fps

        # Current probability
        self.chances = self.weather[str(self.current_month)]

        # Logical variables
        self.max_width = self.main.data.setting["game_width"]
        self.state = self.main.data.progress["weather"]["state"]

        # Floating clouds
        self.max_clouds = 4
        self.starting_point_divisions = 8
        self.x_starting_points = []

        starting_unit = int(self.max_width / self.starting_point_divisions)
        for parts in range(self.starting_point_divisions):
            self.x_starting_points.append(
                (starting_unit - int(starting_unit / 2)) + (starting_unit * parts)
            )

        # Clouds assets
        self.cloud_objects = {}
        self.cloud_fps = 1 / self.game_fps
        self.cloud_speed = self.game_tick * (self.game_fps * self.cloud_fps)
        self.cloud_tick = 0

        spaces_taken = []
        for index in range(self.max_clouds):
            space = random.choice(self.x_starting_points)
            while space in spaces_taken:
                space = random.choice(self.x_starting_points)
            spaces_taken.append(space)
            self.cloud_objects[str(index)] = {
                "image": random.choice(self.cloud_images),
                "direction": random.choice(["left", "right"]),
                "coordinates": [space, 0],
                "speed": random.randint(1, 2),
            }

        # Rainfall animation
        self.rainfall_index = 0

        self.rainfall_fps = 0.083
        self.rainfall_tick = 0

    def trigger_weather(self):
        # To be called at 12AM to schedule a new weather o remain regular
        self.current_month = self.main.scene_window.time.time.month
        data = self.weather[str(self.current_month)]

        priority = "rainfall" if data["rainfall"] > data["heatwave"] else "heatwave"
        if priority == "rainfall":
            sequence = ["rainfall", "heatwave"]
        elif priority == "heatwave":
            sequence = ["heatwave", "rainfall"]

        new_weather = "regular"
        for weather in sequence:
            chance = random.randint(0, 100)
            if data[weather] >= chance:
                new_weather = weather
                break

        if new_weather == "regular":
            self.main.data.progress["weather"] = {
                "state": "regular",
                "new_weather": "",
                "start": "",
                "end": "",
            }
            self.main.scene_window.update_data()
        else:
            weather_span = self.span[new_weather]
            span = random.randint(weather_span[0], weather_span[1])

            weather_constraint = self.constraints[new_weather]
            value = random.randint(weather_constraint[0], weather_constraint[1])

            start = None
            end = None

            if value + span <= weather_constraint[1]:
                start = value
                end = value + span
            elif value - span >= weather_constraint[0]:
                start = value - span
                end = value

            assert start
            assert end

            start_time: datetime = self.main.scene_window.time.time.replace(
                hour=start, minute=0, second=0
            )
            end_time: datetime = self.main.scene_window.time.time.replace(
                hour=end, minute=0, second=0
            )

            self.main.data.progress["weather"]["new_weather"] = new_weather
            self.main.data.progress["weather"]["start"] = start_time.strftime(
                self.time_format
            )
            self.main.data.progress["weather"]["end"] = end_time.strftime(
                self.time_format
            )
            self.main.scene_window.update_data()

            if self.main.data.progress["tutorial_shown"]:
                notification_format = "%I:%M %p"
                self.main.response_menu.queue_message(
                    [
                        f"Weather Update:",
                        f"",
                        f"{new_weather} Warning",
                        f"From {start_time.strftime(notification_format)}",
                        f"To {end_time.strftime(notification_format)}",
                    ]
                )

    def update_weather(self):
        # To be called hourly to check weather changes
        if self.main.data.progress["weather"]["new_weather"] == "":
            return

        current_time = self.main.scene_window.time.time
        start_time = datetime.strptime(
            self.main.data.progress["weather"]["start"], self.time_format
        )
        end_time = datetime.strptime(
            self.main.data.progress["weather"]["end"], self.time_format
        )

        if current_time >= start_time and current_time <= end_time:
            self.main.data.progress["weather"]["state"] = self.main.data.progress[
                "weather"
            ]["new_weather"]
        else:
            self.main.data.progress["weather"]["state"] = "regular"

        self.state = self.main.data.progress["weather"]["state"]
        self.main.scene_window.update_data()

    def fetch_sprite(self, name):
        sprite = self.rainfall_data["frames"][name]["frame"]
        x, y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        image.blit(self.rainfall_surface, (0, 0), (x, y, width, height))
        return image.convert_alpha()

    def render_clouds(self):
        # Moving Clouds rendering
        for cloud in self.cloud_objects:
            cloud_data = self.cloud_objects[cloud]
            self.main.screen.blit(cloud_data["image"], cloud_data["coordinates"])

        # Cloud movement
        self.cloud_tick += self.game_tick
        if self.cloud_tick >= self.cloud_speed:
            self.cloud_tick = 0

            for cloud in self.cloud_objects:
                reset = False
                if self.cloud_objects[cloud]["direction"] == "left":
                    self.cloud_objects[cloud]["coordinates"][0] -= self.cloud_objects[
                        cloud
                    ]["speed"]

                    rect = self.cloud_objects[cloud]["image"].get_rect()
                    reset_point = 0 - rect.width

                    if self.cloud_objects[cloud]["coordinates"][0] <= reset_point:
                        reset = True

                if self.cloud_objects[cloud]["direction"] == "right":
                    self.cloud_objects[cloud]["coordinates"][0] += self.cloud_objects[
                        cloud
                    ]["speed"]

                    rect = self.cloud_objects[cloud]["image"].get_rect()
                    reset_point = self.max_width + rect.width

                    if self.cloud_objects[cloud]["coordinates"][0] >= reset_point:
                        reset = True

                if reset:
                    direction = random.choice(["left", "right"])
                    self.cloud_objects[cloud]["direction"] = direction
                    self.cloud_objects[cloud]["image"] = random.choice(
                        self.cloud_images
                    )

                    width = self.cloud_objects[cloud]["image"].get_rect().width
                    if direction == "left":
                        coordinates = [self.max_width + width, 0]
                    elif direction == "right":
                        coordinates = [0 - width, 0]
                    self.cloud_objects[cloud]["coordinates"] = coordinates

    def update(self):
        if self.state == "rainfall":
            self.main.screen.blit(self.rainfall_sprites[self.rainfall_index], (0, 0))

            self.rainfall_tick += self.game_tick
            if self.rainfall_tick >= self.rainfall_fps:
                self.rainfall_tick = 0

                self.rainfall_index = (self.rainfall_index + 1) % len(
                    self.rainfall_sprites
                )
        elif self.state == "heatwave":
            self.main.screen.blit(self.heatwave_image, (0, 0))
