import pytest

from pages.login_page import LoginPage
from pages.urls import URLS

EMPTY_USERNAME_MSG = "MUST PROVIDE USERNAME"
EMPTY_PASS_MSG = "MUST PROVIDE PASSWORD"
INCORRECT_CREDS_MSG = "INVALID USERNAME AND/OR PASSWORD"

class TestLoginPageBasics():
    def test_has_username_field(self, browser):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        username_field = login_page.username_field()
        assert username_field is not None, "Expected Log in page to have username field"
    
    def test_has_password_field(self, browser):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        password_field = login_page.password_field()
        assert password_field is not None, "Expected Log in page to have password field"
    
    def test_has_login_button(self, browser):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        login_button = login_page.login_button()
        assert login_button is not None, "Expected Log in page to have login button"


class TestLoginProcess():
    def test_successfull_login(self, browser, new_user):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        login_page.log_in_with(new_user['username'], new_user['password'])
        assert login_page.url_should_change_to(URLS.DEFAULT_URL), (
            "Expected for successfully logged in user to be redirected to default page")

    @pytest.mark.parametrize("username, case", [("", "Empty username"),
                                                ("non-existent-username", "Non-existent username")])
    def test_incorrect_login(self, browser, user, username, case):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        login_page.log_in_with(username, user['password'])
        error_image = login_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: {case}"
            )
        error_text = login_page.get_error_text(error_image)
        if case == "Empty username":
            assert error_text == EMPTY_USERNAME_MSG, (
                f"Expected error image to have text {EMPTY_USERNAME_MSG}, actual text: {error_text}"
                )
        elif case == "Non-existent username":
            assert error_text == INCORRECT_CREDS_MSG, (
                f"Expected error image to have text {INCORRECT_CREDS_MSG}, actual text: {error_text}"
                )

    @pytest.mark.parametrize("password, case", [("", "Empty password"),
                                                ("non-existent-password", "Non-existent password")])
    def test_incorrect_password(self, browser, new_user, password, case):
        login_page = LoginPage(browser, URLS.LOGIN_URL)
        login_page.open()
        login_page.log_in_with(new_user['username'], password)
        error_image = login_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: {case}"
            )
        error_text = login_page.get_error_text(error_image)
        if case == "Empty password":
            assert error_text == EMPTY_PASS_MSG, (
                f"Expected error image to have text {EMPTY_PASS_MSG}, actual text: {error_text}"
                )
        elif case == "Non-existent password":
            assert error_text == INCORRECT_CREDS_MSG, (
                f"Expected error image to have text {INCORRECT_CREDS_MSG}, actual text: {error_text}"
                )
            