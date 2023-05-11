import pytest

from pages.buy_page import BuyPage
from pages.urls import URLS

SUCC_BUY_MSG = "Bought!"
EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"
INVALID_STOCK_SYMBOL = "INVALID SYMBOL"
EMPTY_STOCK_AMOUNT = "MISSING SHARES"
INVALID_STOCK_AMOUNT = "INVALID SHARES"
ZERO_AMOUNT = "TOO FEW SHARES"
EXCEED_CASH = "CAN'T AFFORD"

class TestBuyPageBasics():
    def test_has_stock_symbol_input(self, browser):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        stock_symbol_input = buy_page.symbol_input()
        assert stock_symbol_input is not None, "Expected Buy page to have stock symbol input field"

    def test_has_stock_amount_input(self, browser):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        stock_amount_input = buy_page.amount_input()
        assert stock_amount_input is not None, "Expected Buy page to have stock amount input field"

    def test_has_buy_button(self, browser):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_button = buy_page.buy_button()
        assert buy_button is not None, "Expected Buy page to have buy button"


class TestStockPurchasing():
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("AAPL","1","Symbol: All-caps, 1-digit amount"),
                                                                  ("msft","10","Symbol: All-lowercase, 2-digit amount")])
    def test_successfull_purchase(self, browser, stock_symbol, stock_amount, case, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert a purchase row into mock database
        buy_page.query(database, "insert into purchases (user_id, stockname, amount) values ((select id from users where username = ?), ?, ? )", new_user['username'], stock_symbol, stock_amount)
        assert buy_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected to get redirected to Default page in case of {case} successfull purchase, actual URL: {buy_page.get_current_url()}")
        buy_alert = buy_page.get_success_alert()
        assert buy_alert is not None, (
            f"Couldn't find success alert on default page after successfully purchasing stock(s)")
        assert buy_alert.text == SUCC_BUY_MSG, (
            f"Expected successfully registered user to see {SUCC_BUY_MSG} alert , actual text: {buy_alert.text}")
        results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", new_user['username'])
        assert results is not None, "Expected to find a new row in database containing the latest purchase for current user"
        assert results['stockname'] == stock_symbol, (
            f"Expected a new purchase row in database to have the same stock symbol as the one typed in by user, actual stock symbol in db: {results['stockname']}")
        assert results['amount'] == int(stock_amount), (
            f"Expected a new purchase row in database to have the same stock amount as the one typed in by user, actual stock amount in db: {results['amount']}")
    
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("","1","Empty stock symbol"),
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
    def test_invalid_stock_symbol_purchase(self, browser, stock_symbol, stock_amount, case, database, login):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = buy_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to buy stocks with: {case}")
        error_text = buy_page.get_error_text(error_image)
        if case == "Empty stock symbol":
            assert error_text == EMPTY_STOCK_SYMBOL, (
                f"Expected error image to have text {EMPTY_STOCK_SYMBOL}, actual text: {error_text}")
        else:
            assert error_text == INVALID_STOCK_SYMBOL, (
                f"Expected error image to have text {INVALID_STOCK_SYMBOL}, actual text: {error_text}")

    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("AAPL","","Empty stock amount"),
                                                                  ("NFLX"," ","White-space stock amount (one)"),
                                                                  ("MSFT","   ","White-space stock symbol (few)"),
                                                                  ("MCD","two", "Letters in amount"),
                                                                  ("AAPL","$@%", "Special characters amount"),
                                                                  ("AAPL","пять", "Other alphabets amount #1"),
                                                                  ("AAPL","片仮名", "Other alphabets amount #2"),
                                                                  ("NFLX","💵", "Emoji stock symbol")])
    def test_untypable_invalid_stock_amount_purchase(self, browser, stock_symbol, stock_amount, case, database, login):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = buy_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to buy stocks with: {case}")
        error_text = buy_page.get_error_text(error_image)
        assert error_text == EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {EMPTY_STOCK_AMOUNT}, actual text: {error_text}")
        
    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("MCD","0", "Zero amount"),
                                                                  ("AAPL","-5", "Negative amount"),
                                                                  ("NFLX","2.5", "Non-integer amount (period)"),
                                                                  ("MSFT","1,999", "Non-integer amount (comma)"),
                                                                  ("AAPL","5000", "Buying more than affordable")
                                                                  ])
    def test_typable_invalid_stock_amount_purchase(self, browser, stock_symbol, stock_amount, case, database, login):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = buy_page.get_error_image()
        if case == "Non-integer amount (comma)" or case == "Buying more than affordable":
            assert error_image is not None, (
                f"Expected for application to display an error image with funny cat when trying to buy stocks with: {case}")
            error_text = buy_page.get_error_text(error_image)
            assert error_text == EXCEED_CASH, (
                f"Expected error image to have text {EXCEED_CASH}, actual text: {error_text}")
        else:
            assert error_image is None, (
                f"Expected for application to not proceed with purchase due to incorrect amount value: {case}")

    @pytest.mark.parametrize("stock_symbol, stock_amount, case", [("NFLX"," ","White-space stock amount (one)"),
                                                                  ("MSFT","   ","White-space stock symbol (few)"),
                                                                  ("MCD","two", "Letters in amount"),
                                                                  ("AAPL","$@%", "Special characters amount"),
                                                                  ("AAPL","пять", "Other alphabets amount #1"),
                                                                  ("AAPL","片仮名", "Other alphabets amount #2"),
                                                                  ("NFLX","💵", "Emoji stock symbol"),
                                                                  ("MCD","0", "Zero amount"),
                                                                  ("AAPL","-5", "Negative amount"),
                                                                  ("NFLX","2.5", "Non-integer amount (period)")
                                                                  ])
    def test_invalid_stock_amount_purchase_backend_check(self, browser, stock_symbol, stock_amount, case, database, login):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.hack_input(buy_page.amount_input())
        buy_page.buy_stock(stock_symbol, stock_amount)
        # TODO: avoid hardcoding the default user creds when querying the database
        # Checking the database is only applicable to the real database here, no point in querying the mock db
        # So uncomment the query and assert if you're positive you connect to the real db
        # results = buy_page.query(database, "select stockname, amount, price, timestamp from purchases p join users u on u.id = p.user_id where u.username = ?", "swordy")
        # assert results is None, "Expected to find no new rows of purchases for current user after unsuccessfull transaction"
        error_image = buy_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat when trying to buy stocks with: {case}")
        error_text = buy_page.get_error_text(error_image)
        if case == "Zero amount":
            assert error_text == ZERO_AMOUNT, (
                f"Expected error image to have text {ZERO_AMOUNT}, actual text: {error_text}")
        else:
            assert error_text == INVALID_STOCK_AMOUNT, (
                f"Expected error image to have text {INVALID_STOCK_AMOUNT}, actual text: {error_text}")