import pytest
import pyperclip

from pages.quote_page import QuotePage
from pages.urls import URLS

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

STOCK_SYMBOL_EMPTY = "MISSING SYMBOL"
STOCK_SYMBOL_INVALID = "INVALID SYMBOL"

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
class TestStockAPICalls():
    @pytest.mark.parametrize("stock_symbol, company_name", [("AAPL", "Apple Inc"),
                                                            ("MsFT", "Microsoft Corporation"),
                                                            ("mcd", "McDonald`s Corp")])
    def test_valid_stock_symbol(self, browser, stock_symbol, company_name):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_page.fill_quote_field(stock_symbol)
        quote_page.press_quote_button()
        quote_result = quote_page.quote_result()
        assert quote_result is not None, "Expected Quote page to provide info on referred stock symbol"
        assert quote_result.text.find(company_name), (
            f"Expected to find the following company name in the result of a stock check: {company_name}, actual text: {quote_result.text()}")
        
    @pytest.mark.parametrize("stock_symbol, case", [("", "Empty field"),
                                                    (" ", "One space"),
                                                    ("    ", "Multiple spaces"),
                                                    ("123", "Numbers only"),
                                                    ("$@%?", "Special characters only"),
                                                    ("zyzx", "Non-existent stock symbol (only letters)"),
                                                    ("A23#", "Non-existent stock symbol (combination)"),
                                                    ("тест", "Other alphabets #1"),
                                                    ("片仮名", "Other alphabets #2")
                                                    ])
    def test_invalid_stock_symbol(self, browser, stock_symbol, case):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_page.fill_quote_field(stock_symbol)
        quote_page.press_quote_button()
        quote_result = quote_page.quote_result()
        assert quote_result is None, f"Expected to receive no info in case of: {case}"
        error_image = quote_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: {case}")
        error_text = quote_page.get_error_text(error_image)
        if case == "Empty field":
            assert error_text == STOCK_SYMBOL_EMPTY, (
                f"Expected error image to have text {STOCK_SYMBOL_EMPTY}, actual text: {error_text}")
        else:
            assert error_text == STOCK_SYMBOL_INVALID, (
                f"Expected error image to have text {STOCK_SYMBOL_INVALID}, actual text: {error_text}")

    def test_emoji_stock_symbol(self, browser):
        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_field = quote_page.quote_input()
        # Had to use this javascript workaround to be able to type emojis in chrome.
        # https://stackoverflow.com/questions/59138825/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        text = "😍😍😍"
        browser.execute_script(JS_ADD_TEXT_TO_INPUT, quote_field, text)
        quote_page.press_quote_button()
        quote_result = quote_page.quote_result()
        assert quote_result is None, f"Expected to receive no info in case of: Emoji stock symbol"
        error_image = quote_page.get_error_image()
        assert error_image is not None, (
            f"Expected for application to display an error image with funny cat in case if incorrect input: Emoji stock symbol")
        error_text = quote_page.get_error_text(error_image)
        assert error_text == STOCK_SYMBOL_INVALID, (
            f"Expected error image to have text {STOCK_SYMBOL_INVALID}, actual text: {error_text}")
