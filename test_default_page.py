import time
import pytest
from pytest import approx
from pages.default_page import DefaultPage
from pages.login_page import LoginPage
from pages.urls import URLS

EX_NUMBER_OF_COLUMNS = 5
EXPECTED_HEADERS = ["Symbol", "Name", "Shares", "Price", "TOTAL"]
NEW_USER = "swordy2"
NEW_PASSWORD = "123"
OLD_USER = "swordy1"
OLD_PASSWORD = "123"

@pytest.fixture()
def default_page(browser):
    default_page = DefaultPage(browser, URLS.DEFAULT_URL)
    default_page.open()
    return default_page

# Just one test for the unauthorized user:
def test_unauthorized_user_gets_redirected_to_login_page(default_page):
    assert default_page.url_should_change_to(URLS.LOGIN_URL) , (
        f"Expected to be redirected to /login page; actual url: {default_page.browser.current_url}")
    
###################
# Basic page structure tests for the logged in user:
###################
@pytest.mark.usefixtures("login")
class TestDefaultPageBasicsAuthed():
    def test_has_stock_table(self, default_page):
        stock_table = default_page.get_stocktable()
        assert stock_table is not None, "Expected for logged in user to see a table of purchased stocks"

    def test_stocktable_has_right_headers(self, default_page):
        table_headers = default_page.get_stocktable_headers()
        assert table_headers is not None, "Expected for logged in user to see stock table headers"
        number_of_columns = len(table_headers)
        table_headers = [header.text for header in table_headers]
        assert number_of_columns == EX_NUMBER_OF_COLUMNS, (
            f"Expected the stock table to have {EX_NUMBER_OF_COLUMNS} columns {EXPECTED_HEADERS}; actual number of columns: {number_of_columns}")
        for i in range(number_of_columns):
            assert table_headers[i] == EXPECTED_HEADERS[i], f"Expected  table header {table_headers[i]} to have a name {EXPECTED_HEADERS[i]}"

    def test_stocktable_has_cash_cell(self, default_page):
        cash = default_page.get_cash_cell()
        assert cash is not None, "Expected for logged in user to see an element containing current Cash amount"

    def test_stocktable_has_total_cell(self, default_page):
        total = default_page.get_total_cell()
        assert total is not None, "Expected for logged in user to see an element containing TOTAL amount of money"

#############
# Table tests
#############
class TestDefaultPageTable():
    def test_table_has_no_data_if_no_purchases(self, browser, new_user):
        default_page = DefaultPage(browser, URLS.DEFAULT_URL)
        default_page.open()
        stock_rows = default_page.get_stocktable_rows()
        assert stock_rows is None, "Expected stock table to have no rows of purchased stocks"

    def test_user_has_10k_cash_if_no_purchases(self, browser, new_user):
        default_page = DefaultPage(browser, URLS.DEFAULT_URL)
        default_page.open()
        cash = default_page.get_cash_value()
        assert cash == default_page.INITIAL_CASH, f"Expected total value to be 10,000.00, actual value: {cash}"

    def test_user_has_10k_total_if_no_purchases(self, browser, new_user):
        default_page = DefaultPage(browser, URLS.DEFAULT_URL)
        default_page.open()
        total = default_page.get_total_value()
        assert total == default_page.INITIAL_CASH, f"Expected total value to be 10,000.00, actual value: {total}"

    @pytest.mark.un(OLD_USER)
    @pytest.mark.pw(OLD_PASSWORD)
    def test_table_has_no_data_if_purchased_and_sold(self, login, default_page):
        #todo: replace with account registration, buying and selling stocks
        stock_rows = default_page.get_stocktable_rows()
        assert stock_rows is None, "Expected stock table to have no rows of purchased stocks" 

    @pytest.mark.un(OLD_USER)
    @pytest.mark.pw(OLD_PASSWORD)
    #can be decomposed into: cash is cash - purchases; cash is cash + sells;
    def test_cash_amounts_to_cash_and_sell_cost_if_bought_and_sold(self, login, default_page, database):
        #todo: replace with account registration, buying and selling stocks
        cash = default_page.get_cash_value()
        results = default_page.query(database, "select cash from users where username = ?;", OLD_USER)
        assert cash == results['cash'], f"Expected total cash to equal {results['cash']}, actual amount: {cash}" 

    @pytest.mark.un(OLD_USER)
    @pytest.mark.pw(OLD_PASSWORD)
    #can be decomposed into: total is cash + stock cost; total is cash + sells;
    def test_total_amounts_to_cash_and_purchases_cost_if_bought_and_sold(self, login, default_page, database):
        #todo: replace with account registration, buying and selling stocks
        total = default_page.get_total_value()
        cash = default_page.query(database, "select cash from users where username = ?;", OLD_USER)
        stocks = default_page.query(database, "select sum(amount)*sum(price) as stock_profit from purchases where user_id in (Select id from users where username=?);", OLD_USER)
        dbtotal = cash['cash'] + stocks['stock_profit']
        assert total == dbtotal, f"Expected total cash to equal {dbtotal}, actual amount: {total}" 

    def test_stock_total_should_equal_amount_x_price(self, login, default_page):
        #replace with registering new user and bying four stocks
        stock_info = default_page.get_stocktable_cells()
        for stock in stock_info:
            amount_x_price = round(stock["Price"] * stock["Shares"], 2)
            print(f"\nPrice is {stock['Price']}; Amount is {stock['Shares']}; Multiplied is {amount_x_price}; Table value is {stock['TOTAL']}")
            assert amount_x_price == stock["TOTAL"], (
                f"Expected stock's {stock['Symbol']} total amount to equal {amount_x_price}, actual value: {stock['TOTAL']}")
