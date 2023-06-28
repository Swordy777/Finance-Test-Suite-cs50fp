from selenium.webdriver.support.select import Select

from .base_page import BasePage
from .locators import SellPageLocators


class SellPage(BasePage):
    """
    Sell Page POM.
    Contains methods for interacting with elements on the Sell page
    """

    def symbol_select(self):
        """Returns stock symbol input as Selenium's 'Select' object"""

        symbol_select = self.retrieve_element_if_present(*SellPageLocators.SHARES_LIST)
        if symbol_select is not None:
            symbol_select = Select(symbol_select)
        return symbol_select


    def symbol_select_default_option(self):
        """Returns stock symbol select's default option (first one)"""

        return self.retrieve_element_if_present(*SellPageLocators.SHARES_LIST_DEFAULT_OPTION)


    def amount_input(self):
        """Returns amount input object"""

        return self.retrieve_element_if_present(*SellPageLocators.SHARE_AMOUNT_INPUT)


    def sell_button(self):
        """Returns sell button"""

        return self.retrieve_element_if_present(*SellPageLocators.SELL_BUTTON)


    def sell_stock(self, stock, amount):
        """Picks stock input, fills amount input with given values and presses the sell button"""

        self.symbol_select().select_by_value(str(stock))
        self.fill_input(self.amount_input(), amount)
        self.sell_button().click()


    def add_value_to_default_select_option(self, value):
        """
        Adds/changes an elements 'value' attribute to given value
        Also deletes element's 'disabled' attribute 
        """

        symbol_select = self.symbol_select_default_option()
        if symbol_select is not None:
            js_script = """
            let elm = arguments[0]
            let value = arguments[1]
            if (elm.hasAttribute("disabled"))
            {
                elm.removeAttribute("disabled")
            }
            elm.setAttribute("value", value)
            """
            self.browser.execute_script(js_script, symbol_select, value)


    # Methods below aren't the best design, but we will leave it like this for now

    def more_symbol_selects(self):
        """Returns a list of elements that could match the locator for stock symbol_select"""

        return self.retrieve_multiple_elements_if_present(*SellPageLocators.SHARES_LIST)


    def more_amount_inputs(self):
        """Returns a list of elements that could match the locator for amount input"""

        return self.retrieve_multiple_elements_if_present(*SellPageLocators.SHARE_AMOUNT_INPUT)


    def more_sell_buttons(self):
        """Returns a list of elements that could match the locator for sell button"""

        return self.retrieve_multiple_elements_if_present(*SellPageLocators.SELL_BUTTON)