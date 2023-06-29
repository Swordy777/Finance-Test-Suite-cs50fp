import pytest

from pages.urls import URLS
from pages.common_page import CommonPage
from pages.login_page import LoginPage

from helpers import setup_page
from constants import CommonConstants as CC


@pytest.mark.parametrize("page_url, ex_page_name", 
                         CC.AUTHED_PAGES, 
                         scope="class")
class TestCommonPageStructureAuthed():
    """
    Verify pages having common elements for logged in users
    """

    @pytest.fixture(autouse=True, scope="class")
    def page(self, browser, new_user, page_url, ex_page_name):
        yield setup_page(CommonPage, browser, page_url)


    def test_page_title_is_correct(self, page, ex_page_name):
        """Verify page title"""

        page_title = page.get_page_title()
        assert page_title == ex_page_name, (
            f"Expected page title to be {ex_page_name}, actual title: {page_title}"
            )
        

    def test_has_link_to_default_page(self, page):
        """Verify presence of link to the Default page"""

        assert page.get_default_link() is not None, (
            "Couldn't find the link to the default page (the clickable CS50 logo)"
            )


    def test_cs50logo_is_visible(self, page):
        """Verify page logo"""

        assert page.get_cs50_logo() == CC.CS50_LOGO, (
            f"Page Logo in the navigation bar (sum of spans inside the default page link) doesnt spell {CC.CS50_LOGO}"
            )
    

    def test_no_register_menu_item(self, page):
        """Verify absence of register link/button for logged in users"""

        assert page.get_register_link() is None, (
            "Expected no 'Register' navigation item to exist for logged in user"
            )


    def test_no_login_menu_item(self, page):
        """Verify absence of log in link/button for logged in users"""

        assert page.get_login_link() is None, (
            "Expected no 'Log in' navigation item to exist for logged in user"
            )


    def test_has_logout_menu_item(self, page):
        """Verify presence of of log out link/button for logged in users"""

        assert page.get_logout_link() is not None, (
            "Expected for logged in user to have 'Log out' navigation item"
            )


    def test_nav_items_are_present(self, page):
        """
        Outdated test; asserts are inside the POM method. 
        Verify presence of certain navigation buttons/links
        """

        page.should_have_nav_items()


@pytest.mark.parametrize("page_url, ex_page_name", 
                         CC.UNAUTHED_PAGES,
                         scope="class")
class TestCommonPageStructureUnauthed():
    """
    Test pages having common elements for unauthenticated users
    """

    @pytest.fixture(autouse=True, scope="class")
    def page(self, browser, page_url, ex_page_name):
        yield setup_page(CommonPage, browser, page_url)


    def test_register_page_title_is_correct(self, page, ex_page_name):
        """Verify page title"""

        page_title = page.get_page_title()
        assert page_title == ex_page_name, (
            f"Expected page title to be {ex_page_name}, actual title: {page_title}"
            )
        

    def test_has_link_to_default_page(self, page):
        """Verify presence of link to the Default page"""

        assert page.get_default_link() is not None, (
            "Couldn't find the link to the default page (the clickable CS50 logo)"
            )


    def test_cs50logo_is_visible(self, page):
        """Verify page logo"""

        assert page.get_cs50_logo() == CC.CS50_LOGO, (
            f"Page Logo in the navigation bar (sum of spans inside the default page link) doesnt spell {CC.CS50_LOGO}"
            )


    def test_has_register_menu_item(self, page):
        """Verify presence of register link/button for unauthed users"""

        assert page.get_register_link() is not None, (
            "Expected 'Register' navigation item to be present on register page"
            )


    def test_has_login_menu_item(self, page):
        """Verify presence of log in link/button for unauthed users"""

        assert page.get_login_link() is not None, (
            "Expected 'Log in' navigation item to be present on register page"
            )


    def test_no_logout_menu_item(self, page):
        """Verify absence of of log out link/button for unauthed in users"""

        assert page.get_logout_link() is None, (
            "Expected navigation menu to have no 'Log out' navigation item"
            )
        

    def test_no_nav_items(self, page):
        """
        Outdated test; asserts are inside the POM method. 
        Verify absence of certain navigation buttons/links
        """

        page.should_not_have_nav_items()


@pytest.mark.parametrize("page_url, ex_page_name", 
                         CC.AUTHED_PAGES)
class TestCommonNavigationAuthed():
    """
    Test available navigation routes for logged in users
    """

    @pytest.fixture(autouse=True, scope="function")
    def page(self, browser, new_user, page_url, ex_page_name):
        yield setup_page(CommonPage, browser, page_url)


    def test_go_to_quote_page(self, page):
        """Verify Quote nav item routing"""

        page.get_quote_navitem().click()
        assert page.url_should_change_to(URLS.QUOTE_URL), (
                f"Expected to be able to navigate to Quote page; actual page: {page.get_current_url()}"
                )
        
        
    def test_go_to_buy_page(self, page):
        """Verify Buy nav item routing"""

        page.get_buy_navitem().click()
        assert page.url_should_change_to(URLS.BUY_URL), (
                f"Expected to be able to navigate to Buy page; actual page: {page.get_current_url()}"
                )


    def test_go_to_sell_page(self, page):
        """Verify Sell nav item routing"""

        page.get_sell_navitem().click()
        assert page.url_should_change_to(URLS.SELL_URL), (
                f"Expected to be able to navigate to Sell page; actual page: {page.get_current_url()}"
                )


    def test_go_to_history_page(self, page):
        """Verify History nav item routing"""

        page.get_hist_navitem().click()
        assert page.url_should_change_to(URLS.HISTORY_URL), (
                f"Expected to be able to navigate to History page; actual page: {page.get_current_url()}"
                )


@pytest.mark.parametrize("page_url, ex_page_name", 
                         CC.AUTHED_PAGES)
class TestSessionEnders():
    """
    Test app behaviour with session-ending routes
    """

    @pytest.fixture(autouse=True, scope="function")
    def page(self, browser, new_user, page_url, ex_page_name):
        yield setup_page(CommonPage, browser, page_url)
        # session ends after going to login/register page or after logging out; adding steps to re-log in:
        lp = LoginPage(browser, URLS.LOGIN_URL)
        lp.open()
        lp.log_in_with(new_user.username, new_user.password)


    @pytest.mark.xfail(reason="CS50 team's implementation doesn't forbid logged in user from going to log in page")    
    def test_go_to_login_page(self, page):
        """Verify app behaviour after force redirect to Log in page """

        page.go_to_other_page(URLS.LOGIN_URL)
        assert page.url_should_change_to(URLS.DEFAULT_URL), (
                f"Expected to be redirected to default page because already logged in; actual page: {page.get_current_url()}"
                )


    @pytest.mark.xfail(reason="CS50 team's implementation doesn't forbid logged in user from going to register page")  
    def test_go_to_register_page(self, page):
        """Verify app behaviour after force redirect to Register page"""

        page.go_to_other_page(URLS.REGISTER_URL)
        assert page.url_should_change_to(URLS.DEFAULT_URL), (
                f"Expected to be redirected to default page because already logged in; actual page: {page.get_current_url()}"
                )


    def test_go_to_logout_page(self, page):
        """Verify Log out nav item routing"""

        page.get_logout_link().click()
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be redirected to log in page after logging out; actual page: {page.get_current_url()}"
                )
        

@pytest.mark.parametrize("page_url, ex_page_name", 
                         CC.UNAUTHED_PAGES,
                         scope="class")
class TestCommonNavigationUnauthed():
    """
    Test available navigation routes for unauthed users
    """

    @pytest.fixture(autouse=True, scope="class")
    def page(self, browser, page_url, ex_page_name):
        yield setup_page(CommonPage, browser, page_url)


    def test_go_to_quote_page(self, page):
        """Verify Quote nav item routing"""

        page.go_to_other_page(URLS.QUOTE_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be forced to go to Log in page if unauthed; actual page: {page.get_current_url()}"
                )
        

    def test_go_to_buy_page(self, page):
        """Verify Buy nav item routing"""

        page.go_to_other_page(URLS.BUY_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be forced to go to Log in page if unauthed; actual page: {page.get_current_url()}"
                )
        

    def test_go_to_sell_page(self, page):
        """Verify Sell nav item routing"""

        page.go_to_other_page(URLS.SELL_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be forced to go to Log in page if unauthed; actual page: {page.get_current_url()}"
                )


    def test_go_to_history_page(self, page):
        """Verify History nav item routing"""

        page.go_to_other_page(URLS.HISTORY_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be forced to go to Log in page if unauthed; actual page: {page.get_current_url()}"
                )
   

    def test_go_to_login_page(self, page):
        """Verify app behaviour after force redirect to Log in page"""

        page.go_to_other_page(URLS.LOGIN_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to stay on Log in page if unauthed; actual page: {page.get_current_url()}"
                )
    

    def test_go_to_register_page(self, page):
        """Verify app behaviour after force redirect to Register page"""

        page.go_to_other_page(URLS.REGISTER_URL)
        assert page.url_should_change_to(URLS.REGISTER_URL), (
                f"Expected to stay on Register page if unauthed; actual page: {page.get_current_url()}"
                )
        

    def test_go_to_logout_page(self, page):
        """Verify app behaviour after force redirect to Log out page"""
        
        page.go_to_other_page(URLS.LOGOUT_URL)
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be forced to go to Log in page if unauthed; actual page: {page.get_current_url()}"
                )
