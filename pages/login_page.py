from .base_page import BasePage
from .locators import LoginPageLocators

class LoginPage(BasePage):
    def username_field(self):
        username_field = self.retrieve_element_if_present(*LoginPageLocators.USERNAME_FIELD)
        return username_field

    def password_field(self):
        password_field = self.retrieve_element_if_present(*LoginPageLocators.PASSWORD_FIELD)
        return password_field
    
    def login_button(self):
        login_button = self.retrieve_element_if_present(*LoginPageLocators.LOGIN_BUTTON)
        return login_button
    
    def log_in_with(self, username, password):
        self.username_field().send_keys(username)
        self.password_field().send_keys(password)
        self.login_button().click()