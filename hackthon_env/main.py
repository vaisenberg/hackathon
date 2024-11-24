from currency_coverter_tomain import ILSConverter
from USDToILSConverter import USDToILSConverter
from EUROToILSConverter import EURConverter
from FrankToILSConverter import FConverter
from Fetch_portfolio import fetch_currency_portfolio

def fetch_balance_from_db(client_id):
    """
    Fetches the balance of a customer from the wallet or bank balance table.
    
    :param client_id: The unique ID of the client (user).
    :return: The balance of the client or None if an error occurs.
    """
    conn = connect_db()  # Connect to the database
    cursor = conn.cursor()
    balance = None

    try:
        # Fetch balance from the wallet table (or bank balance table)
        cursor.execute("SELECT amount FROM wallet WHERE client_id = %s;", (client_id,))
        result = cursor.fetchone()

        if result:  # Check if a record was found
            balance = result[0]  # The amount is stored in the first column of the result
        else:
            print(f"No balance found for client_id {client_id}.")
        
    except Exception as e:
        print(f"Error fetching balance from the database: {e}")

    finally:
        cursor.close()
        conn.close()

    return balance

def update_wallet_balance(client_id, new_balance):
    """
    Updates the user's wallet balance in the database.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE wallet SET amount = %s WHERE client_id = %s;"
    cursor.execute(query, (new_balance, client_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Wallet balance updated successfully.")

def update_currency_portfolio(client_id, currency, new_amount):
    """
    Updates the user's currency amount in the portfolio.
    """
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE portfolio SET amount = %s WHERE client_id = %s AND currency = %s;"
    cursor.execute(query, (new_amount, client_id, currency))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Portfolio updated: {currency} amount updated successfully.")



def main_menu():
    print("Welcome to the Financial Assistant!")

    ils_converter = ILSConverter()  # Instantiate the ILSConverter

    # Fetch exchange rates at the start
    if not ils_converter.fetch_exchange_rates():
        print("Failed to fetch exchange rates. Exiting...")
        return

    while True:
        print("\nMain Menu:")
        print("1. Enter new balance and check if it's greater than current balance")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                # Log in by unique number
                login_number = int(input("Enter your login (unique number): "))

                # Fetch client ID from database
                conn = connect_db()
                cursor = conn.cursor()
                query = "SELECT id FROM clients WHERE unique_number = %s;"
                cursor.execute(query, (login_number,))
                client_data = cursor.fetchone()
                cursor.close()
                conn.close()

                if client_data:
                    client_id = client_data[0]  # Extract the actual ID

                    # Fetch balance from the database
                    db_balance = fetch_balance_from_db(client_id)
                    if db_balance is None:
                        print("No balance found for this user.")
                        continue

                    print(f"Your current balance in ILS: {db_balance:.2f}")

                    # Ask the user to enter a new balance
                    new_balance = float(input("Please enter your new balance: "))

                    # Check if the new balance is greater than the existing balance
                    if new_balance > db_balance:
                        print(f"New balance of {new_balance:.2f} ILS is greater than your current balance!")
                        # You can proceed with other actions like updating the wallet or portfolio
                        update_wallet_balance(client_id, new_balance)
                        print(f"Your new balance of {new_balance:.2f} has been successfully updated.")

                    else:
                        print(f"Your new balance of {new_balance:.2f} is not greater than the current balance.")
                        update_wallet_balance(client_id, new_balance)
                        print(f"Your new balance of {new_balance:.2f} has been successfully updated.")

                    # If the balance is negative, check if they have any currency portfolio
                    if db_balance < 0:
                        print("Your balance is negative. Checking your portfolio for available currencies...")
                        portfolio = fetch_currency_portfolio(client_id)

                        if portfolio:
                            print("Your currency portfolio:")
                            for currency, amount in portfolio:
                                print(f"{currency}: {amount:.2f}")

                            # Suggest converting to Shekels
                            for currency, amount in portfolio:
                                if amount > 0:  # Only suggest conversion for non-zero holdings
                                    print(f"Suggestion: Convert {amount:.2f} {currency} to Shekels.")
                                    convert_choice = input(f"Do you want to convert {currency} to Shekels? (yes/no): ").strip().lower()
                                    if convert_choice == 'yes':
                                        converted_amount = ils_converter.convert_to(amount, "ILS")
                                        if converted_amount is not None:
                                            print(f"{amount:.2f} {currency} converts to {converted_amount:.2f} ILS.")

                                            # Update wallet balance
                                            new_wallet_balance = db_balance + converted_amount
                                            update_wallet_balance(client_id, new_wallet_balance)

                                            # Update portfolio
                                            new_currency_amount = 0  # Currency is fully converted
                                            update_currency_portfolio(client_id, currency, new_currency_amount)

                                            print("Conversion completed successfully!")
                                            # Refresh balance and portfolio
                                            db_balance = fetch_balance_from_db(client_id)
                                            portfolio = fetch_currency_portfolio(client_id)
                                    else:
                                        print(f"No conversion performed for {currency}.")
                        else:
                            print("You have no currencies in your portfolio.")
                            print("You need to cut your spending as you have no currency to sell.")
                    else:
                        print(f"Your balance is positive: {db_balance:.2f} ILS.")

                else:
                    print("Invalid login number. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
