import psycopg2
import requests


class Stock:
    """
    Parent class to represent a generic stock.
    """
    def __init__(self, name, symbol, db_config, api_key):
        self.name = name
        self.symbol = symbol  # Stock symbol for API queries
        self.quantity = 0
        self.price = 0.0
        self.db_config = db_config
        self.api_key = api_key

    def connect_db(self):
        """
        Connect to the PostgreSQL database.
        """
        return psycopg2.connect(**self.db_config)

    def fetch_price(self):
        """
        Fetch the latest price of the stock from the TradingEconomics API.
        """
        try:
            url = f"https://api.tradingeconomics.com/markets/symbol/{self.symbol}?c={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if data and isinstance(data, list):
                self.price = data[0].get('Last', 0.0)
                print(f"Fetched price for {self.name}: {self.price}")
            else:
                print(f"Error fetching price for {self.name}. API response: {data}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock price for {self.name}: {e}")

    def buy(self, quantity):
        """
        Buy shares of the stock.
        """
        self.fetch_price()  # Fetch the latest price before buying
        total_cost = quantity * self.price
        self.quantity += quantity
        print(f"Bought {quantity} shares of {self.name} at {self.price} each. Total cost: {total_cost}. Total shares: {self.quantity}")

    def sell(self, quantity):
        """
        Sell shares of the stock.
        """
        if self.quantity >= quantity:
            self.fetch_price()  # Fetch the latest price before selling
            total_revenue = quantity * self.price
            self.quantity -= quantity
            print(f"Sold {quantity} shares of {self.name} at {self.price} each. Total revenue: {total_revenue}. Remaining shares: {self.quantity}")
        else:
            print(f"Error: Not enough shares to sell. You have {self.quantity} shares.")

    def update(self, new_quantity):
        """
        Update the quantity of the stock.
        """
        self.quantity = new_quantity
        print(f"Updated {self.name} to {new_quantity} shares.")

    def upload_to_db(self, customer_name):
        """
        Upload the stock data into PostgreSQL.
        """
        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            # Create table for the stock if it doesn't exist
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.name} (
                id SERIAL PRIMARY KEY,
                customer_name TEXT NOT NULL UNIQUE,
                quantity INT NOT NULL,
                last_price FLOAT NOT NULL
            );
            """
            cursor.execute(create_table_query)

            # Insert or update stock record
            insert_query = f"""
            INSERT INTO {self.name} (customer_name, quantity, last_price)
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_name)
            DO UPDATE SET quantity = EXCLUDED.quantity, last_price = EXCLUDED.last_price;
            """
            cursor.execute(insert_query, (customer_name, self.quantity, self.price))

            connection.commit()
            print(f"{self.name.capitalize()} stock data uploaded successfully.")

        except Exception as e:
            print(f"Error uploading {self.name} stock data to the database: {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()


# Subclasses for specific stocks
class Apple(Stock):
    def __init__(self, db_config, api_key):
        super().__init__('apple', 'AAPL:US', db_config, api_key)


class Cisco(Stock):
    def __init__(self, db_config, api_key):
        super().__init__('cisco', 'CSCO:US', db_config, api_key)


class ElAl(Stock):
    def __init__(self, db_config, api_key):
        super().__init__('el_al', 'ELAL:IT', db_config, api_key)


class Oracle(Stock):
    def __init__(self, db_config, api_key):
        super().__init__('oracle', 'ORCL:US', db_config, api_key)


# StockWallet to manage multiple stocks
class StockWallet:
    def __init__(self, db_config, api_key):
        self.db_config = db_config
        self.api_key = api_key
        self.stocks = {
            'apple': Apple(db_config, api_key),
            'cisco': Cisco(db_config, api_key),
            'el_al': ElAl(db_config, api_key),
            'oracle': Oracle(db_config, api_key)
        }

    def perform_action(self, stock_name, action, *args):
        """
        Perform an action (buy, sell, update, upload) on a specific stock.
        """
        stock = self.stocks.get(stock_name.lower())
        if not stock:
            print(f"Error: {stock_name} is not a valid stock.")
            return

        if action == 'buy':
            stock.buy(*args)
        elif action == 'sell':
            stock.sell(*args)
        elif action == 'update':
            stock.update(*args)
        elif action == 'upload':
            stock.upload_to_db(*args)
        else:
            print(f"Error: {action} is not a valid action.")


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

    # TradingEconomics API key
    api_key = 'your_api_key'

    wallet = StockWallet(db_config, api_key)

    # Perform actions on different stocks
    wallet.perform_action('apple', 'buy', 10)
    wallet.perform_action('cisco', 'sell', 5)  # Error: not enough shares
    wallet.perform_action('el_al', 'update', 20)
    wallet.perform_action('oracle', 'upload', 'customer_1')
