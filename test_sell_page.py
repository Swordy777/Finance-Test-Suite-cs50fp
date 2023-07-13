import pytest
from random import choice

from pages.sell_page import SellPage
from pages.buy_page import BuyPage
from helpers import generate_tests_cls_parametrize, setup_page, zip_by_key
from constants import CommonConstants as CC, DatabaseConstants as DBC, SellConstants as SC, URLS


class TestSellPageBasics():
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def sell_page(self, browser, new_user):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    def test_has_stock_select_input(self, sell_page):
        """Verify presence of Stock symbol select input"""

        assert sell_page.symbol_select() is not None, (
            "Expected the Sell Page to have a dropdown list of possessed stocks"
            )


    def test_stock_select_is_unique(self, sell_page):
        """Verify that Stock symbol select input is one of a kind"""

        more_els = sell_page.more_symbol_selects()
        assert sell_page.is_unique(more_els), (
            f"Expected to find only one stock symbol select input on Sell page; found {len(more_els)}"
            )


    def test_stock_symbol_select_default_option(self, sell_page):
        """Verify Stock symbol select input's default option name"""

        symbol_select = sell_page.symbol_select_default_option()
        assert symbol_select.text == SC.EX_SYMBOL_SELECT_DEFAULT, (
            f"Expected symbol select input on the Sell page to have default value {SC.EX_SYMBOL_SELECT_DEFAULT}, " \
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
        assert amount_value == SC.EX_AMOUNT_INPUT_VALUE, (
            f"Expected stock amount input to be {'empty' if SC.EX_AMOUNT_INPUT_VALUE == '' else SC.EX_AMOUNT_INPUT_VALUE}, " \
                f"actual value: {amount_value}"
                )
        

    def test_stock_amount_input_placeholder(self, sell_page):
        """Verify Stock amount input's placeholder value"""

        amount_ph = sell_page.get_placeholder(sell_page.amount_input())
        assert amount_ph == SC.EX_AMOUNT_INPUT_PH, (
            f"Expected stock amount placeholder text to be {SC.EX_AMOUNT_INPUT_PH}, actual value: {amount_ph}"
            )
        

    def test_has_sell_button(self, sell_page):
        """Verify presence of Sell button"""

        assert sell_page.sell_button() is not None, (
            "Expected Sell page to have Sell button"
            )

    def test_sell_button_is_unique(self, sell_page):
        """Verify that Sell button is one of a kind"""

        more_els = sell_page.more_sell_buttons()
        assert sell_page.is_unique(more_els), (
            f"Expected to find only one Sell button on Sell page; found {len(more_els)}"
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
    def buy_stocks(self, browser, new_user, stock_symbols, stock_amounts, database, db_available):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """
        
        for symbol, amount in zip(stock_symbols, stock_amounts):
            if db_available:
                database.add_tran(new_user.username, symbol, amount, CC.MOCK_PRICE)
                database.change_cash_by(new_user.username, -CC.MOCK_PRICE * amount)
            else:
                buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
                buy_page.buy_stock(symbol, amount)



    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def symbol_select(self, sell_page):
        """
        This class only uses symbol input in its' tests.
        Initiate symbol input object and pass it to tests.
        """
        
        return sell_page.symbol_select()


    def test_number_of_options(self, symbol_select, database, db_available, new_user, stock_symbols):
        """Verify that number of available stock select input options corresponds with number of possessed stocks"""

        options_count = len([option.text for option in symbol_select.options][1:])
        if db_available:
            possessed_stocks = database.possessed_stock_names(new_user.username)
            # Have to check the type of possessed_stocks because of how query() method from database works
            stocks_count = len(possessed_stocks) if isinstance(possessed_stocks, list) else 1
        else:
            stocks_count = len(set([symbol.lower() for symbol in stock_symbols]))
        assert options_count == stocks_count, (
            f"Expected amount of select input options ({options_count}) to be equal to " \
                f"amount of unique possessed stocks ({stocks_count})"
                )


    def test_stock_select_input_has_owned_stock_symbols(self, symbol_select, stock_symbols):
        """Verify that available stock select input options correspond with possessed stocks"""

        options_names = [option.text for option in symbol_select.options][1:]
        for stock_symbol in stock_symbols:
            assert stock_symbol.upper() in options_names, (
                f"Expected to find {stock_symbol} in the dropdown list of stock symbols on Sell page; " \
                    f"actual options: {options_names}"
                    )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(StockSelectBehaviour,
                                                   "stock_symbols, stock_amounts",
                                                   SC.SUCCESSFULL_BATCH_SELLS
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class SuccessfullSelling():
    """
    Test app behaviour in case of successfull stock selling
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, stock_symbol, stock_amount, database, db_available):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        if db_available:
            database.add_tran(new_user.username, stock_symbol, stock_amount, CC.MOCK_PRICE)
            database.change_cash_by(new_user.username, -CC.MOCK_PRICE * stock_amount)
        else:
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(stock_symbol, stock_amount)

        # Return user's initial cash value before selling
        return database.users_cash(new_user.username) if db_available else None


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, new_user, stock_symbol, stock_amount, database):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        sell_page.sell_stock(stock_symbol, stock_amount)


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
        assert sell_alert.text == SC.SUCC_SELL_MSG, (
            f"Expected user to see {SC.SUCC_SELL_MSG} alert after successfull selling, actual text: {sell_alert.text}"
            )
        

    @pytest.mark.db_reliant
    def test_new_db_transaction(self, database, new_user):
        """Verify that new transaction was added to the database table"""

        users_tran_amount = len(database.transactions(new_user.username))
        assert users_tran_amount > 1, (
            f"Expected to find at least 2 transactions in database (buy and sell); actual count: {users_tran_amount}"
            )


    @pytest.mark.db_reliant
    def test_db_transaction_data(self, stock_symbol, stock_amount, database, new_user):
        """Verify correspondence of inputs and db data"""

        # Assemble expected values list
        ex_dict = {DBC.STOCK_NAME: stock_symbol.upper(), DBC.STOCK_AMOUNT: -stock_amount}

        last_transaction = database.last_tran(new_user.username) 
        matches = zip_by_key(last_transaction, ex_dict)
        # All of the expected values should have a match
        if len(matches) == len(ex_dict):
            for match in matches:
                assert match.actual == match.expected, (
                f"Expected for {match.key} in database table record to match with expected data {match.expected}; " \
                    f"actual value for {match.key}: {match.actual}"
                    )
        else:
            pytest.fail(reason="Expected to find all of the expected values in the database table record; " \
                        f"missing: {[k for k, v in ex_dict.items() if k not in last_transaction.keys()]}")


    @pytest.mark.db_reliant
    def test_db_cash_amount_changed(self, stock_amount, buy_stocks, new_user, database):
        """Verify that user's cash amount has changed accordingly"""

        current_cash = database.users_cash(new_user.username)
        last_transaction = database.last_tran(new_user.username) 
        expected_cash = buy_stocks + last_transaction[DBC.PRICE] * stock_amount
        assert current_cash == round(expected_cash, 2), (
            f"Expected db value of user's cash to be equal to {expected_cash}, actual amount: {current_cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(SuccessfullSelling,
                                                   "stock_symbol, stock_amount",
                                                   SC.SUCCESSFULL_SELL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountUntypableSell():
    """
    Test app behaviour in case of invalid amount input.
    Arbitrarily divided into "typable" and "untypable" values
    based on Chrome browser behaviour for "number" type inputs.
    Due to firefox having different behaviour for the same type of input
    utilizes some workarounds and conditionals for firefox tests
    """

    @pytest.fixture(autouse=True, scope="class")
    def pick_stock(self):
        """Pick random stock"""

        return choice(CC.TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, stock_amount, database, db_available):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        if db_available:
            database.add_tran(new_user.username, pick_stock, 1, CC.MOCK_PRICE)
            database.change_cash_by(new_user.username, -CC.MOCK_PRICE * 1)
        else:
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(pick_stock, 1)

        # Return user's initial cash value before selling
        return database.users_cash(new_user.username) if db_available else None


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        sell_page.sell_stock(pick_stock, stock_amount)


    @pytest.mark.firefox_only
    def test_firefox_untypable_behaviour(self, sell_page, case):
        """
        Verify front-end behaviour for Firefox browser.
        Unlike Chrome, Firefox accepts some input values
        but refuses to proceed if value type differs from
        the input type
        """

        exceptions = [CC.UNTYPABLE_AMOUNT_CASES[0][1], CC.UNTYPABLE_AMOUNT_CASES[7][1]]
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

        exceptions = [CC.UNTYPABLE_AMOUNT_CASES[0][1], CC.UNTYPABLE_AMOUNT_CASES[7][1]]
        error_text = sell_page.get_error_image_text()
        if case in exceptions:
            assert error_text == SC.EMPTY_STOCK_AMOUNT, (
                f"Expected error image to have text {SC.EMPTY_STOCK_AMOUNT}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message is expected to display in cases: {exceptions} " \
                f"but in case of {case} it also returned: {error_text}"
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
        assert error_text == SC.EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {SC.EMPTY_STOCK_AMOUNT} in case {case}, actual text: {error_text}"
            )
        

    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of possessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountUntypableSell,
                                                   "stock_amount, case",
                                                   CC.UNTYPABLE_AMOUNT_CASES
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

        return choice(CC.TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, stock_amount, database, db_available):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        if db_available:
            database.add_tran(new_user.username, pick_stock, 1, CC.MOCK_PRICE)
            database.change_cash_by(new_user.username, -CC.MOCK_PRICE * 1)
        else:
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(pick_stock, 1)

        # Return user's initial cash value before selling
        return database.users_cash(new_user.username) if db_available else None


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Performs stock selling with given stock symbol and amount.
        """
        
        sell_page.sell_stock(pick_stock, stock_amount)


    def test_typable_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        exceptions = [CC.TYPABLE_AMOUNT_CASES[3][1], CC.TYPABLE_AMOUNT_CASES[0][1], CC.TYPABLE_AMOUNT_CASES[4][1]]
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

        exceptions = {CC.TYPABLE_AMOUNT_CASES[3][1]: SC.EXCEED_AMOUNT,
                      CC.TYPABLE_AMOUNT_CASES[0][1]: SC.ZERO_AMOUNT,
                      CC.TYPABLE_AMOUNT_CASES[4][1]: SC.INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case in exceptions:
            ex_error = exceptions[case]

            assert error_text == ex_error, (
                f"Expected error image to have text {ex_error}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message is expected to display in cases: {[key for key in exceptions.keys()]} " \
                f"but in case of {case} it also returned: {error_text}"
                )


    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of possessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountTypableSell,
                                                   "stock_amount, case",
                                                   CC.TYPABLE_AMOUNT_CASES
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

        return choice(CC.TEST_SYMBOLS)


    @pytest.fixture(autouse=True, scope="class")
    def buy_stocks(self, browser, new_user, pick_stock, database, db_available):
        """
        Arrange fixture.
        Performs stock purchasing before selling.
        """

        if db_available:
            database.add_tran(new_user.username, pick_stock, 1, CC.MOCK_PRICE)
            database.change_cash_by(new_user.username, -CC.MOCK_PRICE * 1)
        else:
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(pick_stock, 1)

        # Return user's initial cash value before selling
        return database.users_cash(new_user.username) if db_available else None


    @pytest.fixture(autouse=True, scope="class")
    # Requires buy_stocks() as one of arguments to control the correct order of fixture execution
    def sell_page(self, browser, buy_stocks):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, pick_stock, stock_amount):
        """
        Act fixture.
        Input element's type is being set to text, allowing
        any type of value to be entered
        Performs purchase transaction with given Stock symbol and amount.
        """
        
        sell_page.set_type_to_text(sell_page.amount_input())
        sell_page.sell_stock(pick_stock, stock_amount)


    def test_backend_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        assert sell_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
            )
        

    def test_backend_error_message(self, sell_page, case):
        """Verify error image's message text"""

        cases = {CC.TYPABLE_AMOUNT_CASES[0][1]: SC.ZERO_AMOUNT,
                 CC.UNTYPABLE_AMOUNT_CASES[0][1]: SC.EMPTY_STOCK_AMOUNT,
                 CC.TYPABLE_AMOUNT_CASES[3][1]: SC.EXCEED_AMOUNT,
                 "default": SC.INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}")
        

    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        # Have to check the type of possessed_stocks because of how query() method from database works
        assert isinstance(database.transactions(new_user.username), dict), (
            "Expected user to have only one transaction - of buying the stock"
            )
        

    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user, buy_stocks):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == buy_stocks, (
            f"Expected db value of user's cash to be equal to {buy_stocks}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountBackendSell,
                                                   "stock_amount, case",
                                                   CC.TYPABLE_AMOUNT_CASES + CC.UNTYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidStockSymbolBackend():
    """
    Verify back-end algorithms when submitting invalid stock symbol value.
    """

    @pytest.fixture(autouse=True, scope="class")
    def sell_page(self, browser, new_user, stock_symbol, case):
        return setup_page(SellPage, browser, URLS.SELL_URL)


    @pytest.fixture(autouse=True, scope="class")
    def sell_stocks(self, sell_page, stock_symbol):
        """
        Act fixture.
        Replaces default option's value with a test value.
        After that, performs stock selling with given stock symbol and amount.
        """
        
        sell_page.add_value_to_default_select_option(stock_symbol)
        sell_page.sell_stock(stock_symbol, 1)


    def test_backend_behaviour(self, sell_page, case):
        """Verify presence of error image"""

        assert sell_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to sell stocks with: {case}"
            )
        

    def test_backend_error_message(self, sell_page, case):
        """Verify error image's message text"""

        cases = {CC.INVALID_SYMBOL_CASES[0][1]: SC.EMPTY_STOCK_SYMBOL,
                 "default": SC.INVALID_STOCK_SYMBOL}
        ex_error = None
        error_text = sell_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else: 
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )


    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        db_results = database.transactions(new_user.username)
        assert db_results is None, (
            "Expected user to have no transactions; you can't buy/sell invalid stocks"
            )
        

    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == CC.INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {CC.INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidStockSymbolBackend,
                                                   "stock_symbol, case",
                                                   CC.INVALID_SYMBOL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]