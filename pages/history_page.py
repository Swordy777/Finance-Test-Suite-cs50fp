from .base_page import BasePage
from .locators import HistoryPageLocators


class HistoryPage(BasePage):
    """
    History Page POM.
    Contains methods for interacting with elements on the History page
    """
    
    def history_table(self):
        """Returns the table which displays user's transactions"""

        return self.retrieve_element_if_present(*HistoryPageLocators.HISTORY_TABLE)


    def history_table_headers(self):
        """Returns headers of the history table"""

        return self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_HEADERS)


    def history_rows(self):
        """Returns a list of history table rows"""

        return self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_ROWS)


    def history_table_data(self):
        """
        Collects all the cells and headers of the history table
        Then returns it in a structured format with the help of organize_cell_data()
        """

        table_cells = self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE_ROW_CELLS)
        headers = self.history_table_headers()
        return self.organize_cell_data(table_cells, headers)


    # Methods below aren't the best design, but we will leave it like this for now

    def more_history_tables(self):
        """Returns a list of elements that could match the locator for history table"""

        return self.retrieve_multiple_elements_if_present(*HistoryPageLocators.HISTORY_TABLE)


