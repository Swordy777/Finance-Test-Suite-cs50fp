import pytest

from pages.login_page import LoginPage
from helpers import generate_tests_cls_parametrize, setup_page
from constants import LoginConstants as LC, URLS


class TestLoginPageBasics():
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def login_page(self, browser):
        return setup_page(LoginPage, browser, URLS.LOGIN_URL)


    def test_has_username_input(self, login_page):
        """Verify presence of username input"""

        assert login_page.username_input() is not None, (
            "Expected Log in page to have username input field"
            )
        

    def test_username_input_is_unique(self, login_page):
        """Verify that Username input is one of a kind"""

        more_els = login_page.more_un_inputs()
        assert login_page.is_unique(more_els), (
            f"Expected to find only one username input field on Log in page; found {len(more_els)}"
            )


    def test_username_input_default_value(self, login_page):
        """Verify username input's default value"""
        
        un_input_value = login_page.get_value(login_page.username_input())
        assert un_input_value == LC.EX_USERNAME_VALUE, (
            f"Expected username input field to be {'empty' if LC.EX_USERNAME_VALUE == '' else LC.EX_USERNAME_VALUE}, " \
                f"actual value: {un_input_value}"
                )
        

    def test_username_input_placeholder(self, login_page):
        """Verify username input's placeholder"""

        un_input_ph = login_page.get_placeholder(login_page.username_input())
        assert un_input_ph == LC.EX_USERNAME_PH, (
            f"Expected username input field placeholder text to be {LC.EX_USERNAME_PH}, actual value: {un_input_ph}"
            )


    def test_has_password_input(self, login_page):
        """Verify presence of password input"""

        assert login_page.password_input() is not None, (
            "Expected Log in page to have password input field"
            )
        

    def test_password_input_is_unique(self, login_page):
        """Verify that password input is one of a kind"""

        more_els = login_page.more_pw_inputs()
        assert login_page.is_unique(more_els), (
            f"Expected to find only one password input field on Log in page; found {len(more_els)}"
            )


    def test_password_input_default_value(self, login_page):
        """Verify password input's default value"""
        
        pw_input_value = login_page.get_value(login_page.password_input())
        assert pw_input_value == LC.EX_PASSWORD_VALUE, (
            f"Expected password input field to be empty, actual value: {pw_input_value}"
            )
        

    def test_password_input_placeholder(self, login_page):
        """Verify password input's placeholder"""

        pw_input_ph = login_page.get_placeholder(login_page.password_input())
        assert pw_input_ph == LC.EX_PASSWORD_PH, (
            f"Expected username input field placeholder text to be {LC.EX_PASSWORD_PH}, actual value: {pw_input_ph}"
            )


    def test_has_login_button(self, login_page):
        """Verify presence of log in button"""

        login_button = login_page.login_button()
        assert login_button is not None, (
            "Expected Log in page to have Log in button"
            )


    def test_login_button_is_unique(self, login_page):
        """Verify that Log in button is one of a kind"""

        more_els = login_page.more_login_buttons()
        assert login_page.is_unique(more_els), (
            f"Expected to find only one Log in button on Log in page; found {len(more_els)}"
            )


class TestSuccessfullLogin():
    """
    Test successfull log in scenario
    """

    @pytest.fixture(autouse=True, scope="class")
    def login_page(self, browser, new_user):
        return setup_page(LoginPage, browser, URLS.LOGIN_URL)


    @pytest.fixture(autouse=True, scope="class")
    def log_in_action(self, login_page, new_user):
        """
        Act fixture.
        Performs logging in steps with given username and password
        """
        
        login_page.log_in_with(new_user.username, new_user.password)


    def test_correct_redirection(self, login_page):
        """Verify correct redirection route after successfull log in attempt"""

        assert login_page.url_should_change_to(URLS.DEFAULT_URL), (
            "Expected for successfully logged in user to be redirected to default page"
            )
        

    def test_no_error_image(self, login_page):
        """Verify absense of error image"""

        assert login_page.get_error_image() is None, (
            f"Expected no error image to be displayed in case of successfull log in attempt"
            )


class InvalidLogin():
    """
    Test log in scenario with invalid login
    """

    @pytest.fixture(autouse=True, scope="class")
    def login_page(self, username, case, browser):
        return setup_page(LoginPage, browser, URLS.LOGIN_URL)

    
    @pytest.fixture(autouse=True, scope="class")
    def log_in_action(self, login_page, username, login_creds):
        login_page.log_in_with(username, login_creds.password)


    def test_no_redirection(self, login_page):
        """Verify user stays on the same page after unsuccesfull log in attempt"""

        assert login_page.get_current_url() == URLS.LOGIN_URL, (
            f"Expected for user with invalid credentials to stay on log in page; " \
                f"actual page: {login_page.get_current_url()}"
                )
        
    
    def test_error_image_appears(self, login_page, case):
        """Verify presence of error image"""

        error_image = login_page.get_error_image()
        assert error_image is not None, (
            f"Expected for app to display an error image with funny cat in case if invalid input: {case}"
            )
        

    def test_error_message(self, login_page, case):
        """Verify error message"""

        cases = {LC.INVALID_LOGIN_CASES[0][1]: LC.EMPTY_USERNAME_MSG,
                 "default": LC.INVALID_CREDS_MSG}
        ex_error = None
        error_text = login_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]
            
        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidLogin,
                                                   "username, case",
                                                   LC.INVALID_LOGIN_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidPassword():
    """
    Test log in scenario with invalid password
    """

    @pytest.fixture(autouse=True, scope="class")
    def login_page(self, password, case, browser):
        return setup_page(LoginPage, browser, URLS.LOGIN_URL)


    @pytest.fixture(autouse=True, scope="class")
    def login_action(self, login_page, password, login_creds):
        login_page.log_in_with(login_creds.username, password)


    def test_no_redirection(self, login_page):
        """Verify user stays on the same page after unsuccesfull log in attempt"""

        assert login_page.get_current_url() == URLS.LOGIN_URL, (
            f"Expected for user with invalid credentials to stay on log in page; " \
                f"actual page: {login_page.get_current_url()}"
                )


    def test_error_image_appears(self, login_page, case):
        """Verify presence of error image"""

        assert login_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat in case if invalid input: {case}"
            )
        

    def test_error_message(self, login_page, case):
        """Verify error message"""

        cases = {LC.INVALID_PASSWORD_CASES[0][1]: LC.EMPTY_PASS_MSG,
                 "default": LC.INVALID_CREDS_MSG}
        ex_error = None
        error_text = login_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]
            
        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )
            

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidPassword,
                                                   "password, case",
                                                   LC.INVALID_PASSWORD_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]