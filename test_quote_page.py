import pytest
import pyperclip

from pages.quote_page import QuotePage
from pages.urls import URLS

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

EMPTY_STOCK_SYMBOL = "MISSING SYMBOL"
INVALID_STOCK_SYMBOL = "INVALID SYMBOL"

@pytest.mark.usefixtures("login")
class TestQuotePageBasics():
    def test_has_quote_input(self, browser):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_input = quote_page.quote_input()
        assert quote_input is not None, "Expected Quote page to have 'Symbol' input field"

    def test_has_quote_button(self, browser):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_button = quote_page.quote_button()
        assert quote_button is not None, "Expected Quote page to have 'Quote' button"

@pytest.mark.usefixtures("login")
class TestStockInfoRequests():
    @pytest.mark.parametrize("stock_symbol, company_name", [("AAPL", "Apple Inc"),
                                                            ("MsFT", "Microsoft Corporation"),
                                                            ("mcd", "McDonald`s Corp")])
    def test_valid_stock_symbol(self, browser, stock_symbol, company_name):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_page.fill_quote_input(stock_symbol)
        quote_page.press_quote_button()
        quote_result = quote_page.quote_result()
        assert quote_result is not None, "Expected Quote page to provide info on referred stock symbol"
        assert quote_result.text.find(company_name), (
            f"Expected to find the following company name in the result of a stock check: {company_name}, actual text: {quote_result.text()}")
        
    @pytest.mark.parametrize("stock_symbol, case", [("", "Empty stock symbol"),
                                                    (" ", "White-space stock symbol (one)"),
                                                    ("   ", "White-space stock symbol (few)"),
                                                    ("123", "Numbers only stock symbol"),
                                                    ("0", "Zero stock symbol"),
                                                    ("255.5", "Floating point number stock symbol"),
                                                    ("128,0", "Floating point number (comma) stock symbol"),
                                                    ("06.05.2023", "Date stock symbol"),
                                                    ("NULL", "NULL symbol"),
                                                    ("$@%?", "Special characters only stock symbol"),
                                                    ("zyzx", "Non-existent stock symbol (only letters)"),
                                                    ("$A23", "Non-existent stock symbol (combination)"),
                                                    ("тест", "Other alphabets stock symbol #1"),
                                                    ("片仮名", "Other alphabets stock symbol #2"),
                                                    ("😍😍😍", "Emoji stock symbol")
                                                    ])
    def test_invalid_stock_symbol(self, browser, stock_symbol, case):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_page.fill_input(quote_page.quote_input(), stock_symbol)
        quote_page.press_quote_button()
        quote_result = quote_page.quote_result()
        assert quote_result is None, f"Expected to receive no info in case of: {case}"
        error_image = quote_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: {case}")
        error_text = quote_page.get_error_text(error_image)
        if case == "Empty field":
            assert error_text == EMPTY_STOCK_SYMBOL, (
                f"Expected error image to have text {EMPTY_STOCK_SYMBOL}, actual text: {error_text}")
        else:
            assert error_text == INVALID_STOCK_SYMBOL, (
                f"Expected error image to have text {INVALID_STOCK_SYMBOL}, actual text: {error_text}")
