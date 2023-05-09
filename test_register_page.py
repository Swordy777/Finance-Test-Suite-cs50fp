import pytest
from random import random

from pages.register_page import RegisterPage
from pages.urls import URLS

SUCC_REG_MSG = "Registered!"
ERROR_MSG_NO_PASSWORD = "MISSING PASSWORD"
ERROR_MSG_WRONG_PASSWORD = "PASSWORDS DON'T MATCH"

class TestRegisterPageBasics():
    def test_has_username_field(self, browser):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        username_field = reg_page.get_username_field()
        assert username_field is not None, "Expected Username field to be present on registration page"

    def test_has_password_field(self, browser):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        password_field = reg_page.get_password_field()
        assert password_field is not None, "Expected Password field to be present on registration page"

    def test_has_confirmation_field(self, browser):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        confirm_field = reg_page.get_confirm_field()
        assert confirm_field is not None, "Expected Password Confirmation field to be present on registration page"


class TestRegistrationProcess():
    def test_successfull_registration(self, browser, user, database):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        reg_page.register_new_user(user['username'], user['password'])
        #adding new user to mock table
        reg_page.query(
            database, "insert into users (username, password) values (?, ?);", user['username'], user['password'])
        #checking if the new user was added to users table (this can be performed with real database)
        user_info = reg_page.query(
            database, "select * from users where username = ?", user['username'])
        assert user['username'] == user_info['username'], (
            "Couldn't find a new user in users table"
            )
        assert user_info['cash'] == reg_page.INITIAL_CASH, (
            f"Expected new user to have {reg_page.INITIAL_CASH} amount of cash, actual amount: {user_info['cash']}"
            )
        assert reg_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected successfully registered user to get redirected to default page, actual page: {reg_page.get_current_url()}"
            )
        reg_alert = reg_page.get_success_alert()
        assert reg_alert is not None, (
            f"Couldn't find registration alert on default page after successfull registration"
            )
        alert_text = reg_alert.text
        assert alert_text == SUCC_REG_MSG, (
            f"Expected successfully registered user to see 'Registered!' alert , actual text: {alert_text}"
            )
        
    @pytest.mark.parametrize("username, case", [("", "Empty username"), 
                                                (" ", "Whitespaces only username (one)"),
                                                ("              ", "Whitespaces only username (few)"),
                                                ("swordy", "Existing username"),])
    def test_incorrect_username_registration(self, browser, user, username, case):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        reg_page.register_new_user(username, user['password'])
        alert = reg_page.get_browser_alert()
        assert alert is not None, (
            f"Expected for a browser alert window to pop up in case if incorrect input: {case}"
            )
        assert alert.text == "Username is not available", (
            f"Expected for pop up alert to have text 'Username is not available', actual message: {alert.text}"
            )

    @pytest.mark.parametrize("password, case", [("", "Empty password"),
                                                pytest.param(" ", "White-space password (one)", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to consist of white spaces")),
                                                pytest.param("   ", "White-space password (few)", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to consist of white spaces")),
                                                pytest.param("1234567890", "Numbers only pasword", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to be numbers only")),
                                                pytest.param("abcdefgh", "Letters only pasword", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to be letters only")),
                                                pytest.param("!@#$%^&*()", "Special characters only pasword", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to be typographical only")),
                                                pytest.param("1qaz@wsx", "No uppercase letter pasword", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to not have uppercase letters")),
                                                pytest.param("1a!", "Less than 8 characters password", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to be less than 8 characters")),
                                                pytest.param("1qaz@ws", "7 characters password (border case)", 
                                                             marks=pytest.mark.xfail(
        reason="CS50 team's implementation allows for passwords to be less than 8 characters")),                                                       
                                                   ])
    def test_incorrect_password_registration(self, browser, database, user, password, case):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        reg_page.register_new_user(user['username'], password)
        error_image = reg_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: {case}"
            )
        error_text = reg_page.get_error_text(error_image)
        if case == "Empty password":
            assert error_text == ERROR_MSG_NO_PASSWORD, (
                f"Expected error image to have text {ERROR_MSG_NO_PASSWORD}, actual text: {error_text}"
                )
        else:
            assert error_text == ERROR_MSG_WRONG_PASSWORD, (
                f"Expected error image to have text {ERROR_MSG_WRONG_PASSWORD}, actual text: {error_text}"
                )

    @pytest.mark.parametrize("confirm, case", [("", "Empty confirm"),
                                               ("drow$$4P", "Valid confirm but mismatch with password")])
    def test_incorrect_confirm_registration(self, browser, database, user, confirm, case):
        reg_page = RegisterPage(browser, URLS.REGISTER_URL)
        reg_page.open()
        reg_page.register_new_user(user['username'], user['password'], confirm)
        error_image = reg_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image of funny cat in case if incorrect input: {case}"
            )
        error_text = reg_page.get_error_text(error_image)
        assert error_text == ERROR_MSG_WRONG_PASSWORD, (
                f"Expected error image to have text {ERROR_MSG_WRONG_PASSWORD}, actual text: {error_text}"
                )


