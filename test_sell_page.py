import pytest
import time
from random import random, uniform, randint, choice

from pages.sell_page import SellPage
from pages.buy_page import BuyPage
from pages.urls import URLS
from helpers import generate_tests_cls_parametrize, setup_page


SP_EX_SYMBOL_SELECT_DEFAULT = "Symbol"
SP_EX_AMOUNT_INPUT_VALUE = ""
SP_EX_AMOUNT_INPUT_PH = "Shares"

SP_EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"
SP_INVALID_STOCK_SYMBOL = "SYMBOL NOT OWNED"
SP_SUCC_SELL_MSG = "Sold!"
SP_EMPTY_STOCK_AMOUNT = "MISSING SHARES"
SP_INVALID_STOCK_AMOUNT = "INVALID SHARES"
SP_ZERO_AMOUNT = "SHARES MUST BE POSITIVE"
SP_EXCEED_AMOUNT = "TOO MANY SHARES"

SP_MOCK_PRICE = 777.7
SP_INITIAL_CASH = 10000.0

DB_STOCK_NAME = "stockname"
DB_STOCK_AMOUNT = "amount"
DB_PRICE = "price"

TEST_SYMBOLS = ["AAPL", "MSFT", "NFLX", "MCD"]

SP_SUCCESSFULL_SELL_CASES = [(choice(TEST_SYMBOLS), 1)]

SP_SUCCESSFULL_BATCH_SELLS = [([choice(TEST_SYMBOLS), choice(TEST_SYMBOLS).lower()], 
                               [1, 2])]

SP_INVALID_SYMBOL_CASES = [("", "Empty stock symbol"),
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

SP_UNTYPABLE_AMOUNT_CASES = [("", "Empty stock amount"),
                             (" ", "White-space stock amount (one)"),
                             ("   ", "White-space stock amount (few)"),
                             ("two", "Letters in amount"),
                             ("$@%", "Special characters amount"),
                             ("пять", "Other alphabets amount #1"),
                             ("片仮名", "Other alphabets amount #2"),
                             ("💵💵💵", "Emoji stock amount"),
                             (",", "Comma")]

SP_TYPABLE_AMOUNT_CASES = [(0, "Zero amount"),
                           (randint(-10000, -1), "Negative amount"),
                           (round(int(random()*10) + uniform(0.1, 0.9), 1), "Float amount (period)"),
                           (randint(1000, 10000), "Selling more than you posess"),
                           (round((random()*10), 0), "Fractionless float")]


class TestSellPageBasics():
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def sell_page(self, browser, new_user):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    def test_has_stock_select_input(self, sell_page):
        """Verify presence of Stock symbol select input"""

        assert sell_page.symbol_select() is not None, (
            "Expected the Sell Page to have a dropdown list of posessed stocks"
            )


    def test_stock_select_is_unique(self, sell_page):
        """Verify that Stock symbol select input is one of a kind"""

        more_els = sell_page.more_symbol_selects()
        assert sell_page.is_unique(more_els), (
            f"Expected to find only one stock symbol select input on Sell page; found {len(more_els)}"
            )


    def test_stock_symbol_select_default_value(self, sell_page):
        """Verify Stock symbol select input's default value"""

        symbol_select = sell_page.symbol_select_default_option()
        assert symbol_select.text == SP_EX_SYMBOL_SELECT_DEFAULT, (
            f"Expected symbol select input on the Sell page to have default value {SP_EX_SYMBOL_SELECT_DEFAULT}, " \
                f"actual name: {symbol_select.text}"
                )


    def test_has_stock_amount_input(self, sell_page):
        """Verify presence of Stock amount input"""

        assert sell_page.amount_input() is not None, (
            "Expected Sell page to have stock amount input field"
            )


    def test_stock_amount_input_is_unique(self, sell_page):
        """Verify that Stock amount input is one of a kind"""

        more_els = sell_page.more_amount_inputs()
        assert sell_page.is_unique(more_els), (
            f"Expected to find only one stock amount input field on Sell page; found {len(more_els)}"
            )
                

    def test_stock_amount_input_default_value(self, sell_page):
        """Verify Stock amount input's default value"""

        amount_value = sell_page.get_value(sell_page.amount_input())
        assert amount_value == SP_EX_AMOUNT_INPUT_VALUE, (
            f"Expected stock amount input to be {'empty' if SP_EX_AMOUNT_INPUT_VALUE == '' else SP_EX_AMOUNT_INPUT_VALUE}, " \
                f"actual value: {amount_value}"
                )
        

    def test_stock_amount_input_placeholder(self, sell_page):
        """Verify Stock amount input's placeholder value"""

        amount_ph = sell_page.get_placeholder(sell_page.amount_input())
        assert amount_ph == SP_EX_AMOUNT_INPUT_PH, (
            f"Expected stock amount placeholder text to be {SP_EX_AMOUNT_INPUT_PH}, actual value: {amount_ph}"
            )
        

    def test_has_buy_button(self, sell_page):
        """Verify presence of Sell button"""

        assert sell_page.sell_button() is not None, (
            "Expected Sell page to have Buy button"
            )

    def test_buy_button_is_unique(self, sell_page):
        """Verify that Sell button is one of a kind"""

        more_els = sell_page.more_sell_buttons()
        assert sell_page.is_unique(more_els), (
            f"Expected to find only one Buy button on Sell page; found {len(more_els)}"
            )
        

    def test_no_stocks_in_symbol_select(self, sell_page):
        """Verify that new users doesn't have any stocks available in stock select input"""
        
        assert len(sell_page.symbol_select().options) == 1, (
            f"Expected symbol input on the Sell page to have no stocks for a new user"
            )


class StockSelectBehaviour():
    """
    Test behaviour of stock select input 
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, stock_symbols, stock_amounts, database):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """
        
        buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
            # Insert data into mock database
            # We can't check the price API so we use a mock value
            # COMMENT OUT THESE LINES if you have access to the app's database
            database.mock_db_add_tran(new_user.username, symbol, amount, SP_MOCK_PRICE)
            database.mock_db_change_cash_by(new_user.username, -SP_MOCK_PRICE * amount)


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def symbol_select(self, sell_page):
        """
        This class only uses symbol input in its' tests.
        Initiate symbol input object and pass it to tests.
        """
        
        yield sell_page.symbol_select()


    def test_number_of_options(self, symbol_select, database, new_user):
        """Verify that number of available stock select input options corresponds with number of posessed stocks"""

        options_count = len([option.text for option in symbol_select.options][1:])
        posessed_stocks = database.posessed_stock_names(new_user.username)
        # Have to check the type of posessed_stocks because of how query() method from database works
        stocks_count = len(posessed_stocks) if isinstance(posessed_stocks, list) else 1
        assert options_count == stocks_count, (
            f"Expected amount of select input options ({options_count}) to be equal to " \
                f"amount of unique posessed stocks ({stocks_count})"
                )


    def test_stock_select_input_has_owned_stock_symbols(self, symbol_select, stock_symbols):
        """Verify that available stock select input options correspond with posessed stocks"""

        options_names = [option.text for option in symbol_select.options][1:]
        for stock_symbol in stock_symbols:
            assert stock_symbol.upper() in options_names, (
                f"Expected to find {stock_symbol} in the dropdown list of stock symbols on Sell page; " \
                    f"actual options: {options_names}"
                    )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(StockSelectBehaviour,
                                                   "stock_symbols, stock_amounts",
                                                   SP_SUCCESSFULL_BATCH_SELLS
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class SuccessfullSelling():
    """
    Test app behaviour in case of successfull stock selling
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, stock_symbol, stock_amount, database):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount, SP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, -SP_MOCK_PRICE * stock_amount)

        # Yield user's initial cash value before selling
        yield database.users_cash(new_user.username)


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, new_user, stock_symbol, stock_amount, database):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        sell_page.sell_stock(stock_symbol, stock_amount)
        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount * (-1), SP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, SP_MOCK_PRICE * stock_amount)


    def test_redirect_to_default_page(self, sell_page):
        """Verify being redirected to Default page after successfull selling"""

        assert sell_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected to get redirected to Default page in case of successfull selling, " \
                f"actual URL: {sell_page.get_current_url()}"
                )
        

    def test_has_success_alert(self, sell_page):
        """Verify presence of "success" alert"""

        assert sell_page.get_flash() is not None, (
            f"Couldn't find success alert on default page after successfully selling stock(s)"
            )
        

    def test_alert_message(self, sell_page):
        """Verify alert message"""

        sell_alert = sell_page.get_flash()
        assert sell_alert.text == SP_SUCC_SELL_MSG, (
            f"Expected user to see {SP_SUCC_SELL_MSG} alert after successfull selling, actual text: {sell_alert.text}"
            )
        

    def test_new_db_transaction(self, database, new_user):
        """Verify that new transaction was added to the database table"""

        users_tran_amount = len(database.transactions(new_user.username))
        assert users_tran_amount > 1, (
            f"Expected to find at least 2 transactions in database (buy and sell); actual count: {users_tran_amount}"
            )


    def test_db_transaction_data(self, stock_symbol, stock_amount, database, new_user):
        """Verify correspondence of inputs and db data"""

        # Assemble expected values list
        ex_dict = {DB_STOCK_NAME: stock_symbol.upper(), DB_STOCK_AMOUNT: -stock_amount}

        # Can't test price value, because it's provided by API, for which we don't have testing tools
        # Uncomment this line only if you have access to app's database
        ex_dict.update({DB_PRICE: SP_MOCK_PRICE})

        last_transaction = database.last_tran(new_user.username) 
        for db_key, ex_key in zip(last_transaction, ex_dict):
            assert last_transaction[db_key] == ex_dict[ex_key], (
                    f"Expected {db_key} database value {last_transaction[db_key]} to be equal to " \
                        f"expected value {ex_dict[ex_key]}"
                )


    def test_db_cash_amount_changed(self, stock_amount, buy_stocks, new_user, database):
        """Verify that user's cash amount has changed accordingly"""

        current_cash = database.users_cash(new_user.username)
        last_transaction = database.last_tran(new_user.username) 
        expected_cash = buy_stocks + last_transaction[DB_PRICE] * stock_amount
        assert current_cash == expected_cash, (
            f"Expected db value of user's cash to be equal to {expected_cash}, actual amount: {current_cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(SuccessfullSelling,
                                                   "stock_symbol, stock_amount",
                                                   SP_SUCCESSFULL_SELL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountUntypableSell():
    """
    Test app behaviour in case of invalid amount input
    Arbitrarily divided into "typable" and "untypable" types of values
    based on Chrome browser input behaviour.
    Due to that has some badly designed firefox conditionals here and there.
    """

    @pytest.fixture(autouse=True, scope="class")
    def pick_stock(self):
        """Pick random stock"""

        yield choice(TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, stock_amount, database):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
        buy_page.buy_stock(pick_stock, 1)
        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, pick_stock, 1, SP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, -SP_MOCK_PRICE)

        # Yield user's initial cash value before selling
        yield database.users_cash(new_user.username)


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        # It's an invalid transaction, no need to add rows to mock db
        sell_page.sell_stock(pick_stock, stock_amount)


    @pytest.mark.firefox_only
    def test_firefox_untypable_behaviour(self, sell_page, case):
        """
        Verify front-end behaviour for Firefox browser.
        Unlike Chrome, Firefox accepts some input values
        but refuses to proceed if value type differs from
        the input type
        """

        exceptions = [SP_UNTYPABLE_AMOUNT_CASES[0][1], SP_UNTYPABLE_AMOUNT_CASES[7][1]]
        error_image = sell_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to not proceed with purchase due to invalid amount value: {case}"
                )


    @pytest.mark.firefox_only
    def test_firefox_error_message(self, sell_page, case):
        """Verify error image's message text for Firefox cases"""

        exceptions = [SP_UNTYPABLE_AMOUNT_CASES[0][1], SP_UNTYPABLE_AMOUNT_CASES[7][1]]
        error_text = sell_page.get_error_image_text()
        if case in exceptions:
            assert error_text == SP_EMPTY_STOCK_AMOUNT, (
                f"Expected error image to have text {SP_EMPTY_STOCK_AMOUNT}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message test only applies to cases: {exceptions}"
                )



    @pytest.mark.chrome_only
    def test_chrome_untypable_behaviour(self, sell_page, case):
        """
        Verify front-end behaviour for Chrome browser.
        Normally would not allow to enter "untypable" values
        resulting in submitting an empty element
        """

        assert sell_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
            )
        

    @pytest.mark.chrome_only
    def test_chrome_error_message(self, sell_page, case):
        """Verify error image's message text for Chrome cases"""

        error_text = sell_page.get_error_image_text()
        assert error_text == SP_EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {SP_EMPTY_STOCK_AMOUNT} in case {case}, actual text: {error_text}"
            )
        

    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of posessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountUntypableSell,
                                                   "stock_amount, case",
                                                   SP_UNTYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountTypableSell():
    """
    "Typable" part of amount inputs division into separate classes.
    Although based on Chrome browser behaviour,
    also works the same for Firefox
    """

    @pytest.fixture(autouse=True, scope="class")
    def pick_stock(self):
        """Pick random stock"""

        yield choice(TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, stock_amount, database):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
        buy_page.buy_stock(pick_stock, 1)
        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, pick_stock, 1, SP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, -SP_MOCK_PRICE)

        # Yield user's initial cash value before selling
        yield database.users_cash(new_user.username)


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        # It's an invalid transaction, no need to add rows to mock db
        sell_page.sell_stock(pick_stock, stock_amount)


    def test_typable_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        exceptions = [SP_TYPABLE_AMOUNT_CASES[3][1], SP_TYPABLE_AMOUNT_CASES[0][1], SP_TYPABLE_AMOUNT_CASES[4][1]]
        error_image = sell_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to not proceed with selling due to invalid amount value: {case}"
                )
            

    def test_error_message(self, sell_page, case):
        """Verify error image's message text"""

        exceptions = {SP_TYPABLE_AMOUNT_CASES[3][1]: SP_EXCEED_AMOUNT,
                      SP_TYPABLE_AMOUNT_CASES[0][1]: SP_ZERO_AMOUNT,
                      SP_TYPABLE_AMOUNT_CASES[4][1]: SP_INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case in exceptions:
            ex_error = exceptions[case]

            assert error_text == ex_error, (
                f"Expected error image to have text {ex_error}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message test only applies to cases: {exceptions.keys()}"
                )



    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of posessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountTypableSell,
                                                   "stock_amount, case",
                                                   SP_TYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountBackendSell():
    """
    Test back-end algorithms when submitting invalid amount value.
    """

    @pytest.fixture(autouse=True, scope="class")
    def pick_stock(self):
        """Pick random stock"""

        yield choice(TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, database):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
        buy_page.buy_stock(pick_stock, 1)
        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, pick_stock, 1, SP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, -SP_MOCK_PRICE)

        # Yield user's initial cash value before selling
        yield database.users_cash(new_user.username)


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Input element's type is being set to text, allowing
        any type of value to be entered
        Performs purchase transaction with given Stock symbol and amount.
        """
        
        # It's an invalid transaction, no need to add rows to mock db
        sell_page.set_type_to_text(sell_page.amount_input())
        sell_page.sell_stock(pick_stock, stock_amount)


    def test_backend_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        assert sell_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
            )
        

    def test_backend_error_message(self, sell_page, case):
        """Verify error image's message text"""

        cases = {SP_TYPABLE_AMOUNT_CASES[0][1]: SP_ZERO_AMOUNT,
                 SP_UNTYPABLE_AMOUNT_CASES[0][1]: SP_EMPTY_STOCK_AMOUNT,
                 SP_TYPABLE_AMOUNT_CASES[3][1]: SP_EXCEED_AMOUNT,
                 "default": SP_INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}")
        
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of posessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountBackendSell,
                                                   "stock_amount, case",
                                                   SP_TYPABLE_AMOUNT_CASES + SP_UNTYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidStockSymbolBackend():
    """
    Verify back-end algorithms when submitting invalid stock symbol value.
    """

    @pytest.fixture(autouse=True, scope="class")
    def sell_page(self, browser, new_user, stock_symbol, case):
        yield setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, stock_symbol):
        """
        Act fixture.
        Replaces default option's value with a test value.
        After that, performs stock selling with given stock symbol and amount.
        """
        
        # It's an invalid transaction, no need to add rows to mock db
        sell_page.add_value_to_default_select_option(stock_symbol)
        sell_page.sell_stock(stock_symbol, 1)


    def test_backend_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        assert sell_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
            )
        

    def test_backend_error_message(self, sell_page, case):
        """Verify error image's message text"""

        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case == SP_INVALID_SYMBOL_CASES[0][1]:
            ex_error = SP_EMPTY_STOCK_SYMBOL
        else: 
            ex_error = SP_INVALID_STOCK_SYMBOL

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )


    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        db_results = database.transactions(new_user.username)
        assert db_results is None, (
            "Expected user to have no transactions; you can't buy/sell invalid stocks"
            )
        

    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == SP_INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {SP_INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidStockSymbolBackend,
                                                   "stock_symbol, case",
                                                   SP_INVALID_SYMBOL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]