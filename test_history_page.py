import pytest
import time
from random import randint, choice

from pages.history_page import HistoryPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from pages.urls import URLS
from helpers import setup_page, lookup, compare_time
from constants import SharedConstants as SC, DatabaseConstants as DBC, HistoryConstants as HC




class TestHistoryBasics():
    """
    Verify presence of required elements; their titles, placeholders etc.
    + Default data test
    """

    @pytest.fixture(autouse=True, scope="class")
    def hist_page(self, browser, new_user):
        yield setup_page(HistoryPage, browser, URLS.HISTORY_URL)


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
            f"Expected for the History table to have {len(HC.EXPECTED_HEADERS)} headers; " \
                f"actual number of headers: {len(headers)}"
                )


    def test_header_titles(self, hist_page):
        """
        Verify history table header titles
        """

        headers = [header.text for header in hist_page.history_table_headers()]
        assert headers == HC.EXPECTED_HEADERS, (
            f"Expected History table to have {HC.EXPECTED_HEADERS} header names; actual list of header names: {headers}"
            )


    def test_history_table_empty_if_no_purchases(self, hist_page):
        """Verify new user's history table is empty"""
        
        table_rows = hist_page.history_rows()
        assert table_rows is None, (
            "Expected to find no rows in History table if no transactions were made"
            )
        

class TestHistoryTableDataDependencies():
    """
    Test correspondence of certain History table data with database values
    """

    @pytest.fixture(autouse=True, scope="class")
    def hist_page(self, browser, new_user):
        yield setup_page(HistoryPage, browser, URLS.HISTORY_URL)


    @pytest.fixture(scope="class")
    def mock_purchase_tran(self, database, new_user):
        """Add a mock buying transaction to user's transaction history"""

        test_symbol = choice(SC.TEST_SYMBOLS)
        test_amount = randint(1, 999)
        database.mock_db_add_tran(new_user.username, test_symbol, test_amount, SC.MOCK_PRICE)

        yield (test_symbol, test_amount)


    @pytest.fixture(scope="class")
    def mock_selling_tran(self, database, new_user, mock_purchase_tran):
        """Add a mock selling transaction to user's transaction history"""

        test_symbol, test_amount = mock_purchase_tran
        database.mock_db_add_tran(new_user.username, test_symbol, test_amount, -SC.MOCK_PRICE)


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_table_displays_data_after_purchase(self, hist_page, mock_purchase_tran):
        """Verify that if user bought a stock, then Default page table would have new rows"""

        hist_page.reload()
        assert hist_page.history_rows() is not None, (
            f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
            )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_rows_match_with_purchases(self, hist_page, mock_purchase_tran):
        """Verify that if user bought a stock, Default page would have the same amount of rows as unique possessed stocks"""

        hist_page.reload()
        row_count = len(hist_page.history_rows())
        assert row_count == 1, (
            f"Expected stock table's row count to be equal to amount of unique possessed stocks; actual count: {row_count}"
            )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_purchase_data_matches_db_data(self, hist_page, mock_purchase_tran):
        """Verify that table data corresponds with db data"""

        hist_page.reload()
        test_symbol, test_amount = mock_purchase_tran
        ex_table = {HC.HEADER_SYMBOL: test_symbol,
                    HC.HEADER_AMOUNT: test_amount,
                    HC.HEADER_PRICE: SC.MOCK_PRICE,
                    HC.HEADER_DATETIME: time.localtime()}
        table_data = hist_page.history_table_data()
        for tkey, exkey in zip(table_data, ex_table):
            if exkey == HC.HEADER_DATETIME:
                assert compare_time(table_data[tkey]), (
                f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                    f"actual value: {table_data[HC.HEADER_DATETIME]}"
                    )
            else:
                assert table_data[tkey] == ex_table[exkey], (
                f"Expected for {tkey} in Stock table to match with expected data {ex_table[exkey]}; " \
                    f"actual values for {tkey}: {table_data[tkey]}"
                    )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_selling_data_matches_db_data(self, hist_page, mock_selling_tran, mock_purchase_tran):
        """Verify that table data corresponds with db data"""

        hist_page.reload()
        test_symbol, test_amount = mock_purchase_tran
        ex_table = {HC.HEADER_SYMBOL: test_symbol,
                    HC.HEADER_AMOUNT: -test_amount,
                    HC.HEADER_PRICE: SC.MOCK_PRICE,
                    HC.HEADER_DATETIME: time.localtime()}
        table_data = hist_page.history_table_data()[-1]
        for tkey, exkey in zip(table_data, ex_table):
            if exkey == HC.HEADER_DATETIME:
                assert compare_time(table_data[tkey]), (
                f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                    f"actual value: {table_data[HC.HEADER_DATETIME]}"
                    )
            else:
                assert table_data[tkey] == ex_table[exkey], (
                f"Expected for {tkey} in Stock table to match with expected data {ex_table[exkey]}; " \
                    f"actual values for {tkey}: {table_data[tkey]}"
                    )
                

"""
Tests below were made before I decided to use the 'one test - one assert' concept.
They might be too unstable.
I decided to leave them as is for now.
"""

@pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 1)])
def test_history_table_shows_record_of_buying(browser, stock_symbol, stock_amount, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    buy_page.open()
    buy_page.buy_stock(stock_symbol, stock_amount)
    #"""
    # Insert data into mock database (comment out these lines if you have access to app's db)
    # Can give false results if price changes between the moment of selling and call lookup()
    stock_price = lookup(stock_symbol)['price']
    database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount, stock_price)
    #"""
    ex_dict = {HC.HEADER_SYMBOL: stock_symbol,
               HC.HEADER_AMOUNT: stock_amount,
               HC.HEADER_PRICE: stock_price,
               HC.HEADER_DATETIME: time.localtime()}
    hist_page = HistoryPage(browser, URLS.HISTORY_URL)
    hist_page.open()
    hist_td = hist_page.history_table_data()
    assert hist_td is not None, (
        f"Expected History table to have new row with transaction info"
        )
    db_records = database.last_tran(new_user.username)
    assert db_records is not None, (
        "Expected to find new rows in database containing transaction info for current user"
        )
    for tkey, dkey, exkey in zip(hist_td, db_records, ex_dict):
        if exkey != HC.HEADER_DATETIME:
            assert hist_td[tkey] == ex_dict[exkey], (
            f"Expected for {tkey} in History table to match with expected data {ex_dict[exkey]}; " \
                f"actual values for {tkey}: {hist_td[tkey]}"
                )
            assert db_records[dkey] == ex_dict[exkey], (
            f"Expected for {dkey} in db table to match with expected data {ex_dict[exkey]}; " \
                f"actual values for {dkey}: {db_records[dkey]}"
                )
        else:
            assert compare_time(hist_td[tkey]), (
                f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                    f"actual value: {hist_td[DBC.TIME]}"
                    )
            assert compare_time(db_records[dkey]), (
                f"Expected a new transaction row's timestamp in database to be ±5 sec from current time, " \
                    f"actual value: {db_records[DBC.TIME]}"
                    )


@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [1, 2])])
def test_history_table_shows_multiple_records_of_buying(browser, stock_symbols, stock_amounts, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call lookup()
        stock_price = lookup(symbol)['price']
        database.mock_db_add_tran(new_user.username, symbol, amount, stock_price)
        #"""
    # Assemble expected values list
    ex_values = []
    for symbol, amount in zip(stock_symbols, stock_amounts):
        ex_dict = {HC.HEADER_SYMBOL: symbol,
                   HC.HEADER_AMOUNT: amount,
                   HC.HEADER_PRICE: lookup(symbol)['price'],
                   HC.HEADER_DATETIME: time.localtime()}
        ex_values.append(ex_dict)
    hist_page = HistoryPage(browser, URLS.HISTORY_URL)
    hist_page.open()
    hist_td = hist_page.history_table_data()
    assert hist_td is not None, (
        f"Expected History table to have new row with transaction info"
        )
    db_records = database.transactions(new_user.username)
    assert db_records is not None, (
        "Expected to find new rows in database containing transaction info for current user"
        )
    for table_row, db_row, ex_dict in zip(hist_td, db_records, ex_values):
        for tkey, dkey, exkey in zip(table_row, db_row, ex_dict):
            if exkey != HC.HEADER_DATETIME:
                assert table_row[tkey] == ex_dict[exkey], (
                f"Expected for {tkey} in History table to match with expected data {ex_dict[exkey]}; " \
                    f"actual values for {tkey}: {table_row[tkey]}"
                    )
                assert db_row[dkey] == ex_dict[exkey], (
                f"Expected for {dkey} in db table to match with expected data {ex_dict[exkey]}; " \
                    f"actual values for {dkey}: {db_row[dkey]}"
                    )
            else:
                assert compare_time(table_row[tkey]), (
                f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                    f"actual value: {table_row[DBC.TIME]}"
                    )
                assert compare_time(db_row[dkey]), (
                f"Expected a new transaction row's timestamp in database to be ±5 sec from current time, " \
                    f"actual value: {db_records[DBC.TIME]}"
                    )


@pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 1)])
def test_history_table_shows_record_of_selling(browser, stock_symbol, stock_amount, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    buy_page.open()
    buy_page.buy_stock(stock_symbol, stock_amount)
    #"""
    # Insert data into mock database (comment out these lines if you have access to app's db)
    # Can give false results if price changes between the moment of selling and call lookup()
    stock_price = lookup(stock_symbol)['price']
    database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount, stock_price)
    #"""
    sell_page = SellPage(browser, URLS.SELL_URL)
    sell_page.open()
    sell_page.sell_stock(stock_symbol, stock_amount)
    #"""
    # Insert data into mock database (comment out these lines if you have access to app's db)
    # Can give false results if price changes between the moment of selling and call lookup()
    stock_price = lookup(stock_symbol)['price']
    database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount * (-1), stock_price)
    #"""
    ex_dict = {HC.HEADER_SYMBOL: stock_symbol,
               HC.HEADER_AMOUNT: stock_amount * (-1),
               HC.HEADER_PRICE: stock_price,
               HC.HEADER_DATETIME: time.localtime()}
    hist_page = HistoryPage(browser, URLS.HISTORY_URL)
    hist_page.open()
    hist_td = hist_page.history_table_data()[-1]
    db_records = database.last_tran(new_user.username)
    for tkey, dkey, exkey in zip(hist_td, db_records, ex_dict):
        if exkey != HC.HEADER_DATETIME:
            assert hist_td[tkey] == ex_dict[exkey], (
            f"Expected for {tkey} in History table to match with expected data {ex_dict[exkey]}; " \
                f"actual values for {tkey}: {hist_td[tkey]}"
                )
            assert db_records[dkey] == ex_dict[exkey], (
            f"Expected for {dkey} in db table to match with expected data {ex_dict[exkey]}; " \
                f"actual values for {dkey}: {db_records[dkey]}"
                )
        else:
            assert compare_time(hist_td[tkey]), (
                f"Expected a new transaction row's timestamp in History table to be ±5 sec from current time, " \
                    f"actual value: {hist_td[DBC.TIME]}"
                    )
            assert compare_time(db_records[dkey]), (
                f"Expected a new transaction row's timestamp in database to be ±5 sec from current time, " \
                    f"actual value: {db_records[DBC.TIME]}"
                    )