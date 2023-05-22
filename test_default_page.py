import pytest
from pages.default_page import DefaultPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from pages.urls import URLS

DT_HEADER_SYMBOL = "Symbol"
DT_HEADER_CNAME = "Name"
DT_HEADER_AMOUNT = "Shares"
DT_HEADER_PRICE = "Price"
DT_HEADER_TOTAL = "TOTAL"
EXPECTED_HEADERS = [DT_HEADER_SYMBOL, DT_HEADER_CNAME, DT_HEADER_AMOUNT, DT_HEADER_PRICE, DT_HEADER_TOTAL]

# Just one test for the unauthorized user:
def test_unauthorized_user_gets_redirected_to_login_page(browser):
    dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
    dft_page.open()
    assert dft_page.url_should_change_to(URLS.LOGIN_URL) , (
        f"Expected to be redirected to /login page; actual url: {dft_page.browser.current_url}")
    
@pytest.mark.usefixtures("new_user")
class TestDefaultPageBasicsAuthed():
    def test_has_stock_table(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock_table = dft_page.stocktable()
        assert stock_table is not None, "Expected for logged in user to see a table of purchased stocks"

    def test_stocktable_has_correct_header_amount_and_names(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        table_headers = dft_page.stocktable_headers()
        assert table_headers is not None, "Expected for logged in user to see stock table headers"
        header_names = dft_page.headers_names()
        number_of_headers = len(table_headers)
        ex_number_of_headers = len(EXPECTED_HEADERS)
        assert number_of_headers == ex_number_of_headers, (
            f"Expected the stock table to have {ex_number_of_headers} headers: {EXPECTED_HEADERS}; actual number of headers: {number_of_headers}")
        for header, ex_header in zip(header_names, EXPECTED_HEADERS):
            assert header == ex_header, f"Expected  table header {header} to have a name {ex_header}"

    def test_has_cash_info(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.cash_element()
        assert cash is not None, "Expected for logged in user to see an element containing current Cash amount"

    def test_has_total_info(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.total_element()
        assert total is not None, "Expected for logged in user to see an element containing TOTAL amount of money"

@pytest.mark.usefixtures("new_user")
class TestDefaultPageTable():
    def test_new_user_table_has_no_data(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock_rows = dft_page.stocktable_rows()
        assert stock_rows is None, "Expected stock table to have no rows of purchased stocks for newly registered user"

    def test_new_user_has_10k_cash(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.cash_elm_value()
        assert cash == dft_page.INITIAL_CASH, f"Expected total value to be {dft_page.INITIAL_CASH}, actual value: {cash} for newly registered user"

    def test_new_user_has_10k_total(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.total_elm_value()
        assert total == dft_page.INITIAL_CASH, f"Expected TOTAL value to be {dft_page.INITIAL_CASH}, actual value: {total} for newly registered user"

    @pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
    def test_table_has_no_data_if_purchased_and_sold(self, browser, stock_symbols, stock_amounts):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
        sell_page = SellPage(browser, URLS.SELL_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            sell_page.open()
            sell_page.sell_stock(symbol, amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock_rows = dft_page.stocktable_rows()
        assert stock_rows is None, (
            "Expected stock table to have no rows of data if user sold all their stocks")

    #TODO: add more parameters
    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12),
                                                            ("AAPL", 7),
                                                            ("MSFT", 4)])
    def test_cash_decreases_after_purchasing(self, browser, stock_symbol, stock_amount):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.cash_elm_value()
        table_cells = dft_page.stocktable_cells()
        cash_spent = table_cells[DT_HEADER_PRICE] * table_cells[DT_HEADER_AMOUNT]
        assert cash == round(dft_page.INITIAL_CASH - cash_spent, 2), (
            f"Expected cash to equal initial cash - stock price ({dft_page.INITIAL_CASH - cash_spent}); actual value: {cash}")

    #TODO: add more parameters
    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12),
                                                            ("AAPL", 7),
                                                            ("MSFT", 4)])
    def test_cash_increases_after_selling(self, browser, stock_symbol, stock_amount):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash_after_buying = dft_page.cash_elm_value()
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        cash_earned = sell_page.lookup(stock_symbol)['price'] * stock_amount
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.cash_elm_value()
        assert cash == cash_after_buying + cash_earned, (
            f"Expected Default page table cash value ({cash}) to equal: {cash_after_buying + cash_earned}")

    @pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
    def test_total_equals_cash_and_stock(self, stock_symbols, stock_amounts, browser):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total_after_buying = dft_page.total_elm_value()
        cash_after_buying = dft_page.cash_elm_value()
        table_rows = dft_page.stocktable_cells()
        stock_overall_price = 0
        for row in table_rows:
            stock_overall_price += row[DT_HEADER_PRICE] * row[DT_HEADER_AMOUNT]
        assert total_after_buying == cash_after_buying + stock_overall_price, (
            f"Expected total to equal the sum of leftover cash + stock ({cash_after_buying + stock_overall_price}); actual value: {total}")       
        sell_page = SellPage(browser, URLS.SELL_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            sell_page.open()
            sell_page.sell_stock(symbol, amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.total_elm_value()
        cash = dft_page.cash_elm_value()
        assert total == cash, f"Expected total to equal cash earned from selling stocks, which equals {cash}; actual value: {total}" 

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12),
                                                            ("AAPL", 7),
                                                            ("MSFT", 4)])
    def test_stock_total_should_equal_amount_x_price(self, stock_symbol, stock_amount, browser):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock = dft_page.stocktable_cells()
        amount_x_price = round(stock[DT_HEADER_PRICE] * stock[DT_HEADER_AMOUNT], 2)
        assert amount_x_price == stock[DT_HEADER_TOTAL], (
            f"Expected stock's {stock[DT_HEADER_SYMBOL]} total amount to equal {amount_x_price}, actual value: {stock[DT_HEADER_TOTAL]}")


