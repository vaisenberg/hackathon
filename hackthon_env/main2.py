from currency_coverter_tomain import ILSConverter  # Assuming the ILSConverter is in this file
from Fetch_portfolio import fetch_currency_portfolio  # Assuming this function fetches portfolio from DB
import psycopg2
from psycopg2 import sql
from config import DATABASE


def connect_db():
    """
    Connects to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname="customer_data",  # Your PostgreSQL database name
        user="your_username",    # Your PostgreSQL username
        password="your_password", # Your PostgreSQL password
        host="localhost",        # Database host (default is localhost)
        port="5432"              # PostgreSQL port (default is 5432)
    )
    return conn

def check_customer_exists(customer_id):
    """
    Check if a customer exists in the SQL database by their unique ID and allow the user to update their balance.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Query to check if the customer exists
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    
    if customer:
        print(f"Customer with ID {customer_id} exists.")
        print(f"Name: {customer[1]}")  # Assuming column 1 is name
        print(f"Email: {customer[2]}")  # Assuming column 2 is email
        print(f"Current Balance: {customer[3]:.2f} ILS")  # Assuming column 3 is balance
        
        # Prompt for the new balance in Shekels
        try:
            new_balance = float(input("Enter the new balance in Shekels (ILS): "))
            
            # Update balance in the database
            cursor.execute("UPDATE customers SET balance_ils = %s WHERE customer_id = %s", (new_balance, customer_id))
            conn.commit()
            print(f"Balance for customer ID {customer_id} updated to {new_balance:.2f} ILS.")
            
            # If the new balance is greater than 500, offer conversion
            if new_balance > 500:
                offer_conversion(new_balance)
            
        except ValueError:
            print("Invalid input. Please enter a valid number for the balance.")
        
    else:
        print(f"No customer found with ID {customer_id}.")
    
    conn.close()

def offer_conversion(balance_ils):
    """
    If balance exceeds 500 ILS, offer the user to perform currency conversion.
    """
    print(f"Your balance is {balance_ils:.2f} ILS, which exceeds 500 ILS.")
    convert_option = input("Would you like to convert this balance to USD, EUR, or CHF? (yes/no): ").strip().lower()
    
    if convert_option == 'yes':
        # Initialize the ILSConverter
        ils_converter = ILSConverter()
        
        # Fetch exchange rates before performing any conversion
        if ils_converter.fetch_exchange_rates():
            target_currency = input("Enter the target currency (USD, EUR, CHF): ").strip().upper()
            
            # Validate the currency input
            if target_currency in ["USD", "EUR", "CHF"]:
                converted_amount = ils_converter.convert_to(balance_ils, target_currency)
                if converted_amount is not None:
                    print(f"{balance_ils:.2f} ILS is equivalent to {converted_amount:.2f} {target_currency}.")
            else:
                print("Invalid currency. Please choose USD, EUR, or CHF.")
        else:
            print("Failed to fetch exchange rates. Conversion cannot be performed.")
    else:
        print("You chose not to perform any conversion.")

# Main function to run the program
def main():
    customer_id = int(input("Enter the customer ID to check: "))
    check_customer_exists(customer_id)

if __name__ == "__main__":
    main()