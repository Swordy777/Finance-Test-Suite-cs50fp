import pytest
from random import choice

from pages.buy_page import BuyPage
from helpers import generate_tests_cls_parametrize, setup_page, zip_by_key
from constants import CommonConstants as CC, DatabaseConstants as DBC, BuyConstants as BC, URLS


class TestBuyPageBasics():      
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user):
        return setup_page(BuyPage, browser, URLS.BUY_URL)


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
        assert symbol_value == BC.EX_STOCK_SYMBOL_VALUE, (
            f"Expected stock symbol input to be {'empty' if BC.EX_STOCK_SYMBOL_VALUE == '' else BC.EX_STOCK_SYMBOL_VALUE}, " \
                f"actual value: {symbol_value}"
                )


    def test_stock_symbol_input_placeholder(self, buy_page):
        """Verify Stock symbol input's placeholder value"""

        symbol_ph = buy_page.get_placeholder(buy_page.symbol_input())
        assert symbol_ph == BC.EX_STOCK_SYMBOL_PH, (
            f"Expected stock symbol placeholder text to be {BC.EX_STOCK_SYMBOL_PH}, actual value: {symbol_ph}"
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
        assert amount_value == BC.EX_STOCK_AMOUNT_VALUE, (
            f"Expected stock amount input to be empty, actual value: {amount_value}"
            )
        

    def test_stock_amount_input_placeholder(self, buy_page):
        """Verify Stock amount input's placeholder value"""

        amount_ph = buy_page.get_placeholder(buy_page.amount_input())
        assert amount_ph == BC.EX_STOCK_AMOUNT_PH, (
            f"Expected stock amount placeholder text to be {BC.EX_STOCK_AMOUNT_PH}, actual value: {amount_ph}"
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
        return setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_symbol, stock_amount, db_available, database, new_user):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.buy_stock(stock_symbol, stock_amount)

        # Return data returned by database
        return database.possessed_stocks(new_user.username) if db_available else None


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
        assert alert_text == BC.SUCC_BUY_MSG, (
            f"Expected successfully registered user to see {BC.SUCC_BUY_MSG} alert , actual text: {alert_text}"
            )


    @pytest.mark.db_reliant
    def test_new_db_transaction(self, purchase):
        """Verify that new transaction was added to the database table"""

        assert purchase is not None, (
            "Expected to find a new row in database containing the latest purchase for current user"
            )
        

    @pytest.mark.db_reliant
    def test_db_transaction_data(self, purchase, stock_symbol, stock_amount):
        """Verify correspondence of inputs and db data"""
        
        # Assemble expected values list
        ex_dict = {DBC.STOCK_NAME: stock_symbol.upper(), 
                   DBC.STOCK_AMOUNT: stock_amount}

        matches = zip_by_key(purchase, ex_dict)
        # All of the expected values should have a match
        if len(matches) == len(ex_dict):
            for match in matches:
                assert match.actual == match.expected, (
                f"Expected for {match.key} in database table record to match with expected data {match.expected}; " \
                    f"actual value for {match.key}: {match.actual}"
                    )
        else:
            pytest.fail(reason="Expected to find all of the expected values in the database table record; " \
                        f"missing: {[k for k, v in ex_dict.items() if k not in purchase.keys()]}")


    @pytest.mark.db_reliant
    def test_db_cash_amount_changed(self, stock_amount, database, new_user, purchase):
        """Verify that user's cash amount has changed accordingly"""

        cash = database.users_cash(new_user.username)
        expected_cash = round(CC.INITIAL_CASH - purchase[DBC.PRICE] * stock_amount, 2)
        assert cash == expected_cash, (
            f"Expected db value of user's cash to be equal to {expected_cash}, actual amount: {cash}"
            )
        

# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(SuccessfullPurchase,
                                                   "stock_symbol, stock_amount",
                                                   BC.SUCCESSFULL_PURCHASE_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]



class InvalidSymbolPurchase():
    """
    Test app behaviour in case of invalid symbol input
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_symbol, case):
        return setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_symbol):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.buy_stock(stock_symbol, 1)


    def test_error_image_appears(self, buy_page, case):
        """Verify presence of error image"""

        assert buy_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
            )
        

    def test_correct_error_image_text(self, buy_page, case):
        """Verify error image's message text"""

        cases = {CC.INVALID_SYMBOL_CASES[0][1]: BC.EMPTY_STOCK_SYMBOL,
                 "default": BC.INVALID_STOCK_SYMBOL}
        ex_error = None
        error_text = buy_page.get_error_image_text()
        if case in cases:
            ex_error = BC.EMPTY_STOCK_SYMBOL
        else:
            ex_error = cases["default"]

        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}"
            )

    
    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        assert database.possessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == CC.INITIAL_CASH, (
            f"Expected user's cash value in database to be equal to {CC.INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidSymbolPurchase,
                                                   "stock_symbol, case",
                                                   CC.INVALID_SYMBOL_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountUntypableBuy():
    """
    Test app behaviour in case of invalid amount input.
    Arbitrarily divided into "typable" and "untypable" values
    based on Chrome browser behaviour for "number" type inputs.
    Due to firefox having different behaviour for the same type of input
    utilizes some workarounds and conditionals for firefox tests
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_amount, case):
        return setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.buy_stock(choice(CC.TEST_SYMBOLS), stock_amount)


    @pytest.mark.firefox_only
    def test_firefox_untypable_behaviour(self, buy_page, case):
        """
        Verify front-end behaviour for Firefox browser.
        Unlike Chrome, Firefox accepts some input values,
        but refuses to proceed with form submission
        if value type differs from the input type
        """

        exceptions = [CC.UNTYPABLE_AMOUNT_CASES[0][1],
                      CC.UNTYPABLE_AMOUNT_CASES[7][1]]
        error_image = buy_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to stay on Buy page and block redirect attempts with front-end means in case of: {case}"
                )


    @pytest.mark.firefox_only
    def test_firefox_error_message(self, buy_page, case):
        """Verify error image's message text for Firefox cases"""

        exceptions = [CC.UNTYPABLE_AMOUNT_CASES[0][1],
                      CC.UNTYPABLE_AMOUNT_CASES[7][1]]
        error_text = buy_page.get_error_image_text()
        if case in exceptions:
            assert error_text == BC.EMPTY_STOCK_AMOUNT, (
                f"Expected error image to have text {BC.EMPTY_STOCK_AMOUNT}, actual text: {error_text}"
                )
        else:
            assert error_text is None, (
                f"Error message is expected to display in cases: {exceptions} " \
                f"but in case of {case} it also returned: {error_text}"
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
        assert error_text == BC.EMPTY_STOCK_AMOUNT, (
            f"Expected error image to have text {BC.EMPTY_STOCK_AMOUNT} for case {case}, actual text: {error_text}"
            )
    

    @pytest.mark.db_reliant
    def test_no_db_transaction(self, database, new_user):
        """Verify that no transaction was added to the database table"""

        assert database.possessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == CC.INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {CC.INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountUntypableBuy,
                                                   "stock_amount, case",
                                                   CC.UNTYPABLE_AMOUNT_CASES
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
        return setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.buy_stock(choice(CC.TEST_SYMBOLS), stock_amount)


    def test_typable_behaviour(self, buy_page, case):
        """Verify presence of error image"""

        exceptions = [CC.TYPABLE_AMOUNT_CASES[3][1], 
                      CC.TYPABLE_AMOUNT_CASES[4][1]]
        error_image = buy_page.get_error_image()
        if case in exceptions:
            assert error_image is not None, (
                f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
                )
        else:
            assert error_image is None, (
                f"Expected for app to stay on Buy page and block redirect attempts with front-end means in case of: {case}"
                )
            

    def test_error_message(self, buy_page, case):
        """Verify error image's message text"""

        exceptions = {CC.TYPABLE_AMOUNT_CASES[3][1]: BC.EXCEED_CASH, 
                      CC.TYPABLE_AMOUNT_CASES[4][1]: BC.INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = buy_page.get_error_image_text()
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

        assert database.possessed_stocks(new_user.username) is None, (
            "Expected no new stock transactions to be added to database"
            )


    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == CC.INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {CC.INITIAL_CASH}, actual amount: {cash}"
            )


# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountTypableBuy,
                                                   "stock_amount, case",
                                                   CC.TYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]


class InvalidAmountBackendBuy():
    """
    Test back-end algorithms when submitting invalid amount value.
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_page(self, browser, new_user, stock_amount, case):
        return setup_page(BuyPage, browser, URLS.BUY_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase(self, buy_page, stock_amount):
        """
        Act fixture.
        Input element's type is being set to text, allowing
        any type of value to be entered
        Performs purchase transaction with given Stock symbol and amount.
        """

        buy_page.set_type_to_text(buy_page.amount_input())
        buy_page.buy_stock(choice(CC.TEST_SYMBOLS), stock_amount)


    def test_backend_behaviour(self, buy_page, case):
        """Verify presence of error image"""

        assert buy_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat when trying to buy stocks with: {case}"
            )
        

    def test_backend_error_message(self, buy_page, case):
        """Verify error image's message text"""

        cases = {CC.TYPABLE_AMOUNT_CASES[0][1]: BC.ZERO_AMOUNT,
                 CC.UNTYPABLE_AMOUNT_CASES[0][1]: BC.EMPTY_STOCK_AMOUNT,
                 CC.TYPABLE_AMOUNT_CASES[3][1]: BC.EXCEED_CASH,
                 "default": BC.INVALID_STOCK_AMOUNT}
        ex_error = None
        error_text = buy_page.get_error_image_text()

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

        db_results = database.possessed_stocks(new_user.username)
        assert db_results is None, (
            "Expected no new stock transactions to be added to database"
            )


    @pytest.mark.db_reliant
    def test_db_cash_amount_same(self, database, new_user):
        """Verify that user's cash value stays the same"""

        cash = database.users_cash(new_user.username)
        assert cash == CC.INITIAL_CASH, (
            f"Expected db value of user's cash to be equal to {CC.INITIAL_CASH}, actual amount: {cash}"
            )
        
        
# Generate parametrized classes from template:
generated_classes = generate_tests_cls_parametrize(InvalidAmountBackendBuy,
                                                   "stock_amount, case",
                                                   CC.UNTYPABLE_AMOUNT_CASES + CC.TYPABLE_AMOUNT_CASES
                                                   )
for class_name in generated_classes:
    locals()[class_name] = generated_classes[class_name]