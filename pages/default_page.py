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
        headers = [header.text for header in self.get_stocktable_headers()]
        list_from_stock_row = []
        list_of_stock_lists = []
        res = []
        i = 0
        for each_cell in cells:
            if i < len(headers):
                list_from_stock_row.append(each_cell.text)
                if i == len(headers) - 1:
                    list_of_stock_lists.append(list_from_stock_row)
                    list_from_stock_row = []
                    i = 0
                else:
                    i += 1
        for each_stock_list in list_of_stock_lists:
            res.append(dict(zip(headers, each_stock_list)))
        for each_stock in res:
            each_stock["Shares"] = int(each_stock["Shares"])
            each_stock["Price"] = self.convert_currency_to_number(each_stock["Price"])
            each_stock["TOTAL"] = self.convert_currency_to_number(each_stock["TOTAL"])
        return res

    def get_cash_cell(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE_CASH).text 

    def get_total_cell(self):
        return self.retrieve_element_if_present(*DefaultPageLocators.SHARES_TABLE_TOTAL).text
    
    def get_cash_value(self):
        return self.convert_currency_to_number(self.get_cash_cell())
    
    def get_total_value(self):
        return self.convert_currency_to_number(self.get_total_cell())