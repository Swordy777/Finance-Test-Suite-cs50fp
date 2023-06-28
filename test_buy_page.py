import pytest
import time
from random import random, uniform, randint, choice

from pages.buy_page import BuyPage
from pages.urls import URLS
from helpers import generate_tests_cls_parametrize, setup_page


BP_EX_STOCK_SYMBOL_PH = "Symbol"
BP_EX_STOCK_SYMBOL_VALUE = ""
BP_EX_STOCK_AMOUNT_PH = "Shares"
BP_EX_STOCK_AMOUNT_VALUE = ""
BP_SUCC_BUY_MSG = "Bought!"
BP_EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"
BP_INVALID_STOCK_SYMBOL = "INVALID SYMBOL"
BP_EMPTY_STOCK_AMOUNT = "MISSING SHARES"
BP_INVALID_STOCK_AMOUNT = "INVALID SHARES"
BP_ZERO_AMOUNT = "TOO FEW SHARES"
BP_EXCEED_CASH = "CAN'T AFFORD"
BP_INITIAL_CASH = 10000.00
BP_MOCK_PRICE = 777.77

DB_STOCK_NAME = "stockname"
DB_STOCK_AMOUNT = "amount"
DB_PRICE = "price"

TEST_SYMBOLS = ["AAPL", "MSFT", "NFLX", "MCD"]

BP_SUCCESSFULL_PURCHASE_CASES = [(choice(TEST_SYMBOLS), 1),
                                 (choice(TEST_SYMBOLS).lower(), 10)]

BP_INVALID_SYMBOL_CASES = [("", "Empty stock symbol"),
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

BP_UNTYPABLE_AMOUNT_CASES = [("", "Empty stock amount"),
                             (" ", "White-space stock amount (one)"),
                             ("   ", "White-space stock amount (few)"),
                             ("two", "Letters in amount"),
                             ("$@%", "Special characters amount"),
                             ("пять", "Other alphabets amount #1"),
                             ("片仮名", "Other alphabets amount #2"),
                             ("💵💵💵", "Emoji stock amount"),
                             (",", "Comma")]

BP_TYPABLE_AMOUNT_CASES = [(0, "Zero amount"),
                           (randint(-10000, -1), "Negative amount"),
                           (round(int(random()*10) + uniform(0.1, 0.9), 1), "Float amount (period)"),
                           (randint(1000, 10000), "Buying more than affordable"),
                           (round((random()*10), 0), "Fractionless float")]


class TestBuyPageBasics():      
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    def test_has_stock_symbol_input(self, buy_page):
        """Verify presence of Stock symbol input"""

        assert buy_page.symbol_input() is not None, (
            "Expected Buy page to have stock symbol input field"
            )
        

    def test_stock_symbol_input_is_unique(self, buy_page):
        """Verify that Stock symbol input is one of a kind"""

        more_els = buy_page.more_symbol_inputs()
        assert buy_page.is_unique(more_els), (
            f"Expected to find only one stock symbol input field on Buy page; found {len(more_els)}"
            )
        

    def test_stock_symbol_input_default_value(self, buy_page):
        """Verify Stock symbol input's default value"""

        symbol_value = buy_page.get_value(buy_page.symbol_input())
        assert symbol_value == BP_EX_STOCK_SYMBOL_VALUE, (
            f"Expected stock symbol input to be {'empty' if BP_EX_STOCK_SYMBOL_VALUE == '' else BP_EX_STOCK_SYMBOL_VALUE}, " \
                f"actual value: {symbol_value}"
                )


    def test_stock_symbol_input_placeholder(self, buy_page):
        """Verify Stock symbol input's placeholder value"""

        symbol_ph = buy_page.get_placeholder(buy_page.symbol_input())
        assert symbol_ph == BP_EX_STOCK_SYMBOL_PH, (
            f"Expected stock symbol placeholder text to be {BP_EX_STOCK_SYMBOL_PH}, actual value: {symbol_ph}"
            )


    def test_has_stock_amount_input(self, buy_page):
        """Verify presence of Stock amount input"""

        assert buy_page.amount_input() is not None, (
            "Expected Buy page to have stock amount input field"
            )


    def test_stock_amount_input_is_unique(self, buy_page):
        """Verify that Stock amount input is one of a kind"""

        more_els = buy_page.more_amount_inputs()
        assert buy_page.is_unique(more_els), (
            f"Expected to find only one stock amount input field on Buy page; found {len(more_els)}"
            )
                

    def test_stock_amount_input_default_value(self, buy_page):
        """Verify Stock amount input's default value"""

        amount_value = buy_page.get_value(buy_page.amount_input())
        assert amount_value == BP_EX_STOCK_AMOUNT_VALUE, (
            f"Expected stock amount input to be empty, actual value: {amount_value}"
            )
        

    def test_stock_amount_input_placeholder(self, buy_page):
        """Verify Stock amount input's placeholder value"""

        amount_ph = buy_page.get_placeholder(buy_page.amount_input())
        assert amount_ph == BP_EX_STOCK_AMOUNT_PH, (
            f"Expected stock amount placeholder text to be {BP_EX_STOCK_AMOUNT_PH}, actual value: {amount_ph}"
            )
        

    def test_has_buy_button(self, buy_page):
        """Verify presence of Buy button"""

        assert buy_page.buy_button() is not None, (
            "Expected Buy page to have Buy button"
            )


    def test_buy_button_is_unique(self, buy_page):
        """Verify that Buy button is one of a kind"""

        more_els = buy_page.more_buy_buttons()
        assert buy_page.is_unique(more_els), (
            f"Expected to find only one Buy button on Buy page; found {len(more_els)}"
            )
        

class SuccessfullPurchase():
    """
    Test app behaviour in case of successfull stock purchase
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_symbol, stock_amount):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_symbol, stock_amount, database, new_user):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.buy_stock(stock_symbol, stock_amount)

        # Insert data into mock database
        # We can't check the price API so we use a mock value
        # COMMENT OUT THESE LINES if you have access to the app's database
        database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount, BP_MOCK_PRICE)
        database.mock_db_change_cash_by(new_user.username, -BP_MOCK_PRICE * stock_amount)

        # Yield data returned by database
        yield database.posessed_stocks(new_user.username)


    def test_redirect_to_default_page(self, buy_page):
        """Verify being redirected to Default page after succesfull purchase"""

        assert buy_page.url_should_change_to(URLS.DEFAULT_URL), (
            f"Expected to get redirected to Default page in case of successfull purchase, " \
                f"actual URL: {buy_page.get_current_url()}"
                )


    def test_has_success_alert(self, buy_page):
        """Verify presence of "success" alert"""

        assert buy_page.get_flash() is not None, (
            f"Couldn't find success alert on default page after successfully purchasing stock(s)"
            )
    

    def test_alert_message(self, buy_page):
        """Verify alert message"""

        alert_text = buy_page.get_flash().text
        assert alert_text == BP_SUCC_BUY_MSG, (
            f"Expected successfully registered user to see {BP_SUCC_BUY_MSG} alert , actual text: {alert_text}"
            )


    def test_new_db_transaction(self, purchase):
        """Verify that new transaction was added to the database table"""

        assert purchase is not None, (
            "Expected to find a new row in database containing the latest purchase for current user"
            )
        

    def test_db_transaction_data(self, purchase, stock_symbol, stock_amount):
        """Verify correspondence of inputs and db data"""
        
        # Assemble expected values list
        ex_dict = {DB_STOCK_NAME: stock_symbol.upper(), DB_STOCK_AMOUNT: stock_amount}
        
        # Can't test price value, because it's provided by API, for which we don't have testing tools
        # Uncomment this line only if you have access to app's database
        #ex_dict.update({DB_PRICE: BP_MOCK_PRICE})

        for db_key, ex_key in zip(purchase, ex_dict):
            if db_key == ex_key:
                assert purchase[db_key] == ex_dict[ex_key], (
                    f"Expected {db_key} database value {purchase[db_key]} to be equal to expected value {ex_dict[ex_key]}"
                    )


    def test_db_cash_amount_changed(self, stock_amount, database, new_user, purchase):
        """Verify that user's cash amount has changed accordingly"""

        cash = database.users_cash(new_user.username)
        expected_cash = BP_INITIAL_CASH - purchase[DB_PRICE] * stock_amount
        assert cash == expected_cash, (
            f"Expected db value of user's cash to be equal to {expected_cash}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(SuccessfullPurchase,
                                                   "stock_symbol, stock_amount",
                                                   BP_SUCCESSFULL_PURCHASE_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]



class InvalidSymbolPurchase():
    """
    Test app behaviour in case of invalid symbol input
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_symbol, case):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_symbol):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        # It's an invalid transaction, no need to add rows to mock db
        buy_page.buy_stock(stock_symbol, 1)


    def test_error_image_appears(self, buy_page, case):
        """Verify presence of error image"""

        assert buy_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
            )
        

    def test_correct_error_image_text(self, buy_page, case):
        """Verify error image's message text"""

        cases = {BP_INVALID_SYMBOL_CASES[0][1]: BP_EMPTY_STOCK_SYMBOL,
                 "default": BP_INVALID_STOCK_SYMBOL}
        ex_error = None
        error_text = buy_page.get_error_image_text()
        if case in cases:
            ex_error = BP_EMPTY_STOCK_SYMBOL
        else:
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )

    
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        assert database.posessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == BP_INITIAL_CASH, (
            f"Expected user's cash value in database to be equal to {BP_INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidSymbolPurchase,
                                                   "stock_symbol, case",
                                                   BP_INVALID_SYMBOL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountUntypableBuy():
    """
    Test app behaviour in case of invalid amount input.
    Arbitrarily divided into "typable" and "untypable" types of values
    based on Chrome browser input behaviour.
    Due to that has some badly designed firefox conditionals here and there.
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_amount, case):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        # It's an invalid transaction, no need to add rows to mock db
        buy_page.buy_stock(choice(TEST_SYMBOLS), stock_amount)


    @pytest.mark.firefox_only
    def test_firefox_untypable_behaviour(self, buy_page, case):
        """
        Verify front-end behaviour for Firefox browser.
        Unlike Chrome, Firefox accepts some input values,
        but refuses to proceed with form submission
        if value type differs from the input type
        """

        exceptions = [BP_UNTYPABLE_AMOUNT_CASES[0][1],
                      BP_UNTYPABLE_AMOUNT_CASES[7][1]]
        error_image = buy_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to not proceed with purchase due to invalid amount value: {case}"
                )


    @pytest.mark.firefox_only
    def test_firefox_error_message(self, buy_page, case):
        """Verify error image's message text for Firefox cases"""

        exceptions = [BP_UNTYPABLE_AMOUNT_CASES[0][1],
                      BP_UNTYPABLE_AMOUNT_CASES[7][1]]
        error_text = buy_page.get_error_image_text()
        if case in exceptions:
            assert error_text == BP_EMPTY_STOCK_AMOUNT, (
                f"Expected error image to have text {BP_EMPTY_STOCK_AMOUNT}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message test only applies to cases: {exceptions}"
                )


    @pytest.mark.chrome_only
    def test_chrome_untypable_behaviour(self, buy_page, case):
        """
        Verify front-end behaviour for Chrome browser.
        Normally would not allow to enter "untypable" values
        resulting in submitting an empty element
        """

        assert buy_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
            )
        

    @pytest.mark.chrome_only
    def test_chrome_error_message(self, buy_page, case):
        """Verify error image's message text for Chrome cases"""

        error_text = buy_page.get_error_image_text()
        assert error_text == BP_EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {BP_EMPTY_STOCK_AMOUNT} for case {case}, actual text: {error_text}"
            )
    

    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        assert database.posessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == BP_INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {BP_INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountUntypableBuy,
                                                   "stock_amount, case",
                                                   BP_UNTYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountTypableBuy():
    """
    "Typable" part of amount inputs division into separate classes.
    Although based on Chrome browser behaviour,
    also works the same for Firefox
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_amount, case):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        # It's an invalid transaction, no need to add rows to mock db
        buy_page.buy_stock(choice(TEST_SYMBOLS), stock_amount)


    def test_typable_behaviour(self, buy_page, case):
        """Verify presence of error image"""

        exceptions = [BP_TYPABLE_AMOUNT_CASES[3][1], 
                      BP_TYPABLE_AMOUNT_CASES[4][1]]
        error_image = buy_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to not proceed with purchase due to invalid amount value: {case}"
                )
            

    def test_error_message(self, buy_page, case):
        """Verify error image's message text"""

        exceptions = {BP_TYPABLE_AMOUNT_CASES[3][1]: BP_EXCEED_CASH, 
                      BP_TYPABLE_AMOUNT_CASES[4][1]: BP_INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = buy_page.get_error_image_text()
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

        assert database.posessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == BP_INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {BP_INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountTypableBuy,
                                                   "stock_amount, case",
                                                   BP_TYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountBackendBuy():
    """
    Test back-end algorithms when submitting invalid amount value.
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_amount, case):
        yield setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Input element's type is being set to text, allowing
        any type of value to be entered
        Performs purchase transaction with given Stock symbol and amount.
        """

        # It's an invalid transaction, no need to add rows to mock db
        buy_page.set_type_to_text(buy_page.amount_input())
        buy_page.buy_stock(choice(TEST_SYMBOLS), stock_amount)


    def test_backend_behaviour(self, buy_page, case):
        """Verify presence of error image"""

        assert buy_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
            )
        

    def test_backend_error_message(self, buy_page, case):
        """Verify error image's message text"""

        cases = {BP_TYPABLE_AMOUNT_CASES[0][1]: BP_ZERO_AMOUNT,
                      BP_UNTYPABLE_AMOUNT_CASES[0][1]: BP_EMPTY_STOCK_AMOUNT,
                      BP_TYPABLE_AMOUNT_CASES[3][1]: BP_EXCEED_CASH,
                      "default": BP_INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = buy_page.get_error_image_text()

        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )
        

    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        db_results = database.posessed_stocks(new_user.username)
        assert db_results is None, (
            "Expected no new stock transactions to be added to database"
            )


    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == BP_INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {BP_INITIAL_CASH}, actual amount: {cash}"
            )
        
        
# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountBackendBuy,
                                                   "stock_amount, case",
                                                   BP_UNTYPABLE_AMOUNT_CASES + BP_TYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]