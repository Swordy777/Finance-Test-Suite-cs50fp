from .base_page import BasePage
from .locators import QuotePageLocators

class QuotePage(BasePage):
    def quote_input(self):
        quote_input = self.retrieve_element_if_present(*QuotePageLocators.SHARE_SYMBOL_INPUT)
        return quote_input
    
    def quote_button(self):
        quote_button = self.retrieve_element_if_present(*QuotePageLocators.QUOTE_BUTTON)
        return quote_button
    
    def quote_result(self):
        quote_result = self.retrieve_element_if_present(*QuotePageLocators.SHARE_QUOTE_RESULT)
        return quote_result

    def fill_quote_input(self, text):
        self.fill_input(self.quote_input(), text)

    def press_quote_button(self):
        self.quote_button().click()