from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button
import pygame

from datetime import datetime, timedelta
from pprint import pprint


class BusinessMenu():
    """
    This class will handle menu that is related to businesses when they are
    clicked. This will contain the details, buttons to manage the business
    and the profits and loss statistics.
    """
    def __init__(self, main, time, location):
        self.enable = False
        
        self.main = main
        self.screen = self.main.screen
        self.data = None
        self.time = time
        self.location = location
        
        self.business_cost = None
        self.daily_expense = None
        self.employee_cost = None
        self.income_per_customer = None
        
        # Sprite groups
        self.objects = pygame.sprite.Group()
        self.hoverable_buttons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        
        # Screen objects
        self.background = MenuBackground(
            self.screen, 0.75,
            image=self.main.data.meta_images["menu_background"])
        
        self.canvas_rect = self.background.rect
        self.business_title_message = Message(
            self.screen, 
            [""],
            self.main.data.large_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.09) + self.canvas_rect.y
            )
        )
        self.business_tier_and_size = Message(
            self.screen, 
            [""],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.15) + self.canvas_rect.y
            )
        )
        self.left_side_description = Message(
            self.screen, 
            [""],
            self.main.data.medium_font,
            self.main.data.colors["brown"],
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.035) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.2) + self.canvas_rect.y
            )
        )
        self.collect_sales_button = Button(
            self.screen,
            self.collect_sales_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.105) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["collect_sales_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["collect_sales_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["collect_sales_button_disabled"].convert_alpha()
            }
        )
        self.purchase_business_button = Button(
            self.screen,
            self.purchase_business_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.105) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["purchase_business_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["purchase_business_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["purchase_business_button_disabled"].convert_alpha()
            }
        )
        self.start_business_button = Button(
            self.screen,
            self.start_business_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.325) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["start_business_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["start_business_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["start_business_button_disabled"].convert_alpha()
            }
        )
        self.hire_employee_button = Button(
            self.screen,
            self.hire_employee_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.475) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["hire_employee_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["hire_employee_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["hire_employee_button_disabled"].convert_alpha()
            }
        )
        self.sell_business_button = Button(
            self.screen,
            self.sell_business_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.625) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["sell_business_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["sell_business_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["sell_business_button_disabled"].convert_alpha()
            }
        )
        self.close_business_button = Button(
            self.screen,
            self.close_business_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.775) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["close_business_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["close_business_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["close_business_button_disabled"].convert_alpha()
            }
        )
        
        # Screen dimming
        self.main.display_surface.set_alpha(128)
        
        
    def get_sales(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"]
    
    
    def clear_sales(self):
        self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"] = 0
        
        
    def purchase_business(self):
        self.main.data.progress["cash"] -= self.data.business_data["initial_cost"]
        self.main.data.progress["businesses"][self.location][self.data.name_code]["ownership"] = True
        self.main.data.progress["businesses"][self.location][self.data.name_code]["date_acquired"] = \
            datetime.strftime(datetime.now(), "%Y/%m/%d, %H:%M:%S.%f")
        self.data.set_business_state("open")
        
    
    def check_if_business_is_owned(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["ownership"]
        
        
    def collect_sales_button_callback(self, *args):
        self.collect_sales_button.set_is_disabled(True)
        self.main.data.progress["cash"] += self.main.data.progress["businesses"][self.location][self.data.name_code]["sales"]
        self.clear_sales()
        
    
    def purchase_business_button_callback(self, *args):
        business_cost = self.data.business_data["initial_cost"]
        bank_balance = self.main.data.progress["cash"]
        assumed_balance = bank_balance - business_cost
        
        if bank_balance >= business_cost:
            self.main.confirm_menu.set_message_and_callback(
                ["Are you sure you want",
                " to purchase the business?", "",
                "Your new balance",
                f"will be: P{assumed_balance:,.2f}"],
                self.purchase_business
            )
            self.main.confirm_menu.run()
        else:
            self.main.response_menu.set_message(
                ["You do not have ", 
                 "enough balance on", 
                 "your bank account.", "",
                 f"You still need P{abs(assumed_balance):,.2f}."])
            self.main.response_menu.run()
            
            
    def hire_employee_button_callback(self, *args):
        print("hire employee clicked")
        
    
    def start_business_button_callback(self, *args):
        print("start business clicked")
        
        
    def sell_business_button_callback(self, *args):
        print("sell business clicked")
        
    
    def close_business_button_callback(self, *args):
        print("close business clicked")
            
        
    def set_button_states(self):
        if self.check_if_business_is_owned():
            self.purchase_business_button.visible = False
            self.collect_sales_button.visible = True
        else:
            self.purchase_business_button.visible = True
            self.collect_sales_button.visible = False
        
        if self.get_sales() <= 0:
            self.collect_sales_button.set_is_disabled(True)
        else:
            self.collect_sales_button.set_is_disabled(False)
            
            
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        current_income = ""
        if self.check_if_business_is_owned():
            date_acquired = self.main.data.progress["businesses"][self.location][self.data.name_code]["date_acquired"][:-7]
            sales = f"P {self.get_sales():,.2f}"
            if self.get_sales() > 0:
                current_income = f" +(P {self.data.current_income:,.2f})"
            lifetime_sales = f"P {self.main.data.progress['businesses'][self.location][self.data.name_code]['lifetime_sales']:,.2f}"
        else:
            date_acquired = "N/A"
            sales = "N/A"
            lifetime_sales = "N/A"
        
        self.left_side_description.set_message([
            f"==================================================",
            f"Open until:",
            f"  1:52 AM, April 28, 2022",
            f"==================================================",
            f"Business cost",
            f"  {self.business_cost}",
            f"Operation cost: (8 hours)",
            f"  {self.daily_expense} - Status: Not operating",
            f"Employment cost: (8 hours):",
            f"  {self.employee_cost} - Status: Not operating",
            f"Gross income per customer:",
            f"  {self.income_per_customer}",
            f"Date of acquisition:",
            f"  {date_acquired}",
            f"==================================================",
            f"Sales:",
            f"  {sales}{current_income}",
            f"Lifetime sales:",
            f"  {lifetime_sales}",
            f"==================================================",
        ])
        
        self.set_button_states()
        
        
    def set_data(self, data):
        self.data = data
        
        self.clear()
        self.background.add(self.objects, self.buttons)
        
        # Data set
        self.business_title_message.set_message([self.data.business_data["name"]])
        self.business_tier_and_size.set_message([
            f"Tier {self.main.data.category[self.data.name_code]['tier']} - "
            f"{self.main.data.category[self.data.name_code]['size']} Business"
        ])
        
        # Attributes that must be shown regardless of ownership
        self.business_cost = f"P {self.data.business_data['initial_cost']:,.2f}"
        self.daily_expense = f"P {self.data.business_data['daily_expenses']:,.2f}"
        self.employee_cost = f"P {self.data.business_data['employee_cost']:,.2f}"
        self.income_per_customer = \
            f"P {self.data.business_data['income_per_customer_range'][0]:,.2f} - " \
            f"P {self.data.business_data['income_per_customer_range'][1]:,.2f}"
        
        # Updating the data
        self.update_data()
        
        # Object add
        self.business_title_message.add(self.objects)
        self.business_tier_and_size.add(self.objects)
        self.left_side_description.add(self.objects)
        self.collect_sales_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.purchase_business_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.start_business_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.hire_employee_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.sell_business_button.add(self.objects, self.buttons, self.hoverable_buttons)
        self.close_business_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
        self.background.enable = True
        
    
    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()
        
        
    def handle_event(self, event):
        if not self.enable:
            return
    
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
            self.close()
        
        
    def update(self):
        if not self.enable:
            return
        
        if self.background.enable:
            # Updating the data
            self.update_data()
            
            self.screen.blit(self.main.display_surface, (0, 0)) 
            self.objects.update() 
        
        
    def close(self):
        self.clear()
        self.enable = False
