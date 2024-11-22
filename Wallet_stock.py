import psycopg2

class StockWallet:
    def __init__(self, db_config):
        """
        Initialize the stock wallet with a database configuration and an empty portfolio.
        """
        self.stocks = {
            'apple': 0,
            'cisco': 0,
            'el_al': 0,
            'oracle': 0
        }
        self.db_config = db_config

    def connect_db(self):
        """
        Connect to the PostgreSQL database.
        """
        return psycopg2.connect(**self.db_config)

    def buy_stock(self, stock_name, quantity):
        """
        Buy a stock and update the portfolio.
        """
        if stock_name in self.stocks:
            self.stocks[stock_name] += quantity
            print(f"Bought {quantity} shares of {stock_name}. Total: {self.stocks[stock_name]}")
        else:
            print(f"Error: {stock_name} is not a valid stock.")

    def sell_stock(self, stock_name, quantity):
        """
        Sell a stock and update the portfolio.
        """
        if stock_name in self.stocks:
            if self.stocks[stock_name] >= quantity:
                self.stocks[stock_name] -= quantity
                print(f"Sold {quantity} shares of {stock_name}. Total: {self.stocks[stock_name]}")
            else:
                print(f"Error: Not enough shares to sell. You have {self.stocks[stock_name]} shares.")
        else:
            print(f"Error: {stock_name} is not a valid stock.")

    def update_stock(self, stock_name, new_quantity):
        """
        Update the quantity of a stock in the portfolio.
        """
        if stock_name in self.stocks:
            self.stocks[stock_name] = new_quantity
            print(f"Updated {stock_name} to {new_quantity} shares.")
        else:
            print(f"Error: {stock_name} is not a valid stock.")

    def upload_to_db(self):
        """
        Upload the portfolio data into PostgreSQL.
        Each stock is stored in a separate table.
        """
        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            for stock_name, quantity in self.stocks.items():
                # Replace with the name of your customer, or add a column for customer ID if required.
                customer_name = 'customer_1'

                # Create a table for the stock if it doesn't exist
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {stock_name} (
                    id SERIAL PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    quantity INT NOT NULL
                );
                """
                cursor.execute(create_table_query)

                # Insert or update the stock record
                insert_query = f"""
                INSERT INTO {stock_name} (customer_name, quantity)
                VALUES (%s, %s)
                ON CONFLICT (customer_name)
                DO UPDATE SET quantity = EXCLUDED.quantity;
                """
                cursor.execute(insert_query, (customer_name, quantity))

            connection.commit()
            print("Portfolio uploaded successfully to the database.")

        except Exception as e:
            print(f"Error uploading to the database: {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()

# Example usage
if __name__ == "__main__":
    # Database configuration
    db_config = {
        'dbname': 'your_database_name',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'port': 5432
    }

    wallet = StockWallet(db_config)

    # Perform operations
    wallet.buy_stock('apple', 10)
    wallet.sell_stock('cisco', 5)  # Error: not enough shares
    wallet.update_stock('el_al', 15)
    wallet.upload_to_db()
