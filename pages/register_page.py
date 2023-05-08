from .base_page import BasePage
from .locators import RegisterPageLocators
from .locators import BasePageLocators

class RegisterPage(BasePage):
    def get_username_field(self):
        username_field = self.retrieve_element_if_present(*RegisterPageLocators.USERNAME_FIELD)
        return username_field
    
    def get_password_field(self):
        password_field = self.retrieve_element_if_present(*RegisterPageLocators.PASSWORD_FIELD)
        return password_field
    
    def get_confirm_field(self):
        confirm_field = self.retrieve_element_if_present(*RegisterPageLocators.CONFIRM_FIELD)
        return confirm_field
    
    def get_register_button(self):
        register_button = self.retrieve_element_if_present(*RegisterPageLocators.REGISTER_BUTTON)
        return register_button
    
    def register_new_user(self, username, password, confirm="not specified"):
        if confirm == "not specified":
            confirm = password
        self.get_username_field().send_keys(username)
        self.get_password_field().send_keys(password)
        self.get_confirm_field().send_keys(confirm)
        self.get_register_button().click()


