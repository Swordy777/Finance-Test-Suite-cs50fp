import pytest

from pages.sell_page import SellPage
from pages.buy_page import BuyPage
from pages.urls import URLS

SYMBOL_INPUT_PLACEHOLDER = "Symbol"
EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"
INVALID_STOCK_SYMBOL = "SYMBOL NOT OWNED"
SUCC_SELL_MSG = "Sold!"
EMPTY_STOCK_AMOUNT = "MISSING SHARES"
INVALID_STOCK_AMOUNT = "INVALID SHARES"
ZERO_AMOUNT = "SHARES MUST BE POSITIVE"
EXCEED_AMOUNT = "TOO MANY SHARES"

@pytest.mark.usefixtures("login")
class TestSellPageBasics():
    def test_has_stock_select_input(self, browser):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        symbol_input = sell_page.symbol_input()
        assert symbol_input is not None, "Expected the Sell Page to have a dropdown list of owned stocks"

    def test_stock_select_input_has_owned_stock_symbols(self, browser, database):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query if you're positive you're connected to the real db
        results = sell_page.query(database, "select stockname from purchases p join users u on p.user_id = u.id where u.username=? group by p.stockname having sum(p.amount) > 0;", "swordy")
        symbol_input = sell_page.symbol_input()
        options_names = [option.text for option in symbol_input.options][1:]
        for stock_symbol in results:
            assert stock_symbol['stockname'] in options_names, (
                f"Expected to find {stock_symbol.values()} in the dropdown list of stock symbols on Sell page")
        
    def test_has_stock_amount_input(self, browser):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        amount_input = sell_page.amount_input()
        assert amount_input is not None, "Expected the Sell Page to have stock amount input field"

    def test_has_sell_button(self, browser):
        sell_page = SellPage(browser, URLS.BUY_URL)
        sell_page.open()
        sell_button = sell_page.sell_button()
        assert sell_button is not None, "Expected Sell page to have sell button"
        
def test_new_user_has_no_stock_available_in_symbol_input(browser, new_user):
    sell_page = SellPage(browser, URLS.SELL_URL)
    sell_page.open()
    available_options = sell_page.symbol_input().options
    assert len(available_options) == 1, (
        f"Expected symbol input on the Sell page to have no stocks for a new user")
    assert available_options[0].text == SYMBOL_INPUT_PLACEHOLDER, (
        f"Expected symbol input on the Sell page to have only one option, called {SYMBOL_INPUT_PLACEHOLDER}, actual name: {available_options[0].text}")
    
class TestStockSelling():
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("MSFT","4","Symbol: All-caps, 1-digit amount")])
    def test_successfull_stock_selling(self, browser, stock_symbol, stock_amount, case, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert a purchase row into mock database
        buy_page.query(database, "insert into purchases (user_id, stockname, amount) values ((select id from users where username = ?), ?, ? )", new_user['username'], stock_symbol, int(stock_amount) * -1)
        buy_page.go_to_other_page(URLS.SELL_URL)
        sell_page = SellPage(browser, buy_page.get_current_url())
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        assert sell_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected to get redirected to Default page in case of {case} successfull selling, actual URL: {sell_page.get_current_url()}")
        sell_alert = sell_page.get_success_alert()
        assert sell_alert is not None, (
            f"Couldn't find success alert on default page after successfully selling stock(s)")
        assert sell_alert.text == SUCC_SELL_MSG, (
            f"Expected user to see {SUCC_SELL_MSG} alert after successfull selling, actual text: {sell_alert.text}")
        results = sell_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ? order by timestamp desc limit 1", new_user['username'])
        assert results is not None, "Expected to find a new row in database containing the latest purchase for current user"
        assert results['stockname'].upper() == stock_symbol.upper(), (
            f"Expected a new purchase row in database to have the same stock symbol as the one typed in by user, actual stock symbol in db: {results['stockname']}")
        assert results['amount'] == int(stock_amount) * -1, (
            f"Expected a new purchase row in database to have the same stock amount as the one typed in by user, actual stock amount in db: {results['amount']}")

    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("AAPL","","Empty stock amount"),
                                                                  ("AAPL"," ","White-space stock amount (one)"),
                                                                  ("AAPL","   ","White-space stock symbol (few)"),
                                                                  ("AAPL","two", "Letters in amount"),
                                                                  ("AAPL","$@%", "Special characters amount"),
                                                                  ("AAPL","пять", "Other alphabets amount #1"),
                                                                  ("AAPL","片仮名", "Other alphabets amount #2"),
                                                                  ("AAPL","💵", "Emoji stock symbol")])
    def test_untypable_invalid_stock_amount_selling(self, browser, stock_symbol, stock_amount, case, database, login):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = sell_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to sell stocks with: {case}")
        error_text = sell_page.get_error_text(error_image)
        assert error_text == EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {EMPTY_STOCK_AMOUNT}, actual text: {error_text}")
        
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("AAPL","0", "Zero amount"),
                                                                  ("AAPL","-5", "Negative amount"),
                                                                  ("AAPL","2.5", "Non-integer amount (period)"),
                                                                  ("AAPL","1,999", "Non-integer amount (comma)"),
                                                                  ("AAPL","5000", "Selling more than you posess")
                                                                  ])
    def test_typable_invalid_stock_amount_selling(self, browser, stock_symbol, stock_amount, case, database, login):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = sell_page.get_error_image()
        if case == "Non-integer amount (comma)" or case == "Selling more than you posess" or case == "Zero amount":
            assert error_image is not None, (
                f"Expected for application to display an error image with funny cat when trying to buy stocks with: {case}")
            error_text = sell_page.get_error_text(error_image)
            if case != "Zero amount":
                assert error_text == EXCEED_AMOUNT, (
                    f"Expected error image to have text {EXCEED_AMOUNT}, actual text: {error_text}")
            else:
                assert error_text == ZERO_AMOUNT, (
                    f"Expected error image to have text {ZERO_AMOUNT}, actual text: {error_text}")
        else:
            assert error_image is None, (
                f"Expected for application to not proceed with purchase due to incorrect amount value: {case}")
            
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("NFLX","1","Valid stock symbol, but not owned"),
                                                                  ("","1","Empty stock symbol"),
                                                                  (" ","1","White-space stock symbol (one)"),
                                                                  ("   ","1","White-space stock symbol (few)"),
                                                                  ("123","1", "Numbers only stock symbol"),
                                                                  ("0","1", "Zero stock symbol"),
                                                                  ("255.5","1", "Floating point number stock symbol"),
                                                                  ("128,0","1", "Floating point number (comma) stock symbol"),
                                                                  ("06.05.2023","1", "Date stock symbol"),
                                                                  ("NULL","1", "NULL symbol"),
                                                                  ("$@%?","1", "Special characters only stock symbol"),
                                                                  ("zyzx","1", "Non-existent stock symbol (only letters)"),
                                                                  ("$A23","1", "Non-existent stock symbol (combination)"),
                                                                  ("тест","1", "Other alphabets stock symbol #1"),
                                                                  ("片仮名","1", "Other alphabets stock symbol #2"),
                                                                  ("😍😍😍","1", "Emoji stock symbol")
                                                                  ])
    def test_invalid_stock_symbol_selling_backend_check(self, browser, stock_symbol, stock_amount, case, login):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.add_value_to_default_select_option(stock_symbol)
        sell_page.sell_stock(stock_symbol, stock_amount)
        error_image = sell_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to sell stocks with: {case}")
        error_text = sell_page.get_error_text(error_image)
        if case == "Empty stock symbol":
            assert error_text == EMPTY_STOCK_SYMBOL, (
                f"Expected error image to have text {EMPTY_STOCK_SYMBOL}, actual text: {error_text}")
        else:        
            assert error_text == INVALID_STOCK_SYMBOL, (
            f"Expected error image to have text {INVALID_STOCK_SYMBOL}, actual text: {error_text}")

    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("AAPL"," ","White-space stock amount (one)"),
                                                                  ("AAPL","   ","White-space stock symbol (few)"),
                                                                  ("AAPL","two", "Letters in amount"),
                                                                  ("AAPL","$@%", "Special characters amount"),
                                                                  ("AAPL","пять", "Other alphabets amount #1"),
                                                                  ("AAPL","片仮名", "Other alphabets amount #2"),
                                                                  ("AAPL","💵", "Emoji stock symbol"),
                                                                  ("AAPL","0", "Zero amount"),
                                                                  ("AAPL","-5", "Negative amount"),
                                                                  ("AAPL","2.5", "Non-integer amount (period)")
                                                                  ])
    def test_invalid_stock_amount_selling_backend_check(self, browser, stock_symbol, stock_amount, case, database, login):
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.hack_amount_input(sell_page.amount_input())
        sell_page.sell_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = sell_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to sell stocks with: {case}")
        error_text = sell_page.get_error_text(error_image)
        if case == "Zero amount":
            assert error_text == ZERO_AMOUNT, (
                f"Expected error image to have text {ZERO_AMOUNT}, actual text: {error_text}")
        else:
            assert error_text == INVALID_STOCK_AMOUNT, (
                f"Expected error image to have text {INVALID_STOCK_AMOUNT}, actual text: {error_text}")