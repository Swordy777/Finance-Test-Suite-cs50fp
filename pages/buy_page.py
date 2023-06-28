from .base_page import BasePage
from .locators import BuyPageLocators


class BuyPage(BasePage):
    """
    Buy Page POM.
    Contains methods for interacting with elements on the Buy page
    """
    
    def symbol_input(self):
        """Returns stock symbol input"""

        return self.retrieve_element_if_present(*BuyPageLocators.SHARES_SYMBOL_INPUT)
    

    def amount_input(self):
        """Returns amount input object"""

        return self.retrieve_element_if_present(*BuyPageLocators.SHARES_AMOUNT_INPUT)
        

    def buy_button(self):
        """Returns buy button object"""

        return self.retrieve_element_if_present(*BuyPageLocators.BUY_BUTTON)
    

    def buy_stock(self, stock, amount):
        """Fills stock symbol input and amount input with given values and presses the buy button"""
        
        self.fill_input(self.symbol_input(), stock)
        self.fill_input(self.amount_input(), amount)
        self.buy_button().click()


    # Methods below aren't the best design, but we will leave it like this for now
    
    def more_symbol_inputs(self):
        """Returns a list of elements that could match the locator for stock symbol input"""

        return self.retrieve_multiple_elements_if_present(*BuyPageLocators.SHARES_SYMBOL_INPUT)
    

    def more_amount_inputs(self):
        """Returns a list of elements that could match the locator for amount input"""

        return self.retrieve_multiple_elements_if_present(*BuyPageLocators.SHARES_AMOUNT_INPUT)
    

    def more_buy_buttons(self):
        """Returns a list of elements that could match the locator for buy button"""

        return self.retrieve_multiple_elements_if_present(*BuyPageLocators.BUY_BUTTON)