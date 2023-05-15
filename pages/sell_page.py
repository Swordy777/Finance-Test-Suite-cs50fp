from selenium.webdriver.support.select import Select

from .base_page import BasePage
from .locators import SellPageLocators

class SellPage(BasePage):
    def symbol_input(self):
        symbol_input = self.retrieve_element_if_present(*SellPageLocators.SHARES_LIST)
        if symbol_input is not None:
            symbol_input = Select(symbol_input)
        return symbol_input
    
    def symbol_input_default_option(self):
        default_option = self.retrieve_element_if_present(*SellPageLocators.SHARES_LIST_DEFAULT_OPTION)
        return default_option

    def amount_input(self):
        amount_input = self.retrieve_element_if_present(*SellPageLocators.SHARE_AMOUNT_INPUT)
        return amount_input
    
    def sell_button(self):
        sell_button = self.retrieve_element_if_present(*SellPageLocators.SELL_BUTTON)
        return sell_button

    def press_sell_button(self):
        self.sell_button().click()

    def sell_stock(self, stock, amount):
        self.symbol_input().select_by_value(stock)
        self.fill_input(self.amount_input(), amount)
        self.press_sell_button()

    def add_value_to_default_select_option(self, value):
        symbol_input = self.symbol_input_default_option()
        if symbol_input is not None:
            js_script = """
            let elm = arguments[0]
            let value = arguments[1]
            if (elm.hasAttribute("disabled"))
            {
                elm.removeAttribute("disabled")
            }
            elm.setAttribute("value", value)
            """
            self.browser.execute_script(js_script, symbol_input, value)