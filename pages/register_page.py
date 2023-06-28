from .base_page import BasePage
from .locators import RegisterPageLocators


class RegisterPage(BasePage):
    """
    Register Page POM.
    Contains methods for interacting with elements on the Register page
    """

    def username_input(self):
        """Returns username input"""

        return self.retrieve_element_if_present(*RegisterPageLocators.USERNAME_INPUT)


    def password_input(self):
        """Returns password input"""

        return self.retrieve_element_if_present(*RegisterPageLocators.PASSWORD_INPUT)


    def confirm_input(self):
        """Returns password confirmation input"""

        return self.retrieve_element_if_present(*RegisterPageLocators.CONFIRM_INPUT)
    
    def register_button(self):
        """Returns register button"""

        return self.retrieve_element_if_present(*RegisterPageLocators.REGISTER_BUTTON)


    def register_new_user(self, username, password, confirm="not specified"):
        """
        Fills username, password and confirm inputs with given values and presses the register button
        If confirm value is not given, it copies the password value
        """
        
        if confirm == "not specified":
            confirm = password
        self.username_input().send_keys(username)
        self.password_input().send_keys(password)
        self.confirm_input().send_keys(confirm)
        self.register_button().click()


    # Methods below aren't the best design, but we will leave it like this for now

    def more_un_inputs(self):
        """Returns a list of elements that could match the locator for username input"""

        return self.retrieve_multiple_elements_if_present(*RegisterPageLocators.USERNAME_INPUT)


    def more_pw_inputs(self):
        """Returns a list of elements that could match the locator for password input"""
        
        return self.retrieve_multiple_elements_if_present(*RegisterPageLocators.PASSWORD_INPUT)


    def more_conf_inputs(self):
        """Returns a list of elements that could match the locator for password confirmation input"""

        return self.retrieve_multiple_elements_if_present(*RegisterPageLocators.CONFIRM_INPUT)


    def more_reg_buttons(self):
        """Returns a list of elements that could match the locator for register button"""
        
        return self.retrieve_multiple_elements_if_present(*RegisterPageLocators.REGISTER_BUTTON)


