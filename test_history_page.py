import pytest
import time

from pages.history_page import HistoryPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from helpers import setup_page, compare_time, zip_by_key
from constants import CommonConstants as CC, DatabaseConstants as DBC, HistoryConstants as HC, URLS


class TestHistoryBasics():
    """
    Verify presence of required elements; their titles, placeholders etc.
    + Default data test
    """

    @pytest.fixture(autouse=True, scope="class")
    def hist_page(self, browser, new_user):
        return setup_page(HistoryPage, browser, URLS.HISTORY_URL)


    def test_has_history_table(self, hist_page):
        """Verify presence of Stock symbol input"""

        assert hist_page.history_table() is not None, (
            "Expected History page to have history table"
            )


    def test_history_table_is_unique(self, hist_page):
        """Verify that stock table is one of a kind"""

        more_els = hist_page.more_history_tables()
        assert hist_page.is_unique(more_els), (
            f"Expected to find only one history table on History page; found {len(more_els)}"
            )
        

    def test_history_table_has_headers(self, hist_page):
        """Verify presence of headers in stock table"""

        assert hist_page.history_table_headers() is not None, (
            "Expected History table to have headers"
            )
        

    def test_header_count(self, hist_page):
        """Verify history table header count"""

        headers = hist_page.history_table_headers()
        assert len(headers) == len(HC.EXPECTED_HEADERS), (
            f"Expected stock table to have {len(HC.EXPECTED_HEADERS)} headers: {HC.EXPECTED_HEADERS}; " \
                f"actual header count: {len(headers)}"
                )
        

    def test_header_titles(self, hist_page):
        """Verify history table has the given header titles"""

        headers = [header.text for header in hist_page.history_table_headers()]
        for expected_header in HC.EXPECTED_HEADERS:
            assert expected_header in headers, (
                f"Expected History table to have header named {expected_header}"
                )


    def test_history_table_empty_if_no_purchases(self, hist_page):
        """Verify new user's history table is empty"""
        
        table_rows = hist_page.history_rows()
        assert table_rows is None, (
            "Expected to find no rows in History table if no transactions were made"
            )
        

@pytest.mark.db_reliant
@pytest.mark.parametrize("stock_symbols, stock_amounts", 
                         CC.TABLE_CASES,
                         scope="class")
class TestHistoryTableDataDependencies():
    """
    Test correspondence of History table data with database values
    """

    @pytest.fixture(autouse=True, scope="class")
    def add_mock_transactions(self, new_user, stock_symbols, stock_amounts, database):
        """Adds mock transactions to user's transaction history"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            database.add_tran(new_user.username, symbol, amount, CC.MOCK_PRICE)
            time.sleep(1)
            database.add_tran(new_user.username, symbol, -amount, CC.MOCK_PRICE)
            time.sleep(1)


    @pytest.fixture(autouse=True, scope="class")
    def hist_page(self, browser):
        return setup_page(HistoryPage, browser, URLS.HISTORY_URL)


    def test_table_displays_db_tran_data(self, hist_page):
        """Verify that if database has user transaction data, the history table would have new rows"""

        hist_page.refresh()
        assert hist_page.history_rows() is not None, (
            f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
            )


    def test_rows_match_with_db_tran_count(self, hist_page, stock_symbols):
        """Verify that History page would have the same count of rows as of unique database transactions"""

        hist_page.refresh()
        row_count = len(hist_page.history_rows())
        assert row_count == len(stock_symbols) * 2, (
            f"Expected stock table's row count to be equal to amount of unique possessed stocks; actual count: {row_count}"
            )
        

    def test_tran_data_matches_db_data(self, hist_page, database, new_user):
        """Verify that table data corresponds with database data"""
        
        hist_page.refresh()
        table_data = hist_page.history_table_data()
        db_data = database.transactions(new_user.username)
        db_list = []
        for db_row in db_data:
            db_dict = {HC.HEADER_SYMBOL: db_row[DBC.STOCK_NAME],
                       HC.HEADER_AMOUNT: db_row[DBC.STOCK_AMOUNT],
                       HC.HEADER_PRICE: db_row[DBC.PRICE],
                       HC.HEADER_DATETIME: db_row[DBC.TIME]}
            db_list.append(db_dict)
        # Reverse list of expected table records if tested app displays them in order from newest to oldest
        # db_list.reverse()
        for db_dict, table_row in zip(db_list, table_data):
            matches = zip_by_key(table_row, db_dict)
            # All of the expected values should have a match
            if len(matches) == len(db_dict):
                for match in matches:
                    assert match.actual == match.expected, (
                    f"Expected for {match.key} in History table to match with expected data {match.expected}; " \
                        f"actual value for {match.key}: {match.actual}"
                        )
            else:
                pytest.fail(reason="Expected to find all of the expected values in the table; " \
                            f"missing: {[k for k, v in db_dict.items() if k not in table_row.keys()]}")


@pytest.mark.parametrize("stock_symbols, stock_amounts", 
                         CC.TABLE_CASES,
                         scope="class")
class TestHistoryTableBehaviour():
    """
    Test what data displays in history table based on inputs.
    Simpler version of the TestHistoryTableDataDependencies() class
    due to absence of database access
    """

    @pytest.fixture(autouse=True, scope="class")
    def buy_and_sell(self, browser, new_user, stock_symbols, stock_amounts):
        """Buy and sell stocks with given inputs"""

        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page = setup_page(BuyPage, browser, URLS.BUY_URL)
            buy_page.buy_stock(symbol, amount)
            sell_page = setup_page(SellPage, browser, URLS.SELL_URL)
            sell_page.sell_stock(symbol, amount)


    @pytest.fixture(autouse=True, scope="class")
    def hist_page(self, browser):
        return setup_page(HistoryPage, browser, URLS.HISTORY_URL)


    def test_table_displays_tran_data(self, hist_page):
        """Verify that if user performed buying and selling transactions, the history table would have new rows"""

        assert hist_page.history_rows() is not None, (
            f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
            )


    def test_rows_match_with_tran_count(self, hist_page, stock_symbols):
        """Verify that if user bought a stock, History page would have the same count of rows as of unique transactions"""

        row_count = len(hist_page.history_rows())
        assert row_count == len(stock_symbols) * 2, (
            f"Expected stock table's row count to be equal to amount of unique possessed stocks; actual count: {row_count}"
            )
        

    def test_tran_data_matches_inputs(self, hist_page, stock_symbols, stock_amounts):
        """Verify that table data corresponds with inputs"""

        table_data = hist_page.history_table_data()
        ex_list = []
        for symbol, amount in zip(stock_symbols, stock_amounts):
            # Buy tran expected inputs
            ex_dict = {HC.HEADER_SYMBOL: symbol, HC.HEADER_AMOUNT: amount}
            ex_list.append(ex_dict)
            # Sell tran expected inputs
            ex_dict = {HC.HEADER_SYMBOL: symbol, HC.HEADER_AMOUNT: -amount}
            ex_list.append(ex_dict)
        # Reverse list of expected table records if tested app displays them in order from newest to oldest
        # ex_list.reverse()
        for ex_dict, table_row in zip(ex_list, table_data):
            matches = zip_by_key(table_row, ex_dict)
            # All of the expected values should have a match
            if len(matches) == len(ex_dict):
                for match in matches:
                    if match.key == HC.HEADER_DATETIME:
                        assert compare_time(match.actual), (
                        f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                            f"actual value: {match.actual}"
                            )
                    else:
                        assert match.actual == match.expected, (
                        f"Expected for {match.key} in History table to match with expected data {match.expected}; " \
                            f"actual values for {match.key}: {match.actual}"
                            )
            else:
                pytest.fail(reason="Expected to find all of the expected values in the table; " \
                            f"missing: {[k for k, v in ex_dict.items() if k not in table_row.keys()]}")


