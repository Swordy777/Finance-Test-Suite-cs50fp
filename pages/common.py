from .base_page import BasePage
from .locators import BasePageLocators


class Common(BasePage):
    """
    Common POM.
    Contains methods for interacting with common navigation elements across all pages.
    Is more specific than BasePage()
    """
    
    def get_page_title(self):
        """Returns the page title"""
        
        return self.browser.title


    def get_logout_link(self):
        """Finds and returns the Log out navigation item"""
        
        return self.retrieve_element_if_present(*BasePageLocators.LOGOUT_LINK)


    def get_register_link(self):
        """Finds and returns the Register navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.REGISTER_LINK)


    def get_login_link(self):
        """Finds and returns the Log in navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.LOGIN_LINK)
    

    def get_default_link(self):
        """Finds and returns the link to the Default Page"""

        return self.retrieve_element_if_present(*BasePageLocators.DEFAULT_LINK)
    

    def get_cs50_logo(self):
        """Finds and returns a text representation of the CS50 logo"""

        cs50_logo_parts = self.retrieve_multiple_elements_if_present(*BasePageLocators.CS50_LOGO_PART)
        logo_text = ""
        for each_span_element in cs50_logo_parts:
            logo_text += each_span_element.text
        return logo_text


    def get_quote_navitem(self):
        """Finds and returns the Quote navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.QUOTE_LINK)


    def get_buy_navitem(self):
        """Finds and returns the Buy navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.BUY_LINK)


    def get_sell_navitem(self):
        """Finds and returns the Sell navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.SELL_LINK)
    

    def get_hist_navitem(self):
        """Finds and returns the History navigation item"""

        return self.retrieve_element_if_present(*BasePageLocators.HISTORY_LINK)


    def should_have_nav_items(self):
        """
        Outdated POM method. 
        Was programmed before making the choice to have no asserts in POM methods
        But we will leave it like this for now
        Checks if the page has all the navigation items and returns a list of errors if any occured.
        """
        
        errors = []
        if self.get_quote_navitem() is None:
            errors.append("Couldn't find 'Quote' navigation item")
        if self.get_buy_navitem() is None:
            errors.append("Couldn't find 'Buy' navigation item")
        if self.get_sell_navitem() is None:
            errors.append("Couldn't find 'Sell' navigation item")
        if self.get_hist_navitem() is None:
            errors.append("Couldn't find 'History' navigation item")
        assert not errors, "; ".join(errors)


    def should_not_have_nav_items(self):
        """
        Outdated POM method. 
        Was programmed before making the choice to have no asserts in POM methods
        But we will leave it like this for now
        Checks if the page has no navigation items and returns a list of errors if any occured.
        """

        errors = []
        if self.get_quote_navitem() is not None:
            errors.append("Expected navigation menu to have no 'Quote' navigation item")
        if self.get_buy_navitem() is not None:
            errors.append("Expected navigation menu to have no 'Buy' navigation item")
        if self.get_sell_navitem() is not None:
            errors.append("Expected navigation menu to have no 'Sell' navigation item")
        if self.get_hist_navitem() is not None:
            errors.append("Expected navigation menu to have no 'History' navigation item")
        assert not errors, "; ".join(errors)