import pytest

from pages.history_page import HistoryPage
from pages.buy_page import BuyPage
from pages.sell_page import SellPage
from pages.urls import URLS

HT_HEADER_SYMBOL = "Symbol"
HT_HEADER_AMOUNT = "Shares"
HT_HEADER_PRICE = "Price"
HT_HEADER_DATETIME = "Transacted"
EXPECTED_HEADERS = [HT_HEADER_SYMBOL, HT_HEADER_AMOUNT, HT_HEADER_PRICE, HT_HEADER_DATETIME]

@pytest.mark.usefixtures("new_user")
class TestHistoryBasics():
    def test_has_history_table(self, browser):
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        hist_table = hist_page.history_table()
        assert hist_table is not None, (
            "Expected the History page to have history table; couldn't find it")

    def test_history_table_has_headers(self, browser):
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        headers = hist_page.history_table_headers()
        assert headers is not None, "Expected the History table to have headers"
        assert len(headers) == len(EXPECTED_HEADERS), (
            f"""
            Expected for the History table to have {len(EXPECTED_HEADERS)} headers; 
            actual number of headers: {len(headers)}
            """)
        headers = [header.text for header in headers]
        assert headers == EXPECTED_HEADERS, (
            f"Expected History table to have {EXPECTED_HEADERS} header names; actual list of header names: {headers}")


@pytest.mark.usefixtures("new_user")
class TestHistoryTransactions():
    def test_history_table_empty_if_no_purchases(self, browser):
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        table_rows = hist_page.history_rows()
        assert table_rows is None, (
            "Expected to find no rows in History table if no purchases were made")

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 1)])
    def test_history_table_shows_record_of_buying(self, browser, stock_symbol, stock_amount, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert the purchase into mock database
        buy_page.query(database, 
                       """
                       insert into purchases (user_id, stockname, price, amount) 
                       values ((select id from users where username = ?), ?, ?, ? )
                       """, 
                       new_user['username'], stock_symbol, 100.0, stock_amount)
        # Query database for the new purchase transaction
        buy_db_record = buy_page.query(database, 
                                       f"""
                                       Select stockname as {HT_HEADER_SYMBOL}, amount as {HT_HEADER_AMOUNT}, 
                                       price as {HT_HEADER_PRICE}, Timestamp as {HT_HEADER_DATETIME} 
                                       from purchases p join users u on u.id = p.user_id 
                                       where u.username = ? order by {HT_HEADER_DATETIME} desc limit 1
                                       """, 
                                       new_user['username'])
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        hist_td = hist_page.history_table_data()
        #print(strptime(hist_td['Transacted'], "%Y-%m-%d %H:%M:%S"))
        for key in buy_db_record:
            #TODO: get rid of key conditionals, price and date will be available in real db
            if key == HT_HEADER_SYMBOL or key == HT_HEADER_AMOUNT:
                assert buy_db_record[key] == hist_td[key], (
                f"Expected for database data and History page table row data to be the same; actual values for {key}: {buy_db_record[key]} in database and {hist_td[key]} in History table")

    @pytest.mark.parametrize("stock_symbols, stock_amounts", [(["NFLX", "AAPL"], [1, 2])])
    def test_history_table_shows_multiple_records_of_buying(self, browser, stock_symbols, stock_amounts, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        for symbol, amount in zip(stock_symbols, stock_amounts):
            buy_page.open()
            buy_page.buy_stock(symbol, amount)
            # Insert the purchase into mock database
            buy_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], symbol, 100.0, amount)
        # Query database for the new purchase transaction
        buy_db_record = buy_page.query(database, 
                                       f"""
                                       Select stockname as {HT_HEADER_SYMBOL}, amount as {HT_HEADER_AMOUNT}, 
                                       price as {HT_HEADER_PRICE}, Timestamp as {HT_HEADER_DATETIME} 
                                       from purchases p join users u on u.id = p.user_id 
                                       where u.username = ? order by {HT_HEADER_DATETIME} asc
                                       """, 
                                       new_user['username'])
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        hist_td = hist_page.history_table_data()
        #print(strptime(hist_td['Transacted'], "%Y-%m-%d %H:%M:%S"))
        print(zip(buy_db_record, hist_td))
        for table_row, db_row in zip(buy_db_record, hist_td):
            for tkey, dkey in zip(table_row, db_row):
                #TODO: get rid of key conditionals, price and date will be available in real db
                if tkey == HT_HEADER_SYMBOL or tkey == HT_HEADER_AMOUNT:
                    assert table_row[tkey] == db_row[dkey], (
                    f"Expected for database data and History page table row data to be the same; actual values for {tkey}: {db_row[dkey]} in database and {table_row[tkey]} in History table")

    @pytest.mark.parametrize("stock_symbol, stock_amount", [("NFLX", 1)])
    def test_history_table_shows_record_of_selling(self, browser, stock_symbol, stock_amount, database, new_user):
        buy_page = BuyPage(browser, URLS.BUY_URL)
        buy_page.open()
        buy_page.buy_stock(stock_symbol, stock_amount)
        # Insert the purchase into mock database
        buy_page.query(database, 
                       """
                       insert into purchases (user_id, stockname, price, amount) 
                       values ((select id from users where username = ?), ?, ?, ? )
                       """, 
                       new_user['username'], stock_symbol, 100.0, stock_amount)
        sell_page = SellPage(browser, URLS.SELL_URL)
        sell_page.open()
        sell_page.sell_stock(stock_symbol, stock_amount)
        # Insert the selling into mock database
        sell_page.query(database, 
                        """
                        insert into purchases (user_id, stockname, price, amount) 
                        values ((select id from users where username = ?), ?, ?, ? )
                        """, 
                        new_user['username'], stock_symbol, 100.0, stock_amount * (-1))
        # Query database for the new purchase transaction
        sell_db_record = sell_page.query(database, 
                                         f"""
                                         Select stockname as {HT_HEADER_SYMBOL}, amount as {HT_HEADER_AMOUNT}, 
                                         price as {HT_HEADER_PRICE}, Timestamp as {HT_HEADER_DATETIME} 
                                         from purchases p join users u on u.id = p.user_id 
                                         where u.username = ? order by {HT_HEADER_DATETIME} desc limit 1
                                         """, 
                                         new_user['username'])
        hist_page = HistoryPage(browser, URLS.HISTORY_URL)
        hist_page.open()
        hist_td = hist_page.history_table_data()[-1]
        #print(strptime(hist_td['Transacted'], "%Y-%m-%d %H:%M:%S"))
        for key in sell_db_record:
            #TODO: get rid of key conditionals, price and date will be available in real db
            if key == HT_HEADER_SYMBOL or key == HT_HEADER_AMOUNT:
                assert sell_db_record[key] == hist_td[key], (
                f"Expected for database data and History page table row data to be the same; actual values for {key}: {sell_db_record[key]} in database and {hist_td[key]} in History table")