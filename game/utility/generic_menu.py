"""
Menu behavior: 
    This will be called as part of a larger objects group. Which is
why it doesn't contain a run() function or main loop for itself. The process
is that it will be called individually and will accept event parameters only
and update in conjuction to its parent window that handles all the objects.

Mostly it will be thrown in another button function as a callback as follows:

def business_callback(self, *args):
    self.business_menu.set_data(args[0])
    self.business_menu.enable = True

Then, the identification to divert game events is if the menu is enabled during
    the parent's mainloop:

# Menu overlays
self.business_menu.update()

# Event processing
for event in pygame.event.get():
    if self.business_menu.enable:
        self.business_menu.handle_event(event)
"""
from game.sprite.menu_background import MenuBackground

import pygame


class GenericMenu:
    """
    Base class for in-game menu system modules. Provides overlay non-stopping
    menu that makes the game run in the background, or also can be used dynamically
    in simulation-stopping scenarios.
    """

    def __init__(self, main) -> None:
        self.main = main
        self.screen = self.main.screen
        self.enable = False

        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tooltips = pygame.sprite.Group()

        # Screen objects
        self.background = MenuBackground(
            self.main.screen, 0.75, image=self.main.data.meta_images["menu_background"]
        )
        self.canvas_rect = self.background.rect

        # Buttons, Messages here

        # Button hierarchy

    def set_button_states(self):
        pass

    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        pass

    def set_data(self):
        self.clear()
        self.background.add(self.objects, self.buttons)
        self.background.enable = True

    def handle_event(self, event):
        if not self.enable:
            return

        if self.main.response_menu.enable:
            self.main.response_menu.handle_event(event)

        elif self.main.confirm_menu.enable:
            self.main.confirm_menu.handle_event(event)

        else:
            if event.type == pygame.QUIT:
                # Closing the game properly
                self.main.close_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.background.enable = False

            elif event.type == pygame.MOUSEMOTION:
                for button in self.hoverable_buttons:
                    button.check_hovered(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        button.check_clicked(mouse_pos)

        if not self.background.enable:
            for button in self.hoverable_buttons:
                button.state = "idle"
                button.set_image_and_rect()
            self.close()

    def update(self):
        if not self.enable:
            return

        if self.background.enable:
            # Updating the data
            self.update_data()

            # Screen dimming
            self.main.display_surface.set_alpha(128)
            self.main.screen.blit(self.main.display_surface, (0, 0))
            self.objects.update()

            for button in self.tooltips:
                button.display_tooltips()

            # Checking if menus will be displaying
            self.main.confirm_menu.update()
            self.main.response_menu.update()

    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()

    def close(self):
        self.clear()
        self.enable = False
        self.main.sliding_menu.has_active_module = False
