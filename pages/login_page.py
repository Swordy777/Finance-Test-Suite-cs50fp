from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    """
    Log in Page POM.
    Contains methods for interacting with elements on the Log in page
    """

    def username_input(self):
        """Returns username input"""

        return self.retrieve_element_if_present(*LoginPageLocators.USERNAME_INPUT)


    def password_input(self):
        """Returns password input"""

        return self.retrieve_element_if_present(*LoginPageLocators.PASSWORD_INPUT)


    def login_button(self):
        """Returns log in button"""

        return self.retrieve_element_if_present(*LoginPageLocators.LOGIN_BUTTON)


    def log_in_with(self, username, password):
        """Fills username input and password input with given values and presses the log in button"""

        self.username_input().send_keys(username)
        self.password_input().send_keys(password)
        self.login_button().click()


    # Methods below aren't the best design, but we will leave it like this for now

    def more_un_inputs(self):
        """Returns a list of elements that could match the locator for username input"""

        return self.retrieve_multiple_elements_if_present(*LoginPageLocators.USERNAME_INPUT)
    
    def more_pw_inputs(self):
        """Returns a list of elements that could match the locator for password input"""

        return self.retrieve_multiple_elements_if_present(*LoginPageLocators.PASSWORD_INPUT)
    
    def more_login_buttons(self):
        """Returns a list of elements that could match the locator for buy button"""

        return self.retrieve_multiple_elements_if_present(*LoginPageLocators.LOGIN_BUTTON)