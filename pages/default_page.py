from .base_page import BasePage
from .locators import DefaultPageLocators

class DefaultPage(BasePage):
    def get_stocktable(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE)
    
    def get_stocktable_headers(self):
        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_HEADERS)
    
    def get_stocktable_rows(self):
        return self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROWS)
    
    def get_stocktable_cells(self):
        cells = self.retrieve_multiple_elements_if_present(*DefaultPageLocators.SHARES_TABLE_ROW_CELLS)
        headers = self.get_stocktable_headers()
        return self.organize_cell_data(cells, headers)

    def get_cash_cell(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE_CASH) 

    def get_total_cell(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE_TOTAL)
    
    def get_cash_value(self):
        return self.convert_currency_to_number(self.get_cash_cell().text)
    
    def get_total_value(self):
        return self.convert_currency_to_number(self.get_total_cell().text)