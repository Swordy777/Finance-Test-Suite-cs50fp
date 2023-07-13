import pytest

from pages.default_page import DefaultPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from helpers import setup_page, zip_by_key
from constants import CommonConstants as CC, DefaultConstants as DC, DatabaseConstants as DBC, URLS


class TestDefaultPageBasics():
    """
    Verify presence of required elements; their titles, placeholders, etc.
    """
    
    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        return setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


    def test_has_stock_table(self, dft_page):
        """Verify presence of stock table"""

        assert dft_page.stocktable() is not None, (
            "Expected Default page to have stock table"
            )


    def test_stock_table_is_unique(self, dft_page):
        """Verify that stock table is one of a kind"""

        more_els = dft_page.more_stocktables()
        assert dft_page.is_unique(more_els), (
            f"Expected to find only one stock table on Default page; found {len(more_els)}"
            )


    def test_stocktable_has_headers(self, dft_page):
        """Verify presence of headers in stock table"""

        assert dft_page.stocktable_headers() is not None, (
            "Expected Default page stock table to have headers"
            )
        

    def test_header_count(self, dft_page):
        """Verify stock table header count"""
       
        header_count = len(dft_page.headers_names())
        assert header_count == len(DC.EXPECTED_HEADERS), (
            f"Expected stock table to have {len(DC.EXPECTED_HEADERS)} headers: {DC.EXPECTED_HEADERS}; " \
                f"actual header count: {header_count}"
                )
        

    def test_has_expected_header_titles(self, dft_page):
        """Verify stock table has the given header titles"""
       
        for expected_header in DC.EXPECTED_HEADERS:
            assert expected_header in dft_page.headers_names(), (
                f"Expected default table to have header named {expected_header}"
                )
            

    def test_has_cash_page_element(self, dft_page):
        """Verify presence of the element displaying user's cash"""

        assert dft_page.cash_element() is not None, (
            "Expected an element displaying user's current Cash amount to be present on the Default page"
            )


    def test_cash_elm_is_unique(self, dft_page):
        """Verify that Cash element is one of a kind"""

        more_els = dft_page.more_cash_elements()
        assert dft_page.is_unique(more_els), (
            f"Expected to find only one Cash element on Default page; found {len(more_els)}"
            )
        

    def test_has_total_page_element(self, dft_page):
        """Verify presence of the element displaying user's total amount of money"""

        assert dft_page.total_element() is not None, (
            "Expected an element displaying user's TOTAL amount of money to be present on the Default page"
            )


    def test_total_elm_is_unique(self, dft_page):
        """Verify that Total element is one of a kind"""

        more_els = dft_page.more_total_elements()
        assert dft_page.is_unique(more_els), (
            f"Expected to find only one total element on Default page; found {len(more_els)}"
            )


    def test_new_user_table_has_no_data(self, dft_page):
        """Verify that table doesn't have any stock rows by default"""

        assert dft_page.stocktable_rows() is None, (
            "Expected stock table to have no rows of purchased stocks for newly registered user"
            )


    def test_initial_cash_value(self, dft_page):
        """Verify displayed default cash value"""

        cash = dft_page.cash_elm_value()
        assert cash == CC.INITIAL_CASH, (
            f"Expected cash value to be {CC.INITIAL_CASH}, actual value: {cash} for newly registered user"
            )


    def test_initial_total_value(self, dft_page):
        """Verify displayed default total value"""

        total = dft_page.total_elm_value()
        assert total == CC.INITIAL_CASH, (
            f"Expected TOTAL value to be {CC.INITIAL_CASH}, actual value: {total} for newly registered user"
            )


@pytest.mark.db_reliant
@pytest.mark.parametrize("stock_symbols, stock_amounts", 
                         CC.TABLE_CASES,
                         scope="class")
class TestDefaultTableDependencies():
    """
    Test correspondence of certain default table data with database values
    """

    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        return setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


    @pytest.fixture(autouse=True, scope="class")
    def set_cash(self, database, new_user, stock_symbols, stock_amounts):
        """Set user's cash to a test value"""

        diff = 0
        for amount in stock_amounts:
            diff += CC.MOCK_PRICE * amount
        diff = round(diff, 2)

        database.change_cash_by(new_user.username, -diff)

        return CC.INITIAL_CASH - diff


    @pytest.fixture(scope="class")
    def mock_purchase_tran(self, database, new_user, stock_symbols, stock_amounts):
        """Add a mock purhase transaction to user's transaction history"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            database.add_tran(new_user.username, symbol, amount, CC.MOCK_PRICE)


    @pytest.fixture(scope="class")
    def mock_selling_tran(self, database, new_user, stock_symbols, stock_amounts, mock_purchase_tran):
        """Add a mock selling transaction to user's transaction history"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            database.add_tran(new_user.username, symbol, amount, -CC.MOCK_PRICE)


    def test_cash_is_read_from_db(self, dft_page, set_cash):
        """Verify that cash cell data is read from user's cash value in database"""

        dft_page.refresh()
        cash = dft_page.cash_elm_value()
        assert cash == set_cash, (
            f"Expected cash element value to be {set_cash}, as is in database; actual value: {cash}"
                )


    # Requires mock_purchase_tran() to be in list of arguments for correct order of fixture execution
    def test_total_equals_db_cash_plus_stock_value(self, dft_page, database, new_user, mock_purchase_tran):
        """Verify that user's TOTAL is a sum of their db cash value + value of all of the stocks"""

        dft_page.refresh()
        total_after_buying = dft_page.total_elm_value()
        total_comp = database.users_cash(new_user.username)
        table_data = dft_page.stocktable_cells()
        for row in table_data:
            total_comp += round(row[DC.HEADER_PRICE] * row[DC.HEADER_AMOUNT], 2)
        assert total_after_buying == round(total_comp, 2), (
            f"Expected total to equal the sum of db cash + stock value ({total_comp}); actual value: {total_after_buying}"
            )


    # Requires mock_purchase_tran() to be in list of arguments for correct order of fixture execution
    def test_table_data_matches_db_data(self, dft_page, database, new_user, mock_purchase_tran):
        """Verify that table data corresponds with db data"""

        dft_page.refresh()
        table_data = dft_page.stocktable_cells()
        db_data = database.possessed_stocks(new_user.username)
        db_list = []
        for db_row in db_data:
            db_dict = {DC.HEADER_SYMBOL: db_row[DBC.STOCK_NAME],
                       DC.HEADER_CNAME: db_row[DBC.STOCK_NAME],
                       DC.HEADER_AMOUNT: db_row[DBC.STOCK_AMOUNT]}
            db_list.append(db_dict)
        for db_dict, table_row in zip(db_list, table_data):
            matches = zip_by_key(table_row, db_dict)
            # All of the expected values should have a match
            if len(matches) == len(db_dict):
                for match in matches:
                    assert match.actual == match.expected, (
                    f"Expected for {match.key} in Stock table to match with expected data {match.expected}; " \
                        f"actual value for {match.key}: {match.actual}"
                        )
            else:
                pytest.fail(reason="Expected to find all of the expected values in the table; " \
                            f"missing: {[k for k, v in db_dict.items() if k not in table_row.keys()]}")


    # Requires mock_selling_tran() to be in list of arguments for correct order of fixture execution
    def test_table_is_empty_after_selling(self, dft_page, mock_selling_tran):
        """Verify that if user sold stock, then Default page table wouldn't have stock rows"""

        dft_page.refresh()
        assert dft_page.stocktable_rows() is None, (
            f"Expected stock table to have no rows after selling possessed stocks"
            )


@pytest.mark.parametrize("stock_symbols, stock_amounts", 
                         CC.TABLE_CASES,
                         scope="class")
class TestDefaultTableBehaviour():
    """
    Test what data displays in default table based on inputs.
    Simpler version of the TestTableDataDependencies() class
    due to absence of database access
    """

    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        return setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


    @pytest.fixture(scope="class")
    def buy_stocks(self, browser, stock_symbols, stock_amounts):
        """Buy stocks with given inputs"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(symbol, amount)


    @pytest.fixture(scope="class")
    def sell_stocks(self, browser, stock_symbols, stock_amounts, buy_stocks):
        """Sell stocks with given inputs"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            sell_page = setup_page(SellPage, browser, URLS.SELL_URL)
            sell_page.sell_stock(symbol, amount)


    # Requires buy_stocks() to be in list of arguments for correct order of fixture execution
    def test_table_displays_data_after_purchase(self, dft_page, buy_stocks):
        """Verify that if user bought a stock, then Default page table would have new rows"""

        assert dft_page.stocktable_rows() is not None, (
            f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
            )


    # Requires buy_stocks() to be in list of arguments for correct order of fixture execution 
    def test_rows_match_with_purchases(self, dft_page, buy_stocks, stock_symbols):
        """Verify that if user bought a stock, Default page would have the same amount of rows as unique possessed stocks"""

        row_count = len(dft_page.stocktable_rows())
        assert row_count == len(set(stock_symbols)), (
            f"Expected stock table's row count to be equal to amount of unique possessed stocks; actual count: {row_count}"
            )


    # Requires buy_stocks() to be in list of arguments for correct order of fixture execution
    def test_table_data_matches_inputs(self, dft_page, buy_stocks, stock_symbols, stock_amounts):
        """Verify that table data corresponds with inputs"""
            
        table_data = dft_page.stocktable_cells()
        ex_list = []
        for symbol, amount in zip(stock_symbols, stock_amounts):
            ex_dict = {DC.HEADER_SYMBOL: symbol,
                        DC.HEADER_CNAME: symbol,
                        DC.HEADER_AMOUNT: amount}
            ex_list.append(ex_dict)
        for ex_dict, table_row in zip(ex_list, table_data):
            matches = zip_by_key(table_row, ex_dict)
            # All of the expected values should have a match
            if len(matches) == len(ex_dict):
                for match in matches:
                    assert match.actual == match.expected, (
                    f"Expected for {match.key} in Stock table to match with expected data {match.expected}; " \
                        f"actual value for {match.key}: {match.actual}"
                        )
            else:
                pytest.fail(reason="Expected to find all of the expected values in the table; " \
                            f"missing: {[k for k, v in ex_dict.items() if k not in table_row.keys()]}")


    # Requires buy_stocks() to be in list of arguments for correct order of fixture execution
    def test_total_equals_cash_plus_stock_value(self, dft_page, buy_stocks):
        """Verify that user's TOTAL is a sum of current cash value + value of all of the stocks"""

        total_after_buying = dft_page.total_elm_value()
        total_comp = dft_page.cash_elm_value()
        table_data = dft_page.stocktable_cells()
        for row in table_data:
            total_comp += round(row[DC.HEADER_PRICE] * row[DC.HEADER_AMOUNT], 2)
        assert total_after_buying == round(total_comp, 2), (
            f"Expected total to equal the sum of leftover cash + stock value ({total_comp}); actual value: {total_after_buying}"
            )
    

    # Requires sell_stocks() to be in list of arguments for correct order of fixture execution
    def test_table_is_empty_after_selling(self, dft_page, sell_stocks):
        """Verify that if user sold their stocks, then Default page table wouldn't have stock rows"""

        assert dft_page.stocktable_rows() is None, (
            f"Expected stock table to have no rows after selling possessed stocks"
            )
        

@pytest.mark.parametrize("stock_symbols, stock_amounts", 
                         CC.TABLE_CASES,
                         scope="class")
class TestStockTotalEqualsAmountByPrice():
    """Verify that TOTAL column contains stock's amount multiplied by stock's price"""

    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        return setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


    @pytest.fixture(autouse=True, scope="class")
    def purchase_tran(self, browser, stock_symbols, stock_amounts, database, db_available, new_user):
        """Adds a mock transaction if database is available; otherwise executes basic stock purchase scenario"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            if db_available:
                database.add_tran(new_user.username, symbol, amount, CC.MOCK_PRICE)
                database.change_cash_by(new_user.username, -CC.MOCK_PRICE * amount)
            else:
                buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
                buy_page.buy_stock(symbol, amount)


    def test_stock_total_is_amount_by_price(self, dft_page, stock_symbols, stock_amounts, db_available):
        """Verify that TOTAL column of each default table row equals amount multiplied by stock price"""

        if db_available: 
            dft_page.refresh()
        table_data = dft_page.stocktable_cells()
        for symbol, amount in zip(stock_symbols, stock_amounts):
            for row in table_data:
                if symbol == row[DC.HEADER_SYMBOL]:
                    amount_by_price = round(amount * row[DC.HEADER_PRICE], 2)
                    assert row[DC.HEADER_TOTAL] == amount_by_price, (
                        f"Expected stock's {row[DC.HEADER_SYMBOL]} amount to equal {amount_by_price}, " \
                            f"actual value: {row[DC.HEADER_TOTAL]}"
                            )