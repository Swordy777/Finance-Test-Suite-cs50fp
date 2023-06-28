from selenium.webdriver.common.by import By


class BasePageLocators():
    """Locators for elements that are common across all pages."""
    
    DEFAULT_LINK = (By.CSS_SELECTOR, "a[href='/']")
    CS50_LOGO_PART = (By.CSS_SELECTOR, ".navbar-brand span")
    QUOTE_LINK = (By.CSS_SELECTOR, "[id='navbar'] a[href='/quote']")
    BUY_LINK = (By.CSS_SELECTOR, "[id='navbar'] a[href='/buy']")
    SELL_LINK = (By.CSS_SELECTOR, "[id='navbar'] a[href='/sell']")
    HISTORY_LINK = (By.CSS_SELECTOR, "[id='navbar'] a[href='/history']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/register']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "[id='navbar'] a[href='/logout']")
    ERROR_IMAGE = (By.TAG_NAME,"img")
    ALERT_MESSAGE = (By.CSS_SELECTOR, ".alert")
    

class LoginPageLocators():
    """Locators for Log in page elements"""

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Log In']")


class RegisterPageLocators():
    """Locators for Register page elements"""

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_INPUT = (By.NAME, "confirmation")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Register']")


class DefaultPageLocators():
    """Locators for Default page elements"""

    SHARES_TABLE = (By.TAG_NAME,"table")
    SHARES_TABLE_HEADERS = (By.CSS_SELECTOR, "table th")
    SHARES_TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    SHARES_TABLE_ROW_CELLS = (By.CSS_SELECTOR, "tbody tr td")
    CASH_ELEMENT = (By.CSS_SELECTOR,"tfoot tr:nth-child(1) td:nth-child(2)")
    TOTAL_ELEMENT = (By.CSS_SELECTOR,"tfoot tr:nth-child(2) td:nth-child(2)")


class QuotePageLocators():
    """Locators for Quote page elements"""

    SHARE_SYMBOL_INPUT = (By.NAME, "symbol")
    QUOTE_BUTTON = (By.XPATH, "//button[text()='Quote']")
    SHARE_QUOTE_RESULT = (By.CSS_SELECTOR, "main p")


class BuyPageLocators():
    """Locators for Buy page elements"""

    SHARES_SYMBOL_INPUT = (By.NAME, "symbol")
    SHARES_AMOUNT_INPUT = (By.NAME, "shares")
    BUY_BUTTON = (By.XPATH, "//button[text()='Buy']")


class SellPageLocators():
    """Locators for Sell page elements"""

    SHARES_LIST = (By.CSS_SELECTOR, "select[name='symbol']")
    SHARES_LIST_DEFAULT_OPTION = (By.CSS_SELECTOR, "select[name='symbol'] option:first-child")
    SHARE_AMOUNT_INPUT = (By.NAME, "shares")
    SELL_BUTTON = (By.XPATH, "//button[text()='Sell']")


class HistoryPageLocators():
    """Locators for History page elements"""

    HISTORY_TABLE = (By.TAG_NAME,"table")
    HISTORY_TABLE_HEADERS = (By.CSS_SELECTOR, "table th")
    HISTORY_TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    HISTORY_TABLE_ROW_CELLS = (By.CSS_SELECTOR, "tbody tr td")