import os
import re
import emoji
import requests
from urllib.parse import urlparse, quote_plus, unquote

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators


class BasePage():
    def __init__(self, browser, url, timeout=4):
        self.browser = browser
        self.url = url
        self.timeout = timeout
        self.INITIAL_CASH = 10000.00
        self.API_KEY = "pk_4e5ad72f580a4034a65dc765141d6d0a"
    
    def retrieve_element_if_present(self, how, what):
        try:
            element = WebDriverWait(self.browser, self.timeout).until(lambda el: el.find_element(how, what))
        except TimeoutException:
            return None
        return element
    
    def retrieve_multiple_elements_if_present(self, how, what):
        try:
            list_of_elements = WebDriverWait(self.browser, self.timeout).until(lambda el: el.find_elements(how, what))
        except TimeoutException:
            return None
        return list_of_elements
    
    def open(self):
        self.browser.get(self.url)

    def go_to_other_page(self, new_url):
        self.browser.get(new_url)

    def get_page_title(self):
        return self.browser.title
    
    def get_current_url(self):
        return self.browser.current_url

    def url_should_change_to(self, new_url):
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.url_to_be(new_url))
        except TimeoutException:
            return False
        return True
    
    def get_logout_link(self):
        logout_link = self.retrieve_element_if_present(*BasePageLocators.LOGOUT_LINK)
        return logout_link

    def get_register_link(self):
        register_link = self.retrieve_element_if_present(*BasePageLocators.REGISTER_LINK)
        return register_link

    def get_login_link(self):
        login_link = self.retrieve_element_if_present(*BasePageLocators.LOGIN_LINK)
        return login_link
    
    def get_success_alert(self):
        success_alert = self.retrieve_element_if_present(*BasePageLocators.ALERT_MESSAGE)
        return success_alert
    
    def get_browser_alert(self):
        try:
            alert = WebDriverWait(self.browser, self.timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        return alert
    
    def get_error_image(self):
        error_image = self.retrieve_element_if_present(*BasePageLocators.ERROR_IMAGE)
        return error_image

    def get_error_image_text(self):
        error_image = self.get_error_image()
        if error_image is None:
            return None
        link = error_image.get_attribute("src")
        parsed_url = urlparse(link).path
        fullname = os.path.split(parsed_url)[1]
        fullname = unquote(fullname)
        name = re.sub(r'(.jpg)$', "" , fullname)
        name = re.sub(r'-', " " , name)
        def reverse_escape(s):
            """
            Escape special characters. But in reverse!!!
            https://github.com/jacebrowning/memegen#special-characters
            """
            for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                s = s.replace(new, old)
            return s
        name = reverse_escape(name)
        name = name.upper()
        return name

    def should_have_default_link(self):
        default_link = self.retrieve_element_if_present(*BasePageLocators.DEFAULT_LINK)
        assert default_link is not None, "Couldn't find link to the default page (the clickable CS50 logo)"
    
    def should_have_cs50_logo(self):
        cs50_logo_parts = self.retrieve_multiple_elements_if_present(*BasePageLocators.CS50_LOGO_PART)
        logo_text = ""
        for each_span_element in cs50_logo_parts:
            logo_text += each_span_element.text
        assert logo_text == "C$50Finance", (
            "Page Logo in the navigation bar (concatenation of spans inside the default page link) doesnt spell 'C$50Finance'")

    def get_quote_navitem(self):
        quote = self.retrieve_element_if_present(*BasePageLocators.QUOTE_LINK)
        return quote

    def get_buy_navitem(self):
        buy = self.retrieve_element_if_present(*BasePageLocators.BUY_LINK)
        return buy

    def get_sell_navitem(self):
        sell = self.retrieve_element_if_present(*BasePageLocators.SELL_LINK)
        return sell
    
    def get_hist_navitem(self):
        hist = self.retrieve_element_if_present(*BasePageLocators.HISTORY_LINK)
        return hist
    
    def fill_input(self, input, text):
        text = str(text)
        if self.contains_emoji(text):
            # Had to use this javascript workaround to be able to type emojis in chrome.
            # https://stackoverflow.com/questions/59138825/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with
            JS_ADD_TEXT_TO_INPUT = """
            var elm = arguments[0], txt = arguments[1];
            elm.value += txt;
            elm.dispatchEvent(new Event('change'));
            """
            self.browser.execute_script(JS_ADD_TEXT_TO_INPUT, input, text)
        else:
            input.send_keys(text)
    
    def hack_amount_input(self, amount_input):
        hack_script = """
        var elm = arguments[0]
        if(elm.hasAttribute("min"))
        {
            elm.removeAttribute("min")
        }
        if(elm.hasAttribute("type"))
        {
            elm.setAttribute("type","text") 
        }          
        """
        self.browser.execute_script(hack_script, amount_input)

    def should_have_nav_items(self):
        errors = []
        if self.get_quote_navitem() is None:
            errors.append("Couldn't find 'Quote' navigation item")
        if self.get_buy_navitem() is None:
            errors.append("Couldn't find 'Buy' navigation item")
        if self.get_sell_navitem() is None:
            errors.append("Couldn't find 'Sell' navigation item")
        if self.get_hist_navitem() is None:
            errors.append("Couldn't find 'History' navigation item")
        assert not errors, "; ".join(errors)

    def should_not_have_nav_items(self):
        errors = []
        if self.get_quote_navitem() is not None:
            errors.append("Expected navigation menu to not have 'Quote' navigation item")
        if self.get_buy_navitem() is not None:
            errors.append("Expected navigation menu to not have 'Buy' navigation item")
        if self.get_sell_navitem() is not None:
            errors.append("Expected navigation menu to not have 'Sell' navigation item")
        if self.get_hist_navitem() is not None:
            errors.append("Expected navigation menu to not have 'History' navigation item")
        assert not errors, "; ".join(errors)

    def organize_cell_data(self, all_cell_elements, all_header_elements):
        cell_inner_text = [cell.text for cell in all_cell_elements]
        header_names = [header.text for header in all_header_elements]
        list_of_rows = []
        if len(cell_inner_text) % len(header_names) == 0:
            rows_amount = int(len(cell_inner_text)/len(header_names))
            for every_row in range(rows_amount):
                new_row = dict.fromkeys(header_names)
                for key in new_row:
                    new_row[key] = cell_inner_text.pop(0)
                    if self.check_if_integer(new_row[key]):
                        new_row[key] = int(new_row[key])
                    elif self.check_if_currency(new_row[key]):
                        new_row[key] = self.convert_currency_to_number(new_row[key])
                list_of_rows.append(new_row)
            if len(list_of_rows) == 1:
                return list_of_rows[0]
            else:
                return list_of_rows
        return None

    #Taking this directly from Finance p-set
    def lookup(self, symbol):
        """Look up quote for symbol."""
        # Contact API
        try:
            url = f"https://cloud.iexapis.com/stable/stock/{quote_plus(symbol)}/quote?token={self.API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            return None
        # Parse response
        try:
            quote = response.json()
            return {
                "name": quote["companyName"],
                "price": float(quote["latestPrice"]),
                "symbol": quote["symbol"]
            }
        except (KeyError, TypeError, ValueError):
            return None
    #
    # Helper functions
    #
    @staticmethod
    def check_if_currency(currency):
        if re.fullmatch(r"^\$(\d{0,3}[,])*(\d{0,3}[.]){1}\d+", currency):
            return True
        return False
    
    @staticmethod
    def check_if_integer(number):
        if re.fullmatch(r"^\-{0,1}\d*", number):
            return True
        return False

    @staticmethod
    def check_if_float(number):
        if re.fullmatch(r"^\-{0,1}\d*[,.]{1}\d*", number):
            return True
        return False
    
    @staticmethod
    def convert_currency_to_number(currency):
        currency = currency.replace("$","")
        currency = currency.replace(",","")
        currency = round(float(currency), 2)
        return currency
        
    @staticmethod
    def query(database, *args):
        if len(args) == 1:
            query = args[0]
            database.execute(query)
            results = database.fetchall()
        elif len(args) > 1:
            query = args[0]
            parameters = args[1:]
            database.execute(query, parameters)
            results = database.fetchall()
        else:
            return None
        if len(results) == 0:
            return None
        elif len(results) == 1:
            query_results = [dict(row) for row in results]
            return query_results[0]
        else:
            query_results = [dict(row) for row in results]
            return query_results

    @staticmethod
    def contains_emoji(text):
        for chars in text:
            if emoji.is_emoji(chars):
                return True
        return False
    

