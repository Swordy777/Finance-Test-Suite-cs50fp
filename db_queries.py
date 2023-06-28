class DataBaseQueries():
    """
    Contains a common method for executing queries which is basically a decorator
    for the cursor.execute() from sqlite, and a bunch of frequently used 'common' queries    
    """
    
    def __init__(self, cursor):
        # To create an instance of this class a database cursor is required as an argument.
        self.cursor = cursor


    def query(self, *args):
        """
        Requires database connection's attribute row_factory to be set to sqlite3.Row

        Adds some more logic on top of how cursor.execute() from sqlite works
        Returns None if query result is empty; a dictionary if only one row is returned;
        a list of dictionaries if more than one row is returned
        """
        
        if len(args) == 1:
            query = args[0]
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        elif len(args) > 1:
            query = args[0]
            parameters = args[1:]
            self.cursor.execute(query, parameters)
            results = self.cursor.fetchall()
        else:
            return None
        if len(results) == 0:
            return None
        else:
            query_results = [dict(row) for row in results]
            if len(results) == 1:
                return query_results[0]
            else:            
                return query_results
            

    def mock_db_add_new_user(self, username, password):
        """Adds new user with given username and password to the users table"""

        return self.query("""
                          INSERT INTO USERS (username, 
                                             password) 
                          VALUES (?, ?);
                          """, 
                          username, 
                          password)
    

    def mock_db_add_tran(self, username, symbol, amount, price):
        """Adds a new transaction for specified user with given stock data"""

        return self.query("""
                          INSERT INTO PURCHASES (user_id, 
                                                 stockname, 
                                                 amount, 
                                                 price) 
                          VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, ?);
                          """, 
                          username, 
                          symbol.upper(), 
                          amount, 
                          price)


    def mock_db_change_cash_by(self, username, value):
        """Changes user's cash value by specified amount"""

        cash = self.users_cash(username)
        return self.query("""
                          UPDATE users SET cash = ? WHERE username = ?;
                          """,
                          cash + value, username)


    def mock_db_delete_tran_data(self, username):
        """Delete all transactions for the given user"""

        return self.query("""
                          DELETE FROM purchases 
                          WHERE user_id IN (SELECT id FROM users WHERE username = ?);
                          """, 
                          username)


    def mock_db_delete_user_data(self, username):
        """Delete user data for the given user"""
        
        return self.query("""
                          DELETE FROM users WHERE username = ?;
                          """, 
                          username)
        

    def user_data(self, username):
        """Provides information about the user from the users table"""

        return self.query("""
                          SELECT * FROM users WHERE username = ?;
                          """, 
                          username)
    

    def posessed_stocks(self, username):
        """
        Returns info about user's posessed stocks, including:
        - name of the stock
        - stock amount for each stock
        - average price of each stock
        """

        return self.query("""
                          SELECT stockname, 
                                 sum(amount) AS amount, 
                                 ROUND(SUM(price*amount)/SUM(amount), 2) AS price 
                          FROM purchases p JOIN users u ON u.id = p.user_id 
                          WHERE u.username = ? GROUP BY stockname HAVING SUM(amount) > 0;
                          """, 
                          username)
    

    def posessed_stock_names(self, username):
        """Returns the symbols of stocks in posession"""

        return self.query("""
                          SELECT DISTINCT stockname 
                          FROM purchases p JOIN users u ON p.user_id = u.id 
                          WHERE u.username=? GROUP BY p.stockname HAVING SUM(p.amount) > 0;
                          """,
                          username)


    def transactions(self, username):
        """Returns all of the transactions made by the given user"""
        
        return self.query("""
                          SELECT stockname, amount, price, timestamp
                          FROM purchases p JOIN users u ON u.id = p.user_id 
                          WHERE u.username = ?
                          ORDER BY timestamp;
                          """, 
                          username)


    def last_tran(self, username):
        """Returns the last transaction made by the given user"""

        return self.query("""
                          SELECT stockname, amount, price, timestamp
                          FROM purchases p JOIN users u ON u.id = p.user_id 
                          WHERE u.username = ?
                          ORDER BY timestamp DESC LIMIT 1;
                          """, 
                          username)


    def stock_total(self, username):
        """Returns the total amount spent on all of the stocks posessed by the given user"""

        return self.query("""
                          SELECT ROUND(SUM(amount * price), 2) as amount_x_price 
                          FROM PURCHASES p JOIN users u ON u.id = p.user_id
                          WHERE u.username = ?
                          """, 
                          username)['amount_x_price']
    

    def users_cash(self, username):
        """Returns user's current cash value"""
        
        return round(self.query("""SELECT cash FROM users WHERE username = ?;""", username)['cash'], 2)
    
