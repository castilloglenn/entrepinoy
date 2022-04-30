from game.sprite.menu_background import MenuBackground
from game.sprite.message import Message
from game.sprite.button import Button
import pygame

from datetime import datetime, timedelta
from numerize.numerize import numerize
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
        
        self.sell_back_ratio = 0.5
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
        self.upgrades_button = Button(
            self.screen,
            self.upgrades_button_callback,
            top_left_coordinates=(
                int(self.canvas_rect.width * 0.65) + self.canvas_rect.x,
                int(self.canvas_rect.height * 0.775) + self.canvas_rect.y
            ),
            **{
                "idle" : self.main.data.scene["upgrades_button_idle"].convert_alpha(),
                "outline" : self.main.data.scene["upgrades_button_hovered"].convert_alpha(),
                "disabled" : self.main.data.scene["upgrades_button_disabled"].convert_alpha()
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
        
    
    def start_business(self):
        self.main.data.progress["cash"] -= self.data.business_data["daily_expenses"]
        self.data.set_business_state("open")
        
    
    def hire_employee(self):
        self.main.data.progress["cash"] -= self.data.business_data["employee_cost"]
        self.data.set_employee_status(True)
        

    def sell_business(self):
        business_selling_price = round(self.data.business_data["initial_cost"] * self.sell_back_ratio, 2)
        self.main.data.progress["cash"] += business_selling_price
        self.data.disown_business()
        
    
    def check_if_business_is_owned(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["ownership"]
    
    
    def check_if_business_is_open(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["is_open"]
    
    
    def check_if_employee_is_working(self):
        return self.main.data.progress["businesses"][self.location][self.data.name_code]["has_employee"]
        
        
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
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                ["You do not have ", 
                 "enough balance on", 
                 "your bank account.", "",
                 f"You still need P{abs(assumed_balance):,.2f}."])
            self.main.response_menu.enable = True
        
    
    def start_business_button_callback(self, *args):
        operation_cost = self.data.business_data["daily_expenses"]
        bank_balance = self.main.data.progress["cash"]
        assumed_balance = bank_balance - operation_cost
        
        if bank_balance >= operation_cost:
            self.main.confirm_menu.set_message_and_callback(
                ["Are you sure you",
                "want to start the", 
                "business operation?", "",
                "Your new balance",
                f"will be: P{assumed_balance:,.2f}"],
                self.start_business
            )
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                ["You do not have ", 
                 "enough balance on", 
                 "your bank account.", "",
                 f"You still need P{abs(assumed_balance):,.2f}."])
            self.main.response_menu.enable = True
            
            
    def hire_employee_button_callback(self, *args):
        employement_cost = self.data.business_data["employee_cost"]
        bank_balance = self.main.data.progress["cash"]
        assumed_balance = bank_balance - employement_cost
        
        if bank_balance >= employement_cost:
            self.main.confirm_menu.set_message_and_callback(
                ["Are you sure you want",
                "to hire an employee", 
                "for the business?", "",
                "Your new balance",
                f"will be: P{assumed_balance:,.2f}"],
                self.hire_employee
            )
            self.main.confirm_menu.enable = True
        else:
            self.main.response_menu.set_message(
                ["You do not have ", 
                 "enough balance on", 
                 "your bank account.", "",
                 f"You still need P{abs(assumed_balance):,.2f}."])
            self.main.response_menu.enable = True
        
        
    def sell_business_button_callback(self, *args):
        business_selling_price = round(self.data.business_data["initial_cost"] * self.sell_back_ratio, 2)
        bank_balance = self.main.data.progress["cash"]
        assumed_balance = bank_balance + business_selling_price
        
        self.main.confirm_menu.set_message_and_callback(
            ["Are you sure you want",
            "to sell the business?", "",
            f"The price will be {self.sell_back_ratio * 100:.0f}% of", 
            f"its original price. (P{business_selling_price:,.2f})",
            f"Your New Balance: P{assumed_balance:,.2f}"],
            self.sell_business
        )
        self.main.confirm_menu.enable = True
        
    
    def upgrades_button_callback(self, *args):
        print("upgrades clicked")
            
        
    def set_button_states(self):
        if self.check_if_business_is_owned():
            self.purchase_business_button.visible = False
            self.collect_sales_button.visible = True
            self.sell_business_button.set_is_disabled(False)
            
            # For the collect sales button
            if self.get_sales() <= 0:
                self.collect_sales_button.set_is_disabled(True)
            else: # Make the button working
                self.collect_sales_button.set_is_disabled(False)
                
            # For employee hiring button
            if self.check_if_employee_is_working():
                self.hire_employee_button.set_is_disabled(True)
            else: # No employee
                self.hire_employee_button.set_is_disabled(False)
            
            # For start business button and close business button
            if self.check_if_business_is_open():
                self.start_business_button.set_is_disabled(True)
                self.upgrades_button.set_is_disabled(False)
            else: # closed
                self.start_business_button.set_is_disabled(False)
                self.hire_employee_button.set_is_disabled(True)
                self.upgrades_button.set_is_disabled(True)
        else:
            self.purchase_business_button.visible = True
            self.collect_sales_button.visible = False
            
            self.start_business_button.set_is_disabled(True)
            self.hire_employee_button.set_is_disabled(True)
            self.sell_business_button.set_is_disabled(True)
            self.upgrades_button.set_is_disabled(True)
            
            
    def parse_seconds_to_data(self, seconds):
        hour = 0
        minute = 0
        
        if seconds >= 60:
            hour = 0
            minute = seconds // 60
            
        if seconds >= 3600:
            hour = seconds // 3600
            minute = (seconds % 3600) // 60
            
        return f"{hour} Hour{'s' if hour > 1 else ''} " \
            f"{minute} Minute{'s' if minute > 1 else ''} "
            
            
    def update_data(self):
        # This will be called in conjunction with the screen update to always
        #   make the details in the business update and buttons will be enabled
        #   when a sale is made and etc.
        current_income = ""
        if self.check_if_business_is_owned():
            open_until_value = self.main.data.progress['businesses'][self.location][self.data.name_code]['open_until']
            if open_until_value == "":
                open_until = "Business is closed"
            else:
                total_seconds = (datetime.strptime(open_until_value, self.time.format) - self.time.time).seconds
                open_until = self.parse_seconds_to_data(total_seconds)
            
            date_acquired_object = datetime.strptime(
                self.main.data.progress["businesses"][self.location][self.data.name_code]["date_acquired"],
                self.time.format
            )
            date_acquired = datetime.strftime(date_acquired_object, self.time.date_display_format)
            sales = f"P{numerize(self.get_sales(), 3)}"
            
            if self.get_sales() > 0 and self.data.current_income > 0:
                current_income = f" +(P{numerize(self.data.current_income, 3)})"
            lifetime_sales = f"P{numerize(self.main.data.progress['businesses'][self.location][self.data.name_code]['lifetime_sales'], 3)}"
            
            if self.data.has_employee:
                employed_until = "Employee is working"
            else:
                employed_until = "No employee"
                
            previous_profit = f"P{numerize(self.main.data.progress['businesses'][self.location][self.data.name_code]['last_profit'], 3)}"
            lifetime_profit = f"P{numerize(self.main.data.progress['businesses'][self.location][self.data.name_code]['lifetime_profit'], 3)}"
        else:
            open_until = "N/A"
            date_acquired = "N/A"
            sales = "N/A"
            lifetime_sales = "N/A"
            employed_until = "N/A"
            previous_profit = "N/A"
            lifetime_profit = "N/A"
            
        self.left_side_description.set_message([
            f"==================================================",
            f"Date of acquisition:",
            f"  {date_acquired}",
            f"Business cost:", 
            f"  {self.business_cost}",
            f"Gross income per customer:",
            f"  {self.income_per_customer}",
            f"==================================================",
            f"Operation Cost: {self.daily_expense} ({self.main.data.meta['operating_hours']} Hours)", 
            f"  Status: {open_until}",
            f"",
            f"Employment Cost: {self.employee_cost} ({self.main.data.meta['operating_hours']} Hours)",
            f"  Status: {employed_until}",
            f"==================================================",
            f"Sales:              Lifetime Sales:",
            f"  {sales:7s}{current_income:11s}  {lifetime_sales}",
            f"",
            f"Last Profit:        Lifetime Profit:",
            f"  {previous_profit:18s}  {lifetime_profit}",
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
        self.business_cost = f"P{self.data.business_data['initial_cost']:,.2f}"
        self.daily_expense = f"P{numerize(self.data.business_data['daily_expenses'], 3)}"
        self.employee_cost = f"P{numerize(self.data.business_data['employee_cost'], 3)}"
        self.income_per_customer = \
            f"P{self.data.business_data['income_per_customer_range'][0]:,.2f} to " \
            f"P{self.data.business_data['income_per_customer_range'][1]:,.2f}"
        
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
        self.upgrades_button.add(self.objects, self.buttons, self.hoverable_buttons)
        
        self.background.enable = True
        
    
    def clear(self):
        self.objects.empty()
        self.hoverable_buttons.empty()
        self.buttons.empty()
        
        
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
            self.close()
        
        
    def update(self):
        if not self.enable:
            return
        
        if self.background.enable:
            # Updating the data
            self.update_data()
            
            self.screen.blit(self.main.display_surface, (0, 0)) 
            self.objects.update()
            
            # Checking if menus will be displaying
            self.main.confirm_menu.update()
            self.main.response_menu.update()
        
        
    def close(self):
        self.clear()
        self.enable = False
