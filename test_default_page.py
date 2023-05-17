import pytest
from pages.default_page import DefaultPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from pages.urls import URLS

OLD_USER = "swordy1"
OLD_PASSWORD = "123"
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
        stock_table = dft_page.get_stocktable()
        assert stock_table is not None, "Expected for logged in user to see a table of purchased stocks"

    def test_stocktable_has_correct_headers(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        table_headers = dft_page.get_stocktable_headers()
        assert table_headers is not None, "Expected for logged in user to see stock table headers"
        table_headers = [header.text for header in table_headers]
        assert len(table_headers) == len(EXPECTED_HEADERS), (
            f"Expected the stock table to have {len(EXPECTED_HEADERS)} columns {EXPECTED_HEADERS}; actual number of columns: {len(table_headers)}")
        for theader, ex_header in zip(table_headers, EXPECTED_HEADERS):
            assert theader == ex_header, f"Expected  table header {theader} to have a name {ex_header}"

    def test_stocktable_has_cash_cell(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.get_cash_cell()
        assert cash is not None, "Expected for logged in user to see an element containing current Cash amount"

    def test_stocktable_has_total_cell(self, browser):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.get_total_cell()
        assert total is not None, "Expected for logged in user to see an element containing TOTAL amount of money"

class TestDefaultPageTable():
    def test_new_user_table_has_no_data(self, browser, new_user):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock_rows = dft_page.get_stocktable_rows()
        assert stock_rows is None, "Expected stock table to have no rows of purchased stocks for newly registered user"

    def test_new_user_has_10k_cash(self, browser, new_user):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.get_cash_value()
        assert cash == dft_page.INITIAL_CASH, f"Expected total value to be 10,000.00, actual value: {cash} for newly registered user"

    def test_new_user_has_10k_total(self, browser, new_user):
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.get_total_value()
        assert total == dft_page.INITIAL_CASH, f"Expected TOTAL value to be 10,000.00, actual value: {total} for newly registered user"

    @pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
    def test_table_has_no_data_if_purchased_and_sold(self, browser, stock_symbols, stock_amounts, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
            buy_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], symbol, buy_page.lookup(symbol)['price'], amount)
        sell_page = SellPage(browser, URLS.SELL_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            sell_page.open()
            sell_page.sell_stock(symbol, amount)
            buy_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], symbol, buy_page.lookup(symbol)['price'], amount * (-1))
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock_rows = dft_page.get_stocktable_rows()
        assert stock_rows is None, (
            "Expected stock table to have no rows of data if user sold all posessed stocks")
        posessed_stocks = dft_page.query(database, 
                                  """
                                  select stockname from purchases p join users u on p.user_id = u.id 
                                  where u.username=? group by p.stockname having sum(p.amount) > 0;
                                  """,
                                  new_user['username'])
        assert posessed_stocks is None, (
            "Expected the sum of user's stocks in database to equal to zero after selling everything")

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12)])
    def test_cash_decreases_after_purchasing(self, new_user, browser, database, stock_symbol, stock_amount):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert the purchase into mock database
        buy_page.query(database, 
                    """
                    insert into purchases (user_id, stockname, price, amount) 
                    values ((select id from users where username = ?), ?, ?, ? )
                    """, 
                    new_user['username'], stock_symbol, buy_page.lookup(stock_symbol)['price'], stock_amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.get_cash_value()
        table_cells = dft_page.get_stocktable_cells()
        cash_spent = table_cells[DT_HEADER_PRICE] * table_cells[DT_HEADER_AMOUNT]
        assert cash == dft_page.INITIAL_CASH - cash_spent, (
            f"Expected cash to equal initial cash ({dft_page.INITIAL_CASH}) - stock price ({cash_spent}); actual value: {cash}")
        db_cash = dft_page.query(database, "select cash from users where username = ?;", new_user['username'])
        assert cash == db_cash['cash'], f"Expected total cash to equal {db_cash['cash']}, actual amount: {cash}" 

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12)])
    def test_cash_increases_after_selling(self, new_user, browser, database, stock_symbol, stock_amount):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        buy_page.query(database, 
                    """
                    insert into purchases (user_id, stockname, price, amount) 
                    values ((select id from users where username = ?), ?, ?, ? )
                    """, 
                    new_user['username'], stock_symbol, buy_page.lookup(stock_symbol)['price'], stock_amount)
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        sell_page.query(database, 
                    """
                    insert into purchases (user_id, stockname, price, amount) 
                    values ((select id from users where username = ?), ?, ?, ? )
                    """, 
                    new_user['username'], stock_symbol, buy_page.lookup(stock_symbol)['price'], stock_amount * (-1))
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        cash = dft_page.get_cash_value()
        db_cash = dft_page.query(database, "select cash from users where username = ?", new_user['username'])
        assert cash == db_cash['cash'], (
            f"Expected Default page table cash value ({cash}) to equal database cash value ({db_cash})")

    @pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [12, 6])])
    def test_total_equals_cash_and_stock(self, new_user, stock_symbols, stock_amounts, browser, database):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
            buy_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], symbol, buy_page.lookup(symbol)['price'], amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.get_total_value()
        cash = dft_page.get_cash_value()
        table_rows = dft_page.get_stocktable_cells()
        for row in table_rows:
            cash += row[DT_HEADER_PRICE] * row[DT_HEADER_AMOUNT]
        assert total == cash, (
            f"Expected total to equal the sum of leftover cash + stock cost, which equals {cash}; actual value: {total}")       
        sell_page = SellPage(browser, URLS.SELL_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            sell_page.open()
            sell_page.sell_stock(symbol, amount)
            sell_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], symbol, buy_page.lookup(symbol)['price'], amount * (-1))
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        total = dft_page.get_total_value()
        cash = dft_page.get_cash_value()
        stock_profit = dft_page.query(database, 
                                      f"""
                                      select sum(amount)*sum(price) as stock_profit from purchases 
                                      where user_id in (Select id from users where username=?);
                                      """, 
                                      new_user['username'])
        cash = dft_page.query(database, "select cash from users where username = ?;", OLD_USER)
        dbtotal = cash['cash'] + stock_profit['stock_profit']
        assert total == dbtotal, f"Expected total to equal leftover cash + stock selling profits, which equals {dbtotal}; actual value: {total}" 

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 12)])
    def test_stock_total_should_equal_amount_x_price(self, new_user, stock_symbol, stock_amount, browser, database):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        buy_page.query(database, 
                    """
                    insert into purchases (user_id, stockname, price, amount) 
                    values ((select id from users where username = ?), ?, ?, ? )
                    """, 
                    new_user['username'], stock_symbol, buy_page.lookup(stock_symbol)['price'], stock_amount)
        dft_page = DefaultPage(browser, URLS.DEFAULT_URL)
        dft_page.open()
        stock = dft_page.get_stocktable_cells()
        amount_x_price = round(stock[DT_HEADER_PRICE] * stock[DT_HEADER_AMOUNT], 2)
        # print(f"\nPrice is {stock[DT_HEADER_PRICE]}; Amount is {stock[DT_HEADER_AMOUNT]}; Multiplied is {amount_x_price}; Table value is {stock[DT_HEADER_TOTAL]}")
        assert amount_x_price == stock[DT_HEADER_TOTAL], (
            f"Expected stock's {stock[DT_HEADER_SYMBOL]} total amount to equal {amount_x_price}, actual value: {stock[DT_HEADER_TOTAL]}")
