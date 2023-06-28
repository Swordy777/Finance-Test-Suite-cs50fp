from .base_page import BasePage
from .locators import QuotePageLocators


class QuotePage(BasePage):
    """
    Quote Page POM.
    Contains methods for interacting with elements on the Quote page
    """

    def quote_input(self):
        """Returns quote input"""

        return self.retrieve_element_if_present(*QuotePageLocators.SHARE_SYMBOL_INPUT)


    def quote_button(self):
        """Returns quote button"""

        return self.retrieve_element_if_present(*QuotePageLocators.QUOTE_BUTTON)


    def quote_result(self):
        """Returns resulting string with stock info"""

        return self.retrieve_element_if_present(*QuotePageLocators.SHARE_QUOTE_RESULT)


    def get_stock_quote(self, text):
        """Fills quote input and presses the quote button"""

        self.fill_input(self.quote_input(), text)
        self.quote_button().click()


    # Methods below aren't the best design, but we will leave it like this for now

    def more_quote_inputs(self):
        """Returns a list of elements that could match the locator for quote input"""

        return self.retrieve_multiple_elements_if_present(*QuotePageLocators.SHARE_SYMBOL_INPUT)

    def more_quote_buttons(self):
        """Returns a list of elements that could match the locator for quote button"""

        return self.retrieve_multiple_elements_if_present(*QuotePageLocators.QUOTE_BUTTON)