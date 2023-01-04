from game.sprite.message import Message

import pygame


class Epilogue:
    """
    This class will present the epilogue sequence based on whether the user have
    successfully finished the game or not. There will be two sequences:
        Good Ending
            1. Epilogue Story (Frames) Presentation Window
            2. End credits scene
        Bad Ending
            1. Epilogue Story (Frames) Presentation Window
    """

    def __init__(self, main) -> None:
        # Setting up the assets
        self.main = main

        # Albums
        self.albums = ["good_ending", "bad_ending"]

        # Data
        self.end_credits = [
            "EntrePinoy",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "From",
            "Me and the Boys",
            "Studios",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "The Development Team",
            "",
            "",
            "",
            "",
            "",
            "Allen Glenn E. Castillo",
            "Lead Developer",
            "System Designer",
            "Sound Designer",
            "",
            "",
            "",
            "Sebastian Raphael B. Garcia",
            "Lead Graphic Artist",
            "Story Writer",
            "QA Tester",
            "",
            "",
            "",
            "Ernest John C. Cabigat",
            "Lead Researcher",
            "Lead Sound Designer",
            "QA Tester",
            "",
            "",
            "",
            "Anjelo Morris O. Felizardo",
            "Graphic Artist",
            "Researcher",
            "QA Tester",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Advisers",
            "",
            "",
            "",
            "",
            "",
            "Mariella R. Leyba, MIT",
            "Technical Adviser",
            "",
            "",
            "",
            "",
            "",
            "Carlo P. Malabanan, MIT",
            "IT PROGRAM COORDINATOR",
            "DEPARTMENT RESEARCH COORDINATOR",
            "Capstone Adviser",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Special Thanks to:",
            "",
            "",
            "",
            "",
            "",
            "Background Music",
            "",
            "",
            "",
            '"Cool Menu Loop"',
            "",
            '"Game Menu Looping"',
            "",
            '"Young Heroes"',
            "",
            '"Happy Endings"',
            "",
            "",
            "",
            "by Eric Matyas",
            "www.soundimage.org",
            "",
            "",
            "",
            "",
            "",
            "Sound Effects",
            "",
            "",
            "",
            '"Coins1-15"',
            "",
            "",
            '"SynthChime1"',
            "",
            "",
            '"UI-Quirky20, 37"',
            "",
            "by Eric Matyas",
            "www.soundimage.org",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "But most importantly",
            "We are highly grateful",
            "To have you as our player",
            "",
            "",
            "",
            "",
            "",
            "Thank you,",
            f"{self.main.data.progress['name']}!",
            "",
            "You're the",
            "best!",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "ENTREPINOY: 2D IDLE BUSINESS",
            "SIMULATION GAME FOR THE STUDENTS",
            "OF BACHELOR OF SCIENCE IN",
            "ENTREPRENEURSHIP IN",
            "CVSU IMUS CAMPUS",
            "",
            "",
            "",
            "",
            "",
            "A Capstone Project",
            "Submitted to the Faculty",
            "of Department Computer Studies",
            "Cavite State University",
            "Imus, Cavite",
            "",
            "",
            "",
            "",
            "",
            "January 2023",
        ]

    def run(self, album):
        assert album in self.albums

        if self.main.data.progress["credits_shown"]:
            return

        pygame.mixer.music.load(self.main.data.music["epilogue"])
        pygame.mixer.music.play(-1)

        self.main.slide_show.set_album(
            album,
            self.main.data.progress["name"],
            self.main.data.progress["gender"],
        )
        self.main.transition.setup_and_fade_out(
            transition_length=2,
            duration_length=self.main.slide_show.get_total_hold(),
            display_image=self.main.slide_show.image,
        )
        self.main.slide_show.run()

        if album == "good_ending":
            self.main.display_surface.set_alpha(255)
            self.canvas_rect = self.main.display_surface.get_rect()
            width = round(self.canvas_rect.height * 1.12)
            limit = -(width * (len(self.end_credits) / 28))
            speed = 0.15  # 1.0 y to zero in 1 second
            frame_unit = (
                1
                / self.main.data.setting["fps"]
                * self.main.data.setting["game_height"]
            )
            decrement = frame_unit * speed
            end_credits_message = Message(
                self.main.screen,
                self.end_credits,
                self.main.data.large_font,
                self.main.data.colors["white"],
                outline_thickness=2,
                center_coordinates=(
                    int(self.canvas_rect.width * 0.5),
                    int(width),
                ),
            )
            while width > limit:
                self.main.screen.blit(self.main.display_surface, (0, 0))
                end_credits_message.update()

                # Position update
                width -= decrement
                end_credits_message.center_coordinates = (
                    int(self.canvas_rect.width * 0.5),
                    int(width),
                )

                # Event processing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # Closing the game properly
                        self.main.close_game()
                        break

                self.main.refresh_display()

        self.main.data.progress["credits_shown"] = True
        pygame.mixer.music.load(self.main.data.music["scene"])
        pygame.mixer.music.play(-1)
