import pytest
from random import choice

from pages.quote_page import QuotePage
from helpers import setup_page
from constants import CommonConstants as CC, QuoteConstants as QC, URLS


class TestQuotePageBasics():
    """
    Verify presence of required elements; their titles and placeholders
    """

    @pytest.fixture(autouse=True, scope="class")
    def quote_page(self, browser, new_user):
        return setup_page(QuotePage, browser, URLS.QUOTE_URL)


    def test_has_quote_input(self, quote_page):
        """Verify presence of Quote symbol input"""
        
        assert quote_page.quote_input() is not None, (
            "Expected Quote page to have stock symbol input field"
            )
        

    def test_quote_input_is_unique(self, quote_page):
        """Verify that Quote symbol input is one of a kind"""

        more_els = quote_page.more_quote_inputs()
        assert quote_page.is_unique(more_els), (
            f"Expected to find only one stock symbol input field on Quote page; found {len(more_els)}"
            )


    def test_quote_input_default_value(self, quote_page):
        """Verify Quote symbol input's default value"""

        quote_input_value = quote_page.get_value(quote_page.quote_input())
        assert quote_input_value == QC.EX_QUOTE_VALUE, (
            f"Expected Quote input to be {'empty' if QC.EX_QUOTE_VALUE == '' else QC.EX_QUOTE_VALUE}, " \
                f"actual value: {quote_input_value}"
                )
        

    def test_quote_input_placeholder(self, quote_page):
        """Verify Quote symbol input's placeholder value"""

        quote_input_ph = quote_page.get_placeholder(quote_page.quote_input())
        assert quote_input_ph == QC.EX_QUOTE_PH, (
            f"Expected Quote input placeholder text to be {QC.EX_QUOTE_PH}, actual value: {quote_input_ph}"
            )
        
        
    def test_has_quote_button(self, browser):
        """Verify presence of Quote button"""

        quote_page = QuotePage(browser, URLS.QUOTE_URL)
        quote_page.open()
        quote_button = quote_page.quote_button()
        assert quote_button is not None, (
            "Expected Quote page to have 'Quote' button"
            )


    def test_quote_input_is_unique(self, quote_page):
        """Verify that Quote button is one of a kind"""

        more_els = quote_page.more_quote_buttons()
        assert quote_page.is_unique(more_els), (
            f"Expected to find only one quote button on Quote page; found {len(more_els)}"
            )
        

@pytest.mark.parametrize("stock_symbol",
                         [(choice(CC.TEST_SYMBOLS)),
                          (choice(CC.TEST_SYMBOLS).lower())],
                         scope="class")
class TestValidQuote():
    """
    Test app behaviour in case of valid stock symbol input for Quote page
    """

    @pytest.fixture(autouse=True, scope="class")
    def quote_page(self, browser, new_user, stock_symbol):
        return setup_page(QuotePage, browser, URLS.QUOTE_URL)


    @pytest.fixture(autouse=True, scope="class")
    def get_stock_quote(self, quote_page, stock_symbol):
        """Query Quote page for stock info"""
        
        quote_page.get_stock_quote(stock_symbol)
        return quote_page.quote_result()


    def test_has_quote_result(self, get_stock_quote):
        """Verify requesting stock info returns a resulting string"""
        
        assert get_stock_quote is not None, (
            "Expected to see a text string with information about given stock; received no data or data in other form"
            )
        

    def test_has_company_name(self, get_stock_quote, new_user, stock_symbol):
        """Verify resulting string has company name in it"""
        
        # This test is for company name, but the variable is stock symbol!
        # It is like that because lookup() helper func from finance p-set currently uses stock symbol as company name
        # But if it changes someday this test would be failing
        assert get_stock_quote.text.find('(' + stock_symbol + ')'), (
            f"Expected to find the following company name in the result of a stock check: {'(' + stock_symbol + ')'}, " \
                f"actual text: {get_stock_quote.text()}"
                )
        

@pytest.mark.parametrize("stock_symbol, case",
                         CC.INVALID_SYMBOL_CASES,
                         scope="class")
class TestInvalidQuote():
    """
    Test app behaviour in case of invalid stock symbol input for Quote page
    """

    @pytest.fixture(autouse=True, scope="class")
    def quote_page(self, browser, new_user, stock_symbol, case):
        return setup_page(QuotePage, browser, URLS.QUOTE_URL)


    @pytest.fixture(autouse=True, scope="class")
    def get_stock_quote(self, quote_page, stock_symbol):
        """Query Quote page for stock info"""
        
        quote_page.get_stock_quote(stock_symbol)
        return quote_page.quote_result()
    

    def test_has_no_quote_result(self, get_stock_quote, case):
        """Verify requesting stock info gives no info for invalid input"""

        assert get_stock_quote is None, (
            f"Expected to receive no stock info in case of: {case}"
            )
        

    def test_error_image_appears(self, quote_page, case):
        """Verify presence of error image"""

        assert quote_page.get_error_image() is not None, (
            f"Expected for app to display an error image with funny cat in case if invalid input: {case}"
            )
        
        
    def test_correct_error_image_text(self, quote_page, case):
        """Verify error image's message text"""

        cases = {CC.INVALID_SYMBOL_CASES[0][1]: QC.EMPTY_STOCK_SYMBOL,
                 "default": QC.INVALID_STOCK_SYMBOL}
        ex_error = None
        error_text = quote_page.get_error_image_text()
        if case in cases:
            ex_error = cases[case]
        else:
            ex_error = cases["default"]
            
        assert error_text == ex_error, (
            f"Expected error image to have text {ex_error}, actual text: {error_text}")
