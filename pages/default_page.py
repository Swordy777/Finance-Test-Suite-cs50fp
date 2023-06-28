from .base_page import BasePage
from .locators import DefaultPageLocators


class DefaultPage(BasePage):
    """
    Default Page POM.
    Contains methods for interacting with elements on the "default route" page
    """
    
    def stocktable(self):
        """Returns the table which displays purchased stocks"""
        
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE)
    

    def stocktable_headers(self):
        """Returns a list of the stock table headers"""
        
        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_HEADERS)
    

    def headers_names(self):
        """Returns a list of stock table header names"""
        
        return [header.text for header in self.stocktable_headers()]
    

    def stocktable_rows(self):
        """Returns a list of stock table rows"""

        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROWS)
    

    def stocktable_cells(self):
        """
        Collects all the cells and headers of the stock table
        Then returns it in a structured format with the help of organize_cell_data()
        """

        cells = self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROW_CELLS)
        headers = self.stocktable_headers()
        return self.organize_cell_data(cells, headers)


    def cash_element(self):
        """Returns cell or element containing user's cash value"""

        return self.retrieve_element_if_present(*DefaultPageLocators.CASH_ELEMENT) 


    def total_element(self):
        """Returns cell or element containing user's TOTAL value"""

        return self.retrieve_element_if_present(*DefaultPageLocators.TOTAL_ELEMENT)
    

    def cash_elm_value(self):
        """Takes cash element and returns cash value it stores"""

        return self.currency_to_number(self.cash_element().text)
    

    def total_elm_value(self):
        """Takes TOTAL element and returns TOTAL value it stores"""

        return self.currency_to_number(self.total_element().text)
    

    # Methods below aren't the best design, but we will leave it like this for now

    def more_stocktables(self):
        """Returns a list of elements that could match the locator for stock table"""

        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE)
    

    def more_cash_elements(self):
        """Returns a list of elements that could match the locator for cash element"""

        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.CASH_ELEMENT)


    def more_total_elements(self):
        """Returns a list of elements that could match the locator for TOTAL element"""

        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.TOTAL_ELEMENT)