import pytest
from random import random, randint, choice


from pages.default_page import DefaultPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from pages.urls import URLS
from helpers import generate_tests_cls_parametrize, setup_page, lookup


DT_HEADER_SYMBOL = "Symbol"
DT_HEADER_CNAME = "Name"
DT_HEADER_AMOUNT = "Shares"
DT_HEADER_PRICE = "Price"
DT_HEADER_TOTAL = "TOTAL"
EXPECTED_HEADERS = [DT_HEADER_SYMBOL, DT_HEADER_CNAME, DT_HEADER_AMOUNT, DT_HEADER_PRICE, DT_HEADER_TOTAL]

DP_INITIAL_CASH = 10000.00
DP_MOCK_PRICE = 777.7

DB_STOCK_NAME = "stockname"
DB_STOCK_AMOUNT = "amount"
DB_PRICE = "price"

TEST_SYMBOLS = ["AAPL", "MSFT", "NFLX", "MCD"]


class TestDefaultPageBasics():
    """
    Verify presence of required elements; their titles, placeholders, etc.
    """
    
    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        yield setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


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
        assert header_count == len(EXPECTED_HEADERS), (
            f"Expected stock table to have {len(EXPECTED_HEADERS)} headers: {EXPECTED_HEADERS}; " \
                f"actual header count: {header_count}"
                )
        

    def test_header_titles(self, dft_page):
        """Verify stock table header titles"""
       
        for header, ex_header in zip(dft_page.headers_names(), EXPECTED_HEADERS):
            assert header == ex_header, (
                f"Expected table header {header} to have a name {ex_header}"
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
        assert cash == DP_INITIAL_CASH, (
            f"Expected cash value to be {DP_INITIAL_CASH}, actual value: {cash} for newly registered user"
            )


    def test_initial_total_value(self, dft_page):
        """Verify displayed default total value"""

        total = dft_page.total_elm_value()
        assert total == DP_INITIAL_CASH, (
            f"Expected TOTAL value to be {DP_INITIAL_CASH}, actual value: {total} for newly registered user"
            )


class TestTableDataDependencies():
    """
    Test correspondence of certain table data with database values
    """

    @pytest.fixture(autouse=True, scope="class")
    def dft_page(self, browser, new_user):
        yield setup_page(DefaultPage, browser, URLS.DEFAULT_URL)


    @pytest.fixture(autouse=True, scope="class")
    def set_cash(self, database, new_user):
        """Set user's cash to a test value"""

        database.mock_db_change_cash_by(new_user.username, -DP_MOCK_PRICE)


    @pytest.fixture(scope="class")
    def mock_purchase_tran(self, database, new_user):
        """Add a mock buying transaction to user's transaction history"""

        test_symbol = choice(TEST_SYMBOLS)
        test_amount = randint(1, 999)
        database.mock_db_add_tran(new_user.username, test_symbol, test_amount, DP_MOCK_PRICE)

        yield (test_symbol, test_amount)


    @pytest.fixture(scope="class")
    def mock_selling_tran(self, database, new_user, mock_purchase_tran):
        """Add a mock selling transaction to user's transaction history"""

        test_symbol, test_amount = mock_purchase_tran
        database.mock_db_add_tran(new_user.username, test_symbol, test_amount, -DP_MOCK_PRICE)


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    def test_cash_is_read_from_db(self, dft_page):
        """Verify that cash cell data is read from user's cash value in database"""

        dft_page.reload()
        cash = dft_page.cash_elm_value()
        assert cash == DP_INITIAL_CASH - DP_MOCK_PRICE, (
            f"Expected cash element value to be {DP_INITIAL_CASH - DP_MOCK_PRICE}, as is in database; actual value: {cash}"
                )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_table_displays_data_after_purchase(self, dft_page, mock_purchase_tran):
        """Verify that if user bought a stock, then Default page table would have new rows"""

        dft_page.reload()
        assert dft_page.stocktable_rows() is not None, (
            f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
            )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_rows_match_with_purchases(self, dft_page, mock_purchase_tran):
        """Verify that if user bought a stock, Default page would have the same amount of rows as unique posessed stocks"""

        dft_page.reload()
        row_count = len(dft_page.stocktable_rows())
        assert row_count == 1, (
            f"Expected stock table's row count to be equal to amount of unique posessed stocks; actual count: {row_count}"
            )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_purchase_tran() to be in list of arguments, since this is where we want it to execute 
    def test_table_data_matches_db_data(self, dft_page, mock_purchase_tran):
        """Verify that table data corresponds with db data"""

        dft_page.reload()
        test_symbol, test_amount = mock_purchase_tran
        ex_table = {DT_HEADER_SYMBOL: test_symbol,
                    DT_HEADER_CNAME: test_symbol,
                    DT_HEADER_AMOUNT: test_amount,
                    DT_HEADER_PRICE: DP_MOCK_PRICE}
        table_data = dft_page.stocktable_cells()
        for tkey, exkey in zip(table_data, ex_table):
            assert table_data[tkey] == ex_table[exkey], (
            f"Expected for {tkey} in Stock table to match with expected data {ex_table[exkey]}; " \
                f"actual values for {tkey}: {table_data[tkey]}"
                )


    @pytest.mark.xfail(reason="This test will fail if you don't have access to app's database")
    # Requires mock_selling_tran() to be in list of arguments, since this is where we want it to execute 
    def test_table_is_empty_after_selling(self, dft_page, mock_selling_tran):
        """Verify that if user sold stock, then Default page table wouldn't have stock rows"""

        dft_page.reload()
        assert dft_page.stocktable_rows() is None, (
            f"Expected stock table to have no rows after selling posessed stocks"
            )
        

"""
Tests below were made before I decided to use the 'one test - one assert' concept.
They might be too complex, inefficient or unreliable.
I decided to leave them as is for now.
"""

@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
def test_table_has_new_rows_after_buying_stocks(browser, stock_symbols, stock_amounts, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of buying and call to lookup()
        stock_price = lookup(symbol)['price']
        database.mock_db_add_tran(new_user.username, symbol, amount, stock_price)
        #"""
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    stock_rows = dft_page.stocktable_rows()
    assert stock_rows is not None, (
        f"Expected stock table to have new rows of data after purchasing stocks; but it is empty"
        )
    assert len(stock_rows) == len(stock_symbols), (
        f"Expected stock table to have {len(stock_symbols)} rows of data after purchasing stocks; " \
            f"actual number of rows: {stock_rows}"
            )
    db_results = database.posessed_stock_names(new_user.username)
    assert db_results is not None, (
        "Expected db table to have new rows of data after purchasing stocks; but it is empty"
        )
    assert len(db_results) == len(stock_symbols), (
        f"Expected db table to have {len(stock_symbols)} rows of data after purchasing stocks; " \
            f"actual number of rows: {stock_rows}"
            )


@pytest.mark.parametrize("stock_symbol, stock_amount, company_name", [("NFLX", 12, "NFLX")])
def test_table_has_correct_stock_info(browser, stock_symbol, stock_amount, company_name, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    buy_page.open()
    buy_page.buy_stock(stock_symbol, stock_amount)
    #"""
    # Insert data into mock database (comment out these lines if you have access to app's db)
    # Can give false results if price changes between the moment of selling and call to lookup()
    stock_price = lookup(stock_symbol)['price']
    database.mock_db_add_tran(new_user.username, stock_symbol, stock_amount, stock_price)
    #"""
    ex_table = {DT_HEADER_SYMBOL: stock_symbol,
               DT_HEADER_CNAME: company_name,
               DT_HEADER_AMOUNT: stock_amount,
               DT_HEADER_PRICE: stock_price}
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    table_data = dft_page.stocktable_cells()
    assert table_data is not None, (
        f"Expected stock table to have a new row of data after making a purchase; but it is empty"
        )
    for tkey, exkey in zip(table_data, ex_table):
        assert table_data[tkey] == ex_table[exkey], (
        f"Expected for {tkey} in Stock table to match with expected data {ex_table[exkey]}; " \
            f"actual values for {tkey}: {table_data[tkey]}"
            )
    ex_db = {DT_HEADER_SYMBOL: stock_symbol,
             DT_HEADER_AMOUNT: stock_amount,
             DT_HEADER_PRICE: stock_price}
    db_records = database.posessed_stocks(new_user.username)
    assert db_records is not None, (
        "Expected to find a new row in database containing the latest purchase for current user"
        )
    for dkey, exkey in zip(db_records, ex_db):
        assert db_records[dkey] == ex_db[exkey], (
        f"Expected for {dkey} in db table to match with expected data {ex_db[exkey]}; " \
            f"actual values for {dkey}: {db_records[dkey]}"
            )
        

@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
def test_stock_total_should_equal_amount_x_price(stock_symbols, stock_amounts, browser, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    table_data = dft_page.stocktable_cells()
    for row in table_data:
        amount_x_price = round(row[DT_HEADER_AMOUNT] * row[DT_HEADER_PRICE], 2)
        assert row[DT_HEADER_TOTAL] == amount_x_price, (
            f"Expected stock's {row[DT_HEADER_SYMBOL]} amount to equal {amount_x_price}, " \
                f"actual value: {row[DT_HEADER_TOTAL]}"
                )


@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
def test_table_has_no_data_if_purchased_and_sold(browser, stock_symbols, stock_amounts, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call to lookup()
        price = lookup(symbol)['price']
        database.mock_db_add_tran(new_user.username, symbol, amount, price)
        #"""
    sell_page = SellPage(browser, URLS.SELL_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        sell_page.open()
        sell_page.sell_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call to lookup()
        price = lookup(symbol)['price']
        database.mock_db_add_tran(new_user.username, symbol, amount * (-1), price)
        #"""
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    stock_rows = dft_page.stocktable_rows()
    assert stock_rows is None, (
        "Expected stock table to have no rows of data if user sold all their stocks"
        )
    db_results = database.posessed_stock_names(new_user.username)
    assert db_results is None, (
        "Expected db table to have no stocks with a sum greater than zero"
        )


@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
def test_total_equals_cash_plus_stock_value(stock_symbols, stock_amounts, browser, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call to lookup()
        price = lookup(symbol)['price']
        database.mock_db_change_cash_by(new_user.username, price * amount * (-1))
        database.mock_db_add_tran(new_user.username, symbol, amount, price)
        #"""
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    total_after_buying = dft_page.total_elm_value()
    total_comp = dft_page.cash_elm_value()
    table_data = dft_page.stocktable_cells()
    for row in table_data:
        total_comp += round(row[DT_HEADER_PRICE] * row[DT_HEADER_AMOUNT], 2)
    assert total_after_buying == total_comp, (
        f"Expected total to equal the sum of leftover cash + stock value ({total_comp}); actual value: {total_after_buying}"
        )


@pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
def test_total_equals_cash_after_selling_everything(stock_symbols, stock_amounts, browser, database, new_user):
    buy_page = BuyPage(browser, URLS.BUY_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        buy_page.open()
        buy_page.buy_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call to lookup()
        price = lookup(symbol)['price']
        database.mock_db_change_cash_by(new_user.username, price * amount * (-1))
        database.mock_db_add_tran(new_user.username, symbol, amount, price)
        #"""
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    sell_page = SellPage(browser, URLS.SELL_URL)
    for symbol, amount in zip(stock_symbols, stock_amounts):
        sell_page.open()
        sell_page.sell_stock(symbol, amount)
        #"""
        # Insert data into mock database (comment out these lines if you have access to app's db)
        # Can give false results if price changes between the moment of selling and call to lookup()
        price = lookup(symbol)['price']
        database.mock_db_change_cash_by(new_user.username, price * amount)
        database.mock_db_add_tran(new_user.username, symbol, amount * (-1), price)
        #"""
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    total = dft_page.total_elm_value()
    cash = dft_page.cash_elm_value()
    assert total == cash, (
        f"Expected total to equal cash earned from selling all the stocks ({cash}); actual value: {total}"
        )
    db_cash = database.users_cash(new_user.username)
    assert total == db_cash, (
        f"Expected total to equal db cash value ({db_cash}); actual value: {total}"
        )
 




