from .base_page import BasePage
from .locators import DefaultPageLocators

class DefaultPage(BasePage):
    def stocktable(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE)
    
    def stocktable_headers(self):
        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_HEADERS)
    
    def headers_names(self):
        return [header.text for header in self.stocktable_headers()]
    
    def stocktable_rows(self):
        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROWS)
    
    def stocktable_cells(self):
        cells = self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROW_CELLS)
        headers = self.stocktable_headers()
        return self.organize_cell_data(cells, headers)

    def cash_element(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.CASH_ELEMENT) 

    def total_element(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.TOTAL_ELEMENT)
    
    def cash_elm_value(self):
        return self.convert_currency_to_number(self.cash_element().text)
    
    def total_elm_value(self):
        return self.convert_currency_to_number(self.total_element().text)