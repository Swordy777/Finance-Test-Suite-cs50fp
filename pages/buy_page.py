from .base_page import BasePage
from .locators import BuyPageLocators

class BuyPage(BasePage):
    def symbol_input(self):
        symbol_input = self.retrieve_element_if_present(*BuyPageLocators.SHARE_SYMBOL_INPUT)
        return symbol_input
    
    def amount_input(self):
        amount_input = self.retrieve_element_if_present(*BuyPageLocators.SHARE_AMOUNT_INPUT)
        return amount_input
    
    def buy_button(self):
        buy_button = self.retrieve_element_if_present(*BuyPageLocators.BUY_BUTTON)
        return buy_button

    def press_buy_button(self):
        self.buy_button().click()

    def buy_stock(self, stock, amount):
        self.fill_input(self.symbol_input(), stock)
        self.fill_input(self.amount_input(), amount)
        self.press_buy_button()

