from .base_page import BasePage
from .locators import HistoryPageLocators
from itertools import cycle

class HistoryPage(BasePage):
    def history_table(self):
        history_table = self.retrieve_element_if_present(*HistoryPageLocators.HISTORY_TABLE)
        return history_table
    
    def history_table_headers(self):
        hist_headers = self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_HEADERS)
        return hist_headers
    
    def history_rows(self):
        hist_rows = self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_ROWS)
        return hist_rows
    
    def history_table_data(self):
        history_table_cells = self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_ROW_CELLS)
        headers = self.history_table_headers()
        return self.organize_cell_data(history_table_cells, headers)

