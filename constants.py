import pytest
import time
from random import random, uniform, randint, choice

from pages.urls import URLS

class SharedConstants():
    """Constants which are shared among multiple test modules"""

    # Small list of possible valid stock symbols
    TEST_SYMBOLS = ["AAPL", "MSFT", "NFLX", "MCD"]

    # Initial cash value for newly registered user
    INITIAL_CASH = 10000.00

    # Mock value for a stock price
    MOCK_PRICE = 777.77


    # Test values for cases of invalid symbol input
    # Some tests reference specific list elements,
    # so it is important to add new cases to THE END OF THE LIST 
    INVALID_SYMBOL_CASES = [("", "Empty stock symbol"),
                            (" ", "White-space stock symbol (one)"),
                            ("   ", "White-space stock symbol (few)"),
                            (randint(1, 999), "Digits only stock symbol"),
                            (0, "Zero stock symbol"),
                            (round(random()*10 + 0.1, 1), "Floating point number stock symbol"),
                            (str(round(random()*10 + 0.1, 1)).replace(".",","), "Floating point number (comma) stock symbol"),
                            (time.strftime("%d.%m.%Y", time.localtime()), "Date stock symbol"),
                            ("NULL", "NULL stock symbol"),
                            ("$@%?", "Special characters only stock symbol"),
                            ("zyzx", "Non-existent stock symbol (only letters)"),
                            ("$A23", "Non-existent stock symbol (combination)"),
                            ("тест", "Other alphabets stock symbol #1"),
                            ("片仮名", "Other alphabets stock symbol #2"),
                            ("😍😍😍", "Emoji stock symbol")]

    # Test values for cases of invalid amount input (typable)
    # Some tests reference specific list elements,
    # so it is important to add new cases to THE END OF THE LIST 
    UNTYPABLE_AMOUNT_CASES = [("", "Empty stock amount"),
                              (" ", "White-space stock amount (one)"),
                              ("   ", "White-space stock amount (few)"),
                              ("two", "Letters in amount"),
                              ("$@%", "Special characters amount"),
                              ("пять", "Other alphabets amount #1"),
                              ("片仮名", "Other alphabets amount #2"),
                              ("💵💵💵", "Emoji stock amount"),
                              (",", "Comma")]

    # Test values for cases of invalid amount input (untypable)
    # Some tests reference specific list elements,
    # so it is important to add new cases to THE END OF THE LIST 
    TYPABLE_AMOUNT_CASES = [(0, "Zero amount"),
                            (randint(-10000, -1), "Negative amount"),
                            (round(int(random()*10) + uniform(0.1, 0.9), 1), "Float amount (period)"),
                            (randint(1000, 10000), "Buying more than affordable"),
                            (round((random()*10), 0), "Fractionless float")]
    

class DatabaseConstants():
    """Database column names"""
    # Path to app's database file. By default is set to the mock database
    DATABASE_PATH = "mock.db"


    # Database table column name for each transaction's stock symbol
    STOCK_NAME = "stockname"

    # Database table column name for each transaction's stock amount
    STOCK_AMOUNT = "amount"

    # Database table column name for each transaction's stock price
    PRICE = "price"

    # Database table column name for each transaction's timestamp
    TIME = "timestamp"

    # Database table column name for usernames
    USERNAME = "username"

    # Database table column name for each user's cash
    CASH = "cash"


class BuyConstants():
    """Constants for Buy Page test module"""

    # Expected stock symbol input placeholder value (Buy page)
    EX_STOCK_SYMBOL_PH = "Symbol"

    # Expected stock symbol input default value (Buy page)
    EX_STOCK_SYMBOL_VALUE = ""

    # Expected stock amount input placeholder value (Buy page)
    EX_STOCK_AMOUNT_PH = "Shares"

    # Expected stock amount input default value (Buy page)
    EX_STOCK_AMOUNT_VALUE = ""


    # Expected flash alert message after succesfull purchase
    SUCC_BUY_MSG = "Bought!"


    # Expected error message for purchase attempts with empty stock symbol
    EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"

    # Expected error message for purchase attempts with invalid stock symbol
    INVALID_STOCK_SYMBOL = "INVALID SYMBOL"

    # Expected error message for purchase attempts with empty stock amount
    EMPTY_STOCK_AMOUNT = "MISSING SHARES"

    # Expected error message for purchase attempts with invalid stock amount
    INVALID_STOCK_AMOUNT = "INVALID SHARES"

    # Expected error message for purchase attempts with zero stock amount
    ZERO_AMOUNT = "TOO FEW SHARES"

    # Expected error message for purchase attempts with insufficient funds
    EXCEED_CASH = "CAN'T AFFORD"


    # Test values for cases of succesfull purchases
    SUCCESSFULL_PURCHASE_CASES = [(choice(SharedConstants.TEST_SYMBOLS), 1),
                                  (choice(SharedConstants.TEST_SYMBOLS).lower(), 10)]


class CommonConstants():
    """Constants for tests from the 'common' module"""

    # Expected Logo text for each page the user visits
    CS50_LOGO = "C$50Finance"


    # List of tuples containing expected page title for each page, specific to authenticated users
    AUTHED_PAGES = [(URLS.DEFAULT_URL, "C$50 Finance: Portfolio"),
                    (URLS.QUOTE_URL, "C$50 Finance: Quote"),
                    (URLS.BUY_URL, "C$50 Finance: Buy"),
                    (URLS.SELL_URL, "C$50 Finance: Sell"),
                    (URLS.HISTORY_URL, "C$50 Finance: History")]

    # List of tuples containing expected page title for each page,  specific to unauthenticated users
    UNAUTHED_PAGES = [(URLS.LOGIN_URL, "C$50 Finance: Log In"),
                      (URLS.REGISTER_URL, "C$50 Finance: Register")]
    

class DefaultConstants():
    """Constants for Default Page test module"""

    # Expected header name of the Default table column for stock symbols
    HEADER_SYMBOL = "Symbol"

    # Expected header name of the Default table column for company name
    HEADER_CNAME = "Name"

    # Expected header name of the Default table column for stock amount
    HEADER_AMOUNT = "Shares"

    # Expected header name of the Default table column for stock price
    HEADER_PRICE = "Price"

    # Expected header name of the Default table column for stock total
    HEADER_TOTAL = "TOTAL"


    # List of expected headers above
    EXPECTED_HEADERS = [HEADER_SYMBOL, 
                        HEADER_CNAME, 
                        HEADER_AMOUNT, 
                        HEADER_PRICE, 
                        HEADER_TOTAL]


class HistoryConstants():
    """Constants for History Page test module"""

    # Expected header name of the History table column for stock symbols
    HEADER_SYMBOL = "Symbol"

    # Expected header name of the History table column for stock amount
    HEADER_AMOUNT = "Shares"

    # Expected header name of the History table column for stock price
    HEADER_PRICE = "Price"

    # Expected header name of the History table column for the time of transaction
    HEADER_DATETIME = "Transacted"


    # List of expected headers above
    EXPECTED_HEADERS = [HEADER_SYMBOL, 
                        HEADER_AMOUNT, 
                        HEADER_PRICE, 
                        HEADER_DATETIME]
    

class LoginConstants():
    """Constants for Log in Page test module"""

    # Expected username input placeholder value (Log in page)
    EX_USERNAME_PH = "Username"

    # Expected username input default value (Log in page)
    EX_USERNAME_VALUE = ""

    # Expected password input placeholder value (Log in page)
    EX_PASSWORD_PH = "Password"

    # Expected password input default value (Log in page)
    EX_PASSWORD_VALUE = ""


    # Expected error message for log in attempts with empty username
    EMPTY_USERNAME_MSG = "MUST PROVIDE USERNAME"

    # Expected error message for log in attempts with empty password
    EMPTY_PASS_MSG = "MUST PROVIDE PASSWORD"

    # Expected error message for log in attempts with invalid username/password
    INVALID_CREDS_MSG = "INVALID USERNAME AND/OR PASSWORD"


    # Test values for cases of log in attempts with invalid username
    INVALID_LOGIN_CASES = [("", "Empty username"),
                            ("non-existent-username", "Non-existent username")]

    # Test values for cases of log in attempts with invalid password
    INVALID_PASSWORD_CASES = [("", "Empty password"),
                                ("non-existent-password", "Wrong password")]


class QuoteConstants():
    """Constants for Quote Page test module"""

    # Expected stock symbol input placeholder value (Quote page)
    EX_QUOTE_PH = "Symbol"

    # Expected stock symbol input default value (Quote page)
    EX_QUOTE_VALUE = ""


    # Expected error message for quote queries with empty stock symbol input
    EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"

    # Expected error message for quote queries with invalid stock symbol input
    INVALID_STOCK_SYMBOL = "INVALID SYMBOL"


class RegisterConstants():
    """Constants for Register Page test module"""

    # Expected username input placeholder value (Register page)
    EX_REG_UN_PH = "Username"

    # Expected username input default value (Register page)
    EX_USERNAME_VALUE = ""

    # Expected password input placeholder value (Register page)
    EX_REG_PW_PH = "Password"

    # Expected password input default value (Register page)
    EX_PASSWORD_VALUE = ""

    # Expected password confirmation input placeholder value (Register page)
    EX_REG_CONF_PH = "Password (again)"

    # Expected password confirmation input default value (Register page)
    EX_CONF_VALUE = ""


    # Expected flash alert message after succesfull registration
    SUCC_REG_MSG = "Registered!"


    # Expected error message for registration attempts with empty password
    ERROR_MSG_NO_PASSWORD = "MISSING PASSWORD"

    # Expected error message for registration attempts with different password/confirmation
    ERROR_MSG_WRONG_PASSWORD = "PASSWORDS DON'T MATCH"

    # Expected error message for registration attempts with existing username
    ERROR_MSG_NA_UN = "Username is not available"


    # Test values for cases of invalid username input
    INVALID_USERNAME_CASES = [("", "Empty username"), 
                              (" ", "Whitespaces only username (one)"),
                              ("              ", "Whitespaces only username (few)"),
                              ("placeholder_value", "Registering with the same username twice")]

    # Test values for cases of invalid password confirmation input
    INVALID_CONFIRM_CASES = [("", "Empty confirm"),
                             ("drow$$4P", "Valid confirm but mismatch with password")]

    # Test values for cases of invalid password input
    INVALID_PASSWORD_CASES = [("", "Empty password"),
                              pytest.param
                              (" ", "White-space password (one)", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to consist of white spaces")),
                              pytest.param
                              ("   ", "White-space password (few)", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to consist of white spaces")),
                              pytest.param
                              ("1234567890", "Numbers only pasword", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to be numbers only")),
                              pytest.param
                              ("abcdefgh", "Letters only pasword", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to be letters only")),
                              pytest.param
                              ("!@#$%^&*()", "Special characters only pasword", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to be typographical only")),
                              pytest.param
                              ("1qaz@wsx", "No uppercase letter pasword", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to not have uppercase letters")),
                              pytest.param
                              ("a", "Less than 8 characters PW (border case 1)", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to be less than 8 characters")),
                              pytest.param
                              ("1qaz@ws", "Less than 8 characters PW (border case 2)", marks=pytest.mark.xfail(
                                  reason="CS50 team's implementation allows for passwords to be less than 8 characters"))]
    

class SellConstants():
    """Constants for Sell Page test module"""

    # Expected stock symbol input default option name (Sell page)
    EX_SYMBOL_SELECT_DEFAULT = "Symbol"

    # Expected stock amount input placeholder value (Sell page)
    EX_AMOUNT_INPUT_PH = "Shares"

    # Expected stock amount input default value (Sell page)
    EX_AMOUNT_INPUT_VALUE = ""


    # Expected flash alert message after succesfull selling
    SUCC_SELL_MSG = "Sold!"


    # Expected error message for selling attempts with empty stock symbol
    EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"

    # Expected error message for selling attempts with unpossessed stocks 
    INVALID_STOCK_SYMBOL = "SYMBOL NOT OWNED"

    # Expected error message for selling attempts with empty stock amount 
    EMPTY_STOCK_AMOUNT = "MISSING SHARES"

    # Expected error message for selling attempts with invalid stock amount 
    INVALID_STOCK_AMOUNT = "INVALID SHARES"

    # Expected error message for selling attempts with negative stock amount 
    ZERO_AMOUNT = "SHARES MUST BE POSITIVE"

    # Expected error message for selling attempts with stock amount exceeding available amount
    EXCEED_AMOUNT = "TOO MANY SHARES"


    # Test values for cases of succesfull selling
    SUCCESSFULL_SELL_CASES = [(choice(SharedConstants.TEST_SYMBOLS), 1)]

    # Test values for cases of succesfull selling (multiple stocks)
    SUCCESSFULL_BATCH_SELLS = [([choice(SharedConstants.TEST_SYMBOLS), choice(SharedConstants.TEST_SYMBOLS).lower()], 
                                [1, 2])]
