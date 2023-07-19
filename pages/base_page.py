import os
import re
import emoji
from urllib.parse import urlparse, unquote

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators


# Default timeout value for webpage element search (in seconds)
DEFAULT_TIMEOUT = 4
# Timeout for webpage redirect waits
TRANSITION_TO = 4


class BasePage():
    """
    BasePage POM.
    Its' methods are essential 'building blocks' for all of its' children classes.
    """

    def __init__(self, browser, url, timeout=DEFAULT_TIMEOUT):
        self.browser = browser
        self.url = url
        self.timeout = timeout
    

    def retrieve_element_if_present(self, how, what):
        """
        Looks for an element on the page for (timeout) seconds
        Returns the element object; If element wasn't found returns None
        how - alias for Selenium's find_element By strategy
        what - alias for Selenium's find_element locator argument
        """

        try:
            element = WebDriverWait(self.browser, self.timeout).until(lambda el: el.find_element(how, what))
        except TimeoutException:
            return None
        return element


    def retrieve_multiple_elements_if_present(self, how, what):
        """
        Looks for multiple elements on the page for (timeout) seconds
        Returns a list of element objects; If no element was found returns None
        how - alias for Selenium's find_elements By strategy
        what - alias for Selenium's find_elements locator argument
        """
        
        try:
            list_of_elements = WebDriverWait(self.browser, self.timeout).until(lambda el: el.find_elements(how, what))
        except TimeoutException:
            return None
        return list_of_elements
    

    def open(self):
        """Opens the URL that was used to initiate a POM object"""
        
        self.browser.get(self.url)


    def go_to_other_page(self, new_url):
        """Opens the given URL"""
        
        self.browser.get(new_url)
    

    def get_current_url(self):
        """Returns the URL for the current page"""
        
        return self.browser.current_url
    
    def refresh(self):
        """Refreshes current page"""

        self.browser.refresh()


    def url_should_change_to(self, new_url):
        """
        Waits for (timeout) seconds until current URL changes to given new_url
        Returns True if URL has changed, and False if didn't
        """
        
        try:
            WebDriverWait(self.browser, TRANSITION_TO).until(EC.url_to_be(new_url))
        except TimeoutException:
            return False
        return True
    

    def get_flash(self):
        """
        Returns Flask's 'flash' alert
        https://flask.palletsprojects.com/en/1.1.x/quickstart/#message-flashing
        """
        
        return self.retrieve_element_if_present(*BasePageLocators.ALERT_MESSAGE)
    

    def get_browser_alert(self):
        """
        Looks for a built-in browser alert for (timeout) seconds.
        If found, returns an alert object. If not, returns None
        """
        
        try:
            alert = WebDriverWait(self.browser, self.timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        return alert
    

    def get_error_image(self):
        """Returns https://memegen.link/ generated image from CS50 Finance's apology.html """
        
        return self.retrieve_element_if_present(*BasePageLocators.ERROR_IMAGE)


    def get_error_image_text(self):
        """Parces the error message from get_error_image() and returns it in text format"""
        
        error_image = self.get_error_image()
        if error_image is None:
            return None
        url = error_image.get_attribute("src")
        parsed_url = urlparse(url).path
        filename = unquote(os.path.split(parsed_url)[1])
        name = re.sub(r'-', ' ', re.sub(r'(.jpg)$', '' , filename))
        def reverse_escape(s):
            """
            Escape special characters. But in reverse!!! 
            Slightly altered escape() from CS50's Finance Problem set, as of June 2023
            
            https://github.com/jacebrowning/memegen#special-characters
            """
            for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                s = s.replace(new, old)
            return s
        return reverse_escape(name).upper()


    def get_value(self, input):
        """Returns a value of web element's attribute 'value' """
        
        return input.get_attribute("value")


    def get_placeholder(self, input):
        """Returns a value of web element's attribute 'placeholder'"""

        return input.get_attribute("placeholder")
    

    def is_unique(self, list_of_elements):
        """
        An extension for retrieve_multiple_elements_if_present()
        Checks the argument for being a one of a kind element on the webpage.
        if it is a list of length 1 returns True
        If it isn't, returns False
        """
        
        if isinstance(list_of_elements, list) and len(list_of_elements) == 1:
            return True
        else:
            return False
    

    def fill_input(self, input, text):
        """Fills the input with given text"""
        
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
    

    def set_type_to_text(self, input):
        """
        Adds/changes an elements 'type' attribute to 'text'
        Also deletes element's 'min' and 'max' attributes 
        """
        
        script = """
        var elm = arguments[0]
        var bounds = ["min", "max"]

        for (attr in bounds) {
            if(elm.hasAttribute(attr)) {
                elm.removeAttribute(attr)
            }
        }

        elm.setAttribute("type", "text") 
        """
        self.browser.execute_script(script, input)


    def organize_cell_data(self, all_cell_elements, all_header_elements):
        """
        Takes table's header and cell lists as arguments.
        Checks if division of cell count by header count doesn't provide a remainder
        Then returns a list of dictionaries structured as {header: cell value}
        If there's only one cell row, returns a dictionary for this row
        """
        
        cell_inner_text = [cell.text for cell in all_cell_elements]
        header_names = [header.text for header in all_header_elements]
        list_of_rows = []
        if len(cell_inner_text) % len(header_names) == 0:
            rows_count = int(len(cell_inner_text)/len(header_names))
            for every_row in range(rows_count):
                new_row = dict.fromkeys(header_names)
                for key in new_row:
                    new_row[key] = cell_inner_text.pop(0)
                    if self.is_integer(new_row[key]):
                        new_row[key] = int(new_row[key])
                    elif self.is_currency(new_row[key]):
                        new_row[key] = self.currency_to_number(new_row[key])
                list_of_rows.append(new_row)
            if len(list_of_rows) == 1:
                return list_of_rows[0]
            else:
                return list_of_rows
        return None
        

    @staticmethod
    def is_currency(currency):
        """
        Helper function for organize_cell_data()
        Checks if cell value is formatted as a currency by using regular expression.
        Returns True if it is, and False if it isn't
        """

        # This re expression will only recognize 'clean' currency values, like: $12,345.00
        # If you have some text around the currency, the re expression has to be changed
        if re.fullmatch(r"^\$(\d{1,3}){1}(\,\d{3})*(\.\d{2})", currency):
            return True
        return False
    

    @staticmethod
    def is_integer(number):
        """
        Helper function for organize_cell_data()
        Checks if cell value is formatted as a an integer by using regular expression.
        Returns True if it is, and False if it isn't
        """

        if re.fullmatch(r"^\-{0,1}\d*", number):
            return True
        return False
   

    @staticmethod
    def currency_to_number(currency):
        """
        Helper function for organize_cell_data()
        Strips cell value of currency formatting and casts it to float
        Only works with the basic re expression of is_currency()
        If the expression has been changed, this helper function
        has to be changed accordingly so it would return a float value
        """

        currency = currency.replace("$","")
        currency = currency.replace(",","")
        currency = round(float(currency), 2)
        
        return currency


    @staticmethod
    def contains_emoji(text):
        """
        Helper function for fill_input()
        Checks if the argument contains emoji symbols.
        Returns True if it does, and False if it doesn't
        """

        for chars in text:
            if emoji.is_emoji(chars):
                return True
        return False

