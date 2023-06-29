import pytest

from pages.register_page import RegisterPage
from pages.urls import URLS
from helpers import generate_tests_cls_parametrize, setup_page
from constants import SharedConstants as ShC, DatabaseConstants as DBC, RegisterConstants as RC





class TestRegisterPageBasics():
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def reg_page(self, browser):
        yield setup_page(RegisterPage, browser, URLS.REGISTER_URL)


    def test_has_username_input(self, reg_page):
        """Verify presence of username input"""

        assert reg_page.username_input() is not None, (
            "Expected Username input field to be present on Register page"
            )
        

    def test_username_input_is_unique(self, reg_page):
        """Verify that Username input is one of a kind"""

        more_els = reg_page.more_un_inputs()
        assert reg_page.is_unique(more_els), (
            f"Expected to find only one username input field on Register page; found {len(more_els)}"
            )


    def test_username_input_default_value(self, reg_page):
        """Verify username input's default value"""
        
        un_input_value = reg_page.get_value(reg_page.username_input())
        assert un_input_value == RC.EX_USERNAME_VALUE, (
            f"Expected username input field to be empty, actual value: {un_input_value}"
            )
        

    def test_username_input_placeholder(self, reg_page):
        """Verify username input's placeholder"""

        un_input_ph = reg_page.get_placeholder(reg_page.username_input())
        assert un_input_ph == RC.EX_REG_UN_PH, (
            f"Expected username input field placeholder text to be {RC.EX_REG_UN_PH}, actual value: {un_input_ph}"
            )
        

    def test_has_password_input(self, reg_page):
        """Verify presence of password input"""

        assert reg_page.password_input() is not None, (
            "Expected password input field to be present on Register page"
            )
        

    def test_password_input_is_unique(self, reg_page):
        """Verify that password input is one of a kind"""

        more_els = reg_page.more_pw_inputs()
        assert reg_page.is_unique(more_els), (
            f"Expected to find only one password input field on Register page; found {len(more_els)}"
            )


    def test_password_input_default_value(self, reg_page):
        """Verify password input's default value"""

        pw_input_value = reg_page.get_value(reg_page.password_input())
        assert pw_input_value == RC.EX_PASSWORD_VALUE, (
            f"Expected password input field to be {'empty' if RC.EX_PASSWORD_VALUE == '' else RC.EX_PASSWORD_VALUE}, " \
                f"actual value: {pw_input_value}"
                )
        

    def test_password_input_placeholder(self, reg_page):
        """Verify password input's placeholder"""

        pw_input_ph = reg_page.get_placeholder(reg_page.password_input())
        assert pw_input_ph == RC.EX_REG_PW_PH, (
            f"Expected password input field placeholder text to be {RC.EX_REG_PW_PH}, actual value: {pw_input_ph}"
            )
        
        
    def test_has_confirmation_input(self, reg_page):
        """Verify presence of confirm input"""

        assert reg_page.confirm_input() is not None, (
            "Expected password confirmation input field to be present on registration page"
            )
        

    def test_confirm_input_is_unique(self, reg_page):
        """Verify that confirm input is one of a kind"""

        more_els = reg_page.more_conf_inputs()
        assert reg_page.is_unique(more_els), (
            f"Expected to find only one password confirmation input field on Register page; found {len(more_els)}"
            )
        

    def test_confirm_input_default_value(self, reg_page):
        """Verify confirm input's default value"""

        conf_input_value = reg_page.get_value(reg_page.confirm_input())
        assert conf_input_value == RC.EX_CONF_VALUE, (
            f"Expected password confirmation input field to be empty, actual value: {conf_input_value}"
            )
        

    def test_confirm_input_placeholder(self, reg_page):
        """Verify confirm input's placeholder"""

        conf_input_ph = reg_page.get_placeholder(reg_page.confirm_input())
        assert conf_input_ph == RC.EX_REG_CONF_PH, (
            f"Expected password confirmation  input field placeholder text to be {RC.EX_REG_CONF_PH}, " \
                f"actual value: {conf_input_ph}"
                )
        

    def test_has_register_button(self, reg_page):
        """Verify presence of Register button"""

        register_button = reg_page.register_button()
        assert register_button is not None, (
            "Expected Register page to have register button"
            )


    def test_register_button_is_unique(self, reg_page):
        """Verify that Register button is one of a kind"""

        more_els = reg_page.more_reg_buttons()
        assert reg_page.is_unique(more_els), (
            f"Expected to find only one Register button on Register page; found {len(more_els)}"
            )
        

class TestSuccesfullRegistration():
    """
    Test successfull registration scenario
    """

    @pytest.fixture(autouse=True, scope="class")
    def reg_page(self, browser):
        yield setup_page(RegisterPage, browser, URLS.REGISTER_URL)


    @pytest.fixture(autouse=True, scope="class")
    def registration(self, reg_page, login_creds, database):
        """
        Act fixture.
        Performs registration steps with given username and password
        """

        reg_page.register_new_user(login_creds.username, login_creds.password)

        # Add new user to mock db
        database.mock_db_add_new_user(login_creds.username, login_creds.password)

        yield database.user_data(login_creds.username)

        # Delete new user data from database
        database.mock_db_delete_tran_data(login_creds.username)
        database.mock_db_delete_user_data(login_creds.username)


    def test_correct_redirection(self, reg_page):
        """Verify correct redirection route after successfull registration attempt"""
        
        assert reg_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected successfully registered user to get redirected to Default page, " \
                f"actual page: {reg_page.get_current_url()}"
                )
        

    def test_has_success_alert(self, reg_page):
        """Verify presence of success alert"""
        
        assert reg_page.get_flash() is not None, (
            f"Couldn't find registration alert on default page after successfull registration"
            )
        

    def test_alert_message(self, reg_page):
        """Verify alert message"""

        alert_text = reg_page.get_flash().text
        assert alert_text == RC.SUCC_REG_MSG, (
            f"Expected successfully registered user to see {RC.SUCC_REG_MSG} alert , actual text: {alert_text}"
            )


    def test_db_new_user_data(self, login_creds, registration):
        """Verify that new user data was added to database"""

        assert registration[DBC.USERNAME] == login_creds.username, (
            "Couldn't find a new user row in database"
            )
        

    def test_db_new_user_cash_value(self, registration):
        """Verify new user cash default value"""

        assert registration[DBC.CASH] == ShC.INITIAL_CASH, (
            f"Expected new user to have {ShC.INITIAL_CASH} amount of cash, actual amount: {registration[DBC.CASH]}"
            )
        
        
    def test_db_no_tran_history(self, login_creds, database):
        """Verify tran history is empty for newly registered user"""
        
        tran_history = database.transactions(login_creds.username)
        assert tran_history is None, (
            "Expected new user's transaction history to be empty"
            )
        

class InvalidUsernameRegistration():
    """
    Test registration process with invalid username values
    """

    @pytest.fixture(autouse=True, scope="class")
    def reg_page(self, browser, username, case):
        yield setup_page(RegisterPage, browser, URLS.REGISTER_URL)


    @pytest.fixture(autouse=True, scope="class")
    def registration(self, reg_page, login_creds, username, case, database):
        """
        Act fixture.
        Performs registration steps with given username and password
        """

        if case == RC.INVALID_USERNAME_CASES[3][1]:
            for i in range(2):
                reg_page.open()
                reg_page.register_new_user(login_creds.username, login_creds.password)
                if i == 0: 
                    reg_page.url_should_change_to(URLS.DEFAULT_URL)
        else:
            reg_page.register_new_user(username, login_creds.password)
        yield database.user_data(login_creds.username)


    def test_has_browser_alert(self, reg_page, case):
        """Verify presence of browser's built-in pop up dialogue box"""
        
        assert reg_page.get_browser_alert() is not None, (
            f"Expected for a browser alert window to pop up in case if invalid input: {case}"
            )
        

    def test_browser_alert_text(self, reg_page):
        """Verify pop up's message"""

        alert_text = reg_page.get_browser_alert().text
        assert alert_text == RC.ERROR_MSG_NA_UN, (
            f"Expected for pop up alert to have text {RC.ERROR_MSG_NA_UN}, actual message: {alert_text}"
            )
        

    def test_db_no_new_user(self, registration):
        """Verify that no new user was added to database"""

        assert registration is None, (
            "Expected no new users to be added to database"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidUsernameRegistration,
                                                   "username, case",
                                                   RC.INVALID_USERNAME_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


"""
I wasn't able to find a way to implement xfail marks through @pytest.param() for class generator helper function.
This is why invalid password registration tests are not using 'one test - one assert' concept.
I decided to leave them as is for now.
"""

@pytest.mark.parametrize("password, case", 
                         RC.INVALID_PASSWORD_CASES)
def test_invalid_password_registration(browser, database, login_creds, password, case):
    """
    Test registration process with invalid password values
    """

    reg_page = setup_page(RegisterPage, browser, URLS.REGISTER_URL)
    reg_page.register_new_user(login_creds.username, password)
    assert reg_page.get_error_image() is not None, (
        f"Expected for app to display an error image with funny cat in case if invalid input: {case}"
        )
    
    cases = {RC.INVALID_PASSWORD_CASES[0][1]: RC.ERROR_MSG_NO_PASSWORD,
             "default": RC.ERROR_MSG_WRONG_PASSWORD}
    ex_error = None
    error_text = reg_page.get_error_image_text()
    if case in cases:
        ex_error = cases[case]
    else:
        ex_error = cases["default"]
        
    assert error_text == ex_error, (
        f"Expected error image to have text {ex_error}, actual text: {error_text}"
        )
        
    assert database.user_data(login_creds.username) is None, (
        "Expected no new users to be added to database"
        )


class InvalidConfirmRegistration():
    """
    Test registration process with invalid confirm values
    """

    @pytest.fixture(autouse=True, scope="class")
    def reg_page(self, browser, confirm, case):
        yield setup_page(RegisterPage, browser, URLS.REGISTER_URL)


    @pytest.fixture(autouse=True, scope="class")
    def registration(self, reg_page, login_creds, confirm, database):
        """
        Act fixture.
        Performs registration steps with given username, password and confirm
        """

        reg_page.register_new_user(login_creds.username, login_creds.password, confirm)
        yield database.user_data(login_creds.username)


    def test_error_image_appears(self, reg_page, case):
        """Verify presence of error image"""

        assert reg_page.get_error_image() is not None, (
            f"Expected for app to display an error image of funny cat in case if invalid input: {case}"
            )
        
        
    def test_error_message(self, reg_page):
        """Verify error message"""
        
        error_text = reg_page.get_error_image_text()
        assert error_text == RC.ERROR_MSG_WRONG_PASSWORD, (
                f"Expected error image to have text {RC.ERROR_MSG_WRONG_PASSWORD}, actual text: {error_text}"
                )
        

    def test_db_no_new_user(self, registration):
        """Verify that no new user was added to database"""

        assert registration is None, (
            "Expected no new users to be added to database"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidConfirmRegistration,
                                                   "confirm, case", 
                                                   RC.INVALID_CONFIRM_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]