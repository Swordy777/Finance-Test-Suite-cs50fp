import pytest

from pages.base_page import BasePage
from pages.urls import URLS

AUTHED_PAGES = [(URLS.DEFAULT_URL, "C$50 Finance: Portfolio"),
             (URLS.QUOTE_URL, "C$50 Finance: Quote"),
             (URLS.BUY_URL, "C$50 Finance: Buy"),
             (URLS.SELL_URL, "C$50 Finance: Sell"),
             (URLS.HISTORY_URL, "C$50 Finance: History"),]

UNAUTHED_PAGES = [(URLS.LOGIN_URL, "C$50 Finance: Log In"),
                  (URLS.REGISTER_URL, "C$50 Finance: Register"),]

@pytest.mark.usefixtures("login")
@pytest.mark.parametrize("page_url, ex_page_name", AUTHED_PAGES)
class TestCommonPageStructureAuthed():
    def test_page_title_is_correct(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page_title = page.get_page_title()
        assert page_title == ex_page_name, (
            f"Expected page title to be {ex_page_name}, actual title: {page_title}")
        
    def test_has_link_to_the_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_have_default_link()

    def test_cs50logo_is_visible(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_have_cs50_logo()

    def test_nav_items_are_present(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_have_nav_items()

    def test_no_register_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        register_menu_item = page.get_register_link()
        assert register_menu_item is None, "Expected no 'Register' navigation item to exist for logged in user"

    def test_no_login_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        login_menu_item = page.get_login_link()
        assert login_menu_item is None, "Expected no 'Log in' navigation item to exist for logged in user"

    def test_has_logout_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        logout_menu_item = page.get_logout_link()
        assert logout_menu_item is not None, "Expected for logged in user to have 'Log out' navigation item"

@pytest.mark.parametrize("page_url, ex_page_name", UNAUTHED_PAGES)
class TestCommonPageStructureUnauthed():
    def test_register_page_title_is_correct(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page_title = page.get_page_title()
        assert page_title == ex_page_name, (
            f"Expected page title to be {ex_page_name}, actual title: {page_title}")
        
    def test_has_link_to_the_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_have_default_link()

    def test_cs50logo_is_visible(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_have_cs50_logo()

    def test_has_no_nav_items(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.should_not_have_nav_items()

    def test_no_register_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        register_menu_item = page.get_register_link()
        assert register_menu_item is not None, "Expected 'Register' navigation item to be present on register page"

    def test_has_login_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        login_menu_item = page.get_login_link()
        assert login_menu_item is not None, "Expected 'Log in' navigation item to be present on register page"

    def test_has_no_logout_menu_item(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        logout_menu_item = page.get_logout_link()
        assert logout_menu_item is None, "Expected navigation menu to not have 'Log out' navigation item"

@pytest.mark.usefixtures("login")
@pytest.mark.parametrize("page_url, ex_page_name", AUTHED_PAGES)
class TestCommonNavigation():
    def test_go_to_quote_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.get_quote_navitem().click()
        assert page.url_should_change_to(URLS.QUOTE_URL), (
                f"Expected to be able to navigate to Quote page; actual page: {page.get_current_url()}")

    def test_go_to_buy_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.get_buy_navitem().click()
        assert page.url_should_change_to(URLS.BUY_URL), (
                f"Expected to be able to navigate to Buy page; actual page: {page.get_current_url()}")

    def test_go_to_sell_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.get_sell_navitem().click()
        assert page.url_should_change_to(URLS.SELL_URL), (
                f"Expected to be able to navigate to Sell page; actual page: {page.get_current_url()}")

    def test_go_to_history_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.get_hist_navitem().click()
        assert page.url_should_change_to(URLS.HISTORY_URL), (
                f"Expected to be able to navigate to History page; actual page: {page.get_current_url()}")

    @pytest.mark.xfail(reason="CS50 team's implementation doesn't forbid logged in user from going to log in page")    
    def test_go_to_login_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.go_to_other_page(URLS.LOGIN_URL)
        assert page.url_should_change_to(URLS.DEFAULT_URL), (
                f"Expected to be redirected to default page bc already logged in; actual page: {page.get_current_url()}")
    
    @pytest.mark.xfail(reason="CS50 team's implementation doesn't forbid logged in user from going to register page")  
    def test_go_to_register_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.go_to_other_page(URLS.REGISTER_URL)
        assert page.url_should_change_to(URLS.DEFAULT_URL), (
                f"Expected to be redirected to default page bc already logged in; actual page: {page.get_current_url()}")
        
    def test_go_to_logout_page(self, browser, page_url, ex_page_name):
        page = BasePage(browser, page_url)
        page.open()
        page.get_logout_link().click()
        assert page.url_should_change_to(URLS.LOGIN_URL), (
                f"Expected to be redirected to login page after logging out; actual page: {page.get_current_url()}")